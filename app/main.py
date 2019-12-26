from flask import Flask, render_template, request, abort, json
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import os

USER_KEYS = ['name', 'last_name', 'occupation', 'follows', 'age']

# El cliente se levanta en la URL de la wiki
URL = "mongodb://grupo90:grupo90@gray.ing.puc.cl/grupo90"
client = MongoClient(URL)

# Iniciamos la aplicación de flask
app = Flask(__name__)

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
