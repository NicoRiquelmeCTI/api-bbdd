from flask import Flask, render_template, request, abort, json
from pymongo import MongoClient
import pandas as pd
import os
import atexit
import subprocess

#Instanciar las llaves del documento
D_KEYS = ["id", "content", "metadata"]
METADATA_KEYS = ["time", "sender", "receiver"]
USER_KEYS = ['name', 'last_name', 'occupation', 'follows', 'age']

#Levantar servidor de Mongo
mongod = subprocess.Popen("mongod", stdout=subprocess.DEVNULL)

uri = "mongodb://grupo58:grupo58@gray.ing.puc.cl/grupo58"
# La uri 'estándar' es "mongodb://user:password@ip/database"
atexit.register(mongod.kill)
client = MongoClient(uri)
db = client.get_database()

#Seleccionar colección de correos
correos = db.correos

#Instanciar aplicación de Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Bienvenido</h1>"

@app.route("/message/<string:mid>")
def get_message(mid):
    mensajes = list(correos.find(mid))
    return json.jsonify(mensajes)

@app.route("/message/<string:id>", methods=['DELETE'])
def delete_message(id):
    correos.delete_one({"id": id})
    mensaje = f"Correo id {id} ha sido eliminado"
    return json.jsonify({'result': 'success', 'msn': mensaje})

@app.route("/message/", methods=['POST'])
def new_message():
    return

@app.route("/messages/project-search<string:receiver>")
def project_search_message(receiver):
    correos.createIndex({"metadata.sender":"text"})
    encontrados_sender = entidades.find({$text: {$search: "\"receiver\""}},{"metadata.sender":1})
    encontrados_rec = entidades.find({$text: {$search: "\"receiver\""}},{"metadata.receiver":1})
    encontrados = encontrados_sender + encontrados_rec
    return json.jsonify(encontrados)

@app.route("/messages/content-search<string:content>")
def content_search_message(content):
    return

@app.route("/")
def home():
    return "<h1>HELLO</h1>"

# Mapeamos esta función a la ruta '/plot' con el método get.
@app.route("/plot")
def plot():
    # Export la figura para usarla en el html
    pth = os.path.join('static', 'plot.png')

    # Retorna un html "rendereado"
    return render_template('plot.html')

@app.route("/users")
def get_users():
    # Omitir el _id porque no es json serializable
    resultados = ['Pedro', 'Juan', 'Diego']
    return json.jsonify(resultados)

@app.route("/users", methods=['POST'])
def create_user():
    '''
    Crea un nuevo usuario en la base de datos
    Se  necesitan todos los atributos de model, a excepcion de _id
    '''
    return json.jsonify({'success': True, 'message': 'Usuario con id 1 creado'})

@app.route("/test")
def test():
    # Obtener un parámero de la URL
    param = request.args.get('name', False)
    print("URL param:", param)

    # Obtener un header
    param2 = request.headers.get('name', False)
    print("Header:", param2)

    # Obtener el body
    body = request.data
    print("Body:", body)

    return "OK"

if __name__ == "__main__":
    app.run()
