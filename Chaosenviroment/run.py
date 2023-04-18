#Importar
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os

#Crear app medante instancia
app = Flask(__name__)

#secret key
app.config['SECRET_KEY'] = os.urandom(24)


#conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'BadLands2045.'
app.config['MYSQL_DB'] = 'chaossystem'

mysql = MySQL(app)

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


@app.route('/sesion')
def mostrarproyectos():
    return 'ola sexoso, bienvenido al sex'



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']

        # Verificar si los datos son correctos
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        cur.close()

        if user:
            # Iniciar sesión exitosamente
            return redirect(url_for('sesion'))
        else:
            # Mostrar un mensaje de error
            return 'Nombre de usuario o contraseña incorrectos'

    # Si el método es GET, mostrar el formulario de login
    return '''
        <form method="post">
            <p>Nombre de usuario: <input type="text" name="username"></p>
            <p>Contraseña: <input type="password" name="password"></p>
            <p><input type="submit" value="Iniciar sesión"></p>
        </form>
    '''

#Ejecutar nuestra app cuando ejecutemos este archivo run.py

if __name__ == '__main__':
    app.run(debug=True)