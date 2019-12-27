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

# -------- Entrega 4 --------------

@app.route("/messages/<mid>")
def get_message(mid):
    mensajes = list(correos.find({"id":mid}, {"_id":0}))
    return json.jsonify(mensajes)

@app.route("/messages/<string:id>", methods=['DELETE'])
def delete_message(id):
    correos.delete_one({"id": id})
    mensaje = f"Correo id {id} ha sido eliminado"
    return json.jsonify({'result': 'success', 'msn': mensaje})

@app.route("/messages", methods=['POST'])
def new_message():
    data = {key: request.json[key] for key in D_KEYS}
    print(data)
    count = correos.count_documents({})
    data["id"] = str(count) + "asdf"
    resultado = correos.insert_one(data)
    if (resultado):
        msn = "Correo creado con éxito :D"
        success = True
    else:
        msn = "No se pudo crear el correo :("
        success = False
    return json.jsonify({'result': success, 'msn': msn})

@app.route("/messages/")
def all_messages():
    mensajes = list(correos.find({},{"_id":0}))
    for mensaje in mensajes:
        print(mensaje)
    return json.jsonify({'result': 'Lista completa de correos', 'message': mensajes})

@app.route("/messages/project-search/<string:receiver>")
def project_search_message(receiver):
    qcorreos = list(correos.find({},{"_id":0}))
    proyectos_e = []
    for correo in qcorreos:
        if "receiver" in correo["metadata"].keys() or "sender" in correo["metadata"].keys():
            if correo["metadata"]["receiver"] == receiver or correo["metadata"]["sender"] == receiver:
                print(correo)
                proyectos_e.append(correo)
    return json.jsonify({'result': 'Correos relacionados a: {0}'.format(receiver), 'message': proyectos_e})

@app.route("/messages/content-search/")
def content_search_message():
    mensajes_d = []
    mensajes_r = []
    mensajes_f = []
    if request:
        content = request.json
        print(content)
        if "desired" in content.keys():
            for frase in content["desired"]:
                for correo in list(correos.find({}, {"_id":0})):
                    if frase in correo["content"]:
                        mensajes_d.append(correo)
        elif "required" in content.keys():
            for frase in content["required"]:
                for correo in list(correos.find({}, {"_id":0})):
                    if frase in correo["content"]:
                        mensajes_r.append(correo)
        elif "forbidden" in content.keys():
            for frase in content["forbidden"]:
                for correo in list(correos.find({}, {"_id":0})):
                    if frase in correo["content"]:
                        mensajes_f.append(correo)

        mns = mensajes_d+mensajes_r
        if intersection(mensajes_d, mensajes_r) in mns:
            mns.remove(intersection(mensajes_d, mensajes_r))
        elif mensajes_f in mns:
            mns.remove(mensajes_f)
        return json.jsonify({'result': 'Correos', 'message': mns})
    else:
        return json.jsonify({'result': 'Correos', 'message': "no hay nada que mostrar"})

def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

#------------ Entrega 5 ----------------------------

#Seleccionar colección de socios
socios = db.socios
socios_data = {}
@app.route("/info-socio/<sid>")
def info_socio(sid):
    socio = socios.find({'sid': sid})
    socio_data= {
        'nombre': socio['name'],
        'apellido': socio['last name'],
        'nacionalidad': socio['nacionality']
            } 
    correos = list(db.correos.find({},{"_id":0}))
    for correo in correos:
        if correo['metadata']["sender"] == socio['name']:
            if correo.find({'content':"\"recurso de protección\" -clausurado"}):
                if correo["metadata"]["sender"] in socios_data.keys():
                    socios_data[correo["metadata"]["sender"]] = socios_data[correo["metadata"]["sender"]] + 1
                else:
                    socios_data[correo["metadata"]["sender"]] = 1
    return json.jsonify({'result': 'correos del socio encontrados', 'message': socio_data})

#Seleccionar colección de proyectos
proyectos = db.projectos
@app.route("/info-project/")
def info_proyecto():
    qcorreos = list(correos.find({},{"_id":0}))
    proyectos_e = []
    projects = {}
    for proyecto in list(proyectos.find()):
        for correo in qcorreos:
            if "sender" in correo["metadata"].keys():
                if correo["metadata"]["sender"] == proyecto['name']:
                    if proyecto['name'] in projects.keys():
                        projects[proyecto['name']].append(correo)
                    else:
                        projects[proyecto['name']] = {'poject': proyecto, 'correos':[]}
    data = []
    for np, p in projects.items():
        info_p = {
            'name_project': np,
            'data2': p['project']['arg2'],
            'data3': p['project']['arg3'],
            'conteo': len(p['correos'])
        }
        data.append(info_p)

    return json.jsonify({'result': 'detalle de proyectos', 'message': data})

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
    app.run(debug=True)