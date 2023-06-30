# Del módulo flask importar la clase Flask y los métodos jsonify,request
from flask import Flask ,jsonify ,request
# Del módulo flask_cors importar CORS, se usa en una api rest, permite conectar desde el frontend a una api.
from flask_cors import CORS
# Los siguientes módulos ayudan al manejo de la base de datos.
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app=Flask(__name__) # crear el objeto app de la clase Flask
CORS(app) # Módulo cors es para que me permita acceder desde el frontend al backend.

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sqluser:password@localhost/proyecto'
# URI de la BBDD. Driver de la BD user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none

db= SQLAlchemy(app) #crea el objeto db de la clase SQLAlchemy

ma=Marshmallow(app) #crea el objeto ma de de la clase Marshmallow


# Definir la tabla
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self, nombre, precio, stock, imagen):
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.imagen = imagen

with app.app_context():
    db.create_all() # Acá crea todas las tablas

class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock','imagen')
        
# El objeto producto_schema es para traer un producto
producto_schema=ProductoSchema()
# El objeto productos_schema es para traer múltiples registros de producto
productos_schema=ProductoSchema(many=True)

@app.route('/productos',methods=['GET'])
def get_productos():
    # El metodo query.all() lo hereda de db.Model
    # Permite obtener todos los datos de la tabla Producto
    all_productos=Producto.query.all()
    # Transforma un listado de objetos a JSON
    return productos_schema.jsonify(all_productos)

@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    # request.json contiene el json que envio el cliente
    # Para insertar registro en la tabla de la base de datos
    # Se usará la clase Producto pasándole cada dato recibido.
    # Para agregar los cambios a la db con db.session.add(objeto)
    # Para guardar los cambios a la db con db.session.commit()
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']
    new_producto=Producto(nombre,precio,stock,imagen)
    db.session.add(new_producto)
    db.session.commit()
    # Retornar los datos guardados en formato JSON
    # Para ello, usar el objeto producto_schema para que convierta con
    # jsonify los datos recién ingresados que son objetos a JSON
    return producto_schema.jsonify(new_producto)

@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    # Consultar por id, a la clase Producto.
    # Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
    # Retorna el JSON de un producto recibido como parámetro
    # Para ello, usar el objeto producto_schema para que convierta con
    # jsonify los datos recién ingresados que son objetos a JSON
    return producto_schema.jsonify(producto)

@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    # Consultar por id, a la clase Producto.
    # Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
    # A partir de db y la sesión establecida con la base de datos borrar
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(producto)
    db.session.commit()
    # Devuelve un json con el registro eliminado
    # Para ello, usar el objeto producto_schema para que convierta con
    # jsonify el dato recién eliminado que son objetos a JSON
    return producto_schema.jsonify(producto)

@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    # Consultar por id, a la clase Producto.
    # Se hace una consulta (query) para obtener (get) un registro por id
    producto=Producto.query.get(id)
    # Recibir los datos a modificar
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']
    # Del objeto resultante de la consulta modificar los valores
    producto.nombre=nombre
    producto.precio=precio
    producto.stock=stock
    producto.imagen=imagen
    # Guardar los cambios
    db.session.commit()
    # Para ello, usar el objeto producto_schema para que convierta con
    # jsonify el dato recién eliminado que son objetos a JSON
    return producto_schema.jsonify(producto)

# programa principal *******************************
if __name__=='__main__':
    # Ejecuta el servidor Flask
    app.run(debug=True)