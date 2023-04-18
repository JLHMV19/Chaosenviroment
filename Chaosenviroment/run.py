#Importar
from flask import Flask
from flask_mysqldb import MySQL

#Crear app medante instancia
app = Flask(__name__)

#Crear rutas con sus correspondientes funciones
@app.route('/')
def holamundo():
    return 'sistema del caos activado'

@app.route('/sistemadelcaos')
def mostrarproyectos():
    return 'aqui tendre la maquina de API'

#Ejecutar nuestra app cuando ejecutemos este archivo run.py

if __name__ == '__main__':
    app.run(debug=True)