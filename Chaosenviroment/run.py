#Importar
from flask import Flask, request, redirect, url_for, flash
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

#metodo para verificacion de usuario
def verificar_login(username, password):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    else:
        return None

# Crea una función load_user(user_id) que busca y devuelve un objeto User en la base de datos correspondiente al user_id proporcionado.
@login_manager.user_loader
def load_user(id):
   cur = mysql.connection.cursor()
   cur.execute('SELECT * FROM users WHERE id = %s', (id))
   user_data = cur.fetchone()
   cur.close()
   if user_data:
      return User(user_data[0], user_data[1], user_data[2])
   else:
     return None

# Crea una función de verificación de inicio de sesión (login) que recibe un usuario y una contraseña y devuelve un objeto User si la autenticación es correcta o None en caso contrario.
def verificar_login(username, password):
    cur = mysql.connection.cursor()
    cur.execute('SELECT username, password FROM users WHERE username = %s AND password = %s', (username, password))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    else:
        return None

# Agrega la decoración @login_manager.unauthorized_handler encima de la función de verificación de inicio de sesión para manejar la redirección a la página de inicio de sesión en caso de que el usuario no esté autenticado.
@login_manager.unauthorized_handler
def unauthorized():
    return "no tai registrao"

#secret key
app.config['SECRET_KEY'] = os.urandom(24)


#Crear rutas con sus correspondientes funciones
@app.route('/')
def holamundo():
    return 'sistema del caos activado'

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
    
    return '''
        <h2>Registro</h2>
        <form method="POST">
        <div class="form-group">
      <label for="username">Nombre:</label>
      <input type="text" name="username" id="name" class="form-control" required>
        </div>
        <div class="form-group">
      <label for="email">Email:</label>
      <input type="email" name="email" id="email" class="form-control" required>
    </div>
    <div class="form-group">
      <label for="password">Contraseña:</label>
      <input type="password" name="password" id="password" class="form-control" required>
    </div>
    <button type="submit" class="btn btn-primary">Registrarse</button>
  </form>
        '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']
        id = request.form['id']

        # Verificar si los datos son correctos
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s AND password = %s AND id = %s', (username, password, id))
        user = cur.fetchone()
        cur.close()

        if user:
            # Iniciar sesión exitosamente
            return redirect(url_for('privado'))
        else:
            # Mostrar un mensaje de error
            return 'Nombre de usuario o contraseña incorrectos'

    # Si el método es GET, mostrar el formulario de login
    return '''
        <form method="post">
            <p>Nombre de usuario: <input type="text" name="username"></p>
            <p>Contraseña: <input type="password" name="password"></p>
            <p>ID: <input type="number" name="id"</p>
            <p><input type="submit" value="Iniciar sesión"></p>
        </form>
    '''

@app.route('/privado')
@login_required
def privado():
    return 'Bienvenido al sistema del caos mi estimado wapeton'

#Ejecutar nuestra app cuando ejecutemos este archivo run.py

if __name__ == '__main__':
    app.run(debug=True)