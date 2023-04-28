#Importar
from flask import Flask, request, redirect, url_for, flash, render_template 
from flask_mysqldb import MySQL
import os
from flask_login import login_required, current_user
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

#Crear app medante instancia
app = Flask(__name__)

#conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'BadLands2045.'
app.config['MYSQL_DB'] = 'chaossystem'

mysql = MySQL(app)

#crear objeto de autenticacion
login_manager = LoginManager()
login_manager.init_app(app)

#definicio de la clase usuario
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

#secret key
app.config['SECRET_KEY'] = os.urandom(24)


#Crear rutas con sus correspondientes funciones
@app.route('/')
def holamundo():
    return render_template("intento.html")

#Maquina de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Crear un cursor para interactuar con la base de datos
        cur = mysql.connection.cursor()
        
        # Insertar los datos en la tabla de usuarios
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        
        # Guardar los cambios en la base de datos
        mysql.connection.commit()
        
        # Cerrar la conexión con la base de datos
        cur.close()
        
        # Redirigir al usuario a la página de inicio de sesión
        flash('Registro exitoso. Por favor, inicie sesión.')
        return redirect(url_for('login'))
    
    return render_template("register2.html")

#funcion login_loader
@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    else:
        return None

#esta funcion verifica el login y devuelve el objeto user
def verificar_login(username, password):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    else:
        return None

#esta es la ruta de ejecucion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']

        # Verificar si los datos son correctos
        user = verificar_login(username, password)
        if user:
            # Iniciar sesión exitosamente
            login_user(user)

            # Redirigir al usuario a la página que intentaba acceder originalmente
            next_page = request.args.get('next')
            return redirect(next_page or url_for('privado'))
        else:
            # Mostrar un mensaje de error
            return 'Nombre de usuario o contraseña incorrectos'

    # Si el método es GET, mostrar el formulario de login
    return render_template("login.html")



@app.route('/privado')
@login_required
def privado():
    return 'Bienvenido al sistema del caos mi estimado wapeton'

#Ejecutar nuestra app cuando ejecutemos este archivo run.py
if __name__ == '__main__':
    app.run(debug=True)