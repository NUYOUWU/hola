from flask import Flask, render_template, redirect, request, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Agenda777"
)

cursor = db.cursor()

def encripcontra(password):
    encriptar = generate_password_hash(password)
    return encriptar


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        username = request.form.get('txtusuario')
        password = request.form.get('txtcontrasena')
        
        cursor = db.cursor()
        sql = "SELECT usuarioper, contraper, roles FROM personas WHERE usuarioper = %s"
        cursor.execute(sql, (username,))
        usuario = cursor.fetchone()
        
        if usuario is not None and check_password_hash(usuario[1], password):
            session['usuario'] = usuario[0]
            session['rol'] = usuario[2]
            if usuario[2] == 'administrador':
                return redirect(url_for('mostrar_canciones'))
            else:
                return redirect(url_for('lista'))  # Redirigir a otra página de inicio de sesión normal
        
        print('credenciales invalidas')
        flash('Credenciales inválidas, por favor inténtalo de nuevo', 'error')
    
    return render_template('login.html')
  
@app.route('/logout')
def logout():
    # Eliminar el usuario de la sesión
    session.pop('usuario', None)
    print("la sesion se cerro")
    return redirect(url_for('login'))

@app.route('/')
def lista():
    if 'usuario' in session:
        cursor.execute('SELECT * FROM personas')
        personas = cursor.fetchall()
        return render_template('index.html', personas=personas)
    else:
        return redirect(url_for('login'))

@app.route('/Registrar', methods=['GET', 'POST'])
def Registrar_usuario():
    if request.method == 'POST':
        Nombres = request.form.get('nombre')
        Apellidos = request.form.get('apellido')
        Email = request.form.get('email')
        Direccion = request.form.get('direccion')
        Telefono = request.form.get('telefono')
        Usuario = request.form.get('usuario')
        Contrasena = request.form.get('contrasena')

        Contrasenaencriptada = encripcontra(Contrasena)

        cursor.execute("SELECT * FROM personas WHERE usuarioper = %s", (Usuario,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash('Usuario ya existe')
            return redirect(url_for('Registrar_usuario'))

        cursor.execute("INSERT INTO personas(nombreper, apellidoper, emailper, dirper, telper, usuarioper, contraper, roles) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       (Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Contrasenaencriptada, 'usuario'))
        db.commit()
        flash('Usuario creado correctamente', 'success')

        return redirect(url_for('Registrar_usuario'))
    return render_template('Registrar.html')


@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar_usuario(id):
    if request.method == 'POST':
        nombreper = request.form.get('nombreper')
        apellidoper = request.form.get('apellidoper')
        emailper = request.form.get('emailper')
        dirper = request.form.get('direccionper')
        telper = request.form.get('telefonoper')
        usuarioper = request.form.get('usuarioper')
        passper = request.form.get('passwordper')

        sql = "UPDATE personas SET nombreper=%s, apellidoper=%s, emailper=%s, dirper=%s, telper=%s, usuarioper=%s, contraper=%s WHERE idper=%s"
        cursor.execute(sql, (nombreper, apellidoper, emailper, dirper, telper, usuarioper, passper, id))
        db.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('lista'))
    else:
        cursor.execute('SELECT * FROM personas WHERE idper = %s', (id,))
        data = cursor.fetchone()
        if data:
            return render_template('Editar.html', personas=data)
        else:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('lista'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    if request.method == 'POST':
        cursor.execute('DELETE FROM personas WHERE idper = %s', (id,))
        db.commit()
        flash('Usuario eliminado correctamente', 'success') 
        return redirect(url_for('lista'))




@app.route('/canciones', methods=['GET', 'POST'])
def canciones():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        artista = request.form.get('artista')
        genero = request.form.get('genero')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')
        lanzamiento = request.form.get('lanzamiento')
        cursor.execute("INSERT INTO canciones (titulo, artista, genero, precio, duracion, lanzamiento) VALUES (%s, %s, %s, %s, %s, %s)",
                       (titulo, artista, genero, precio, duracion, lanzamiento))
        db.commit()
        flash('Canción agregada correctamente', 'success')
        return redirect(url_for('canciones')) 
    else:
        cursor.execute('SELECT * FROM canciones')
        canciones = cursor.fetchall()
        return render_template('canciones.html', canciones=canciones)



@app.route('/compras', methods=['GET', 'POST'])
def compras():
    if request.method == 'POST':
        id_compra = request.form.get('id_compra')
        fecha_compra = request.form.get('fecha_compra')
        precio = request.form.get('precio')
        user_id = request.form.get('user_id')
        cancion_id = request.form.get('cancion_id')
        metodo_pago = request.form.get('metodo_pago')
        
        # Validación de userId
        if user_id is None:
            flash('Por favor, proporcione un ID de usuario válido', 'error')
            return redirect(url_for('compras'))
        
        cursor.execute("INSERT INTO compras (id_compra, fechaCompra, precio, userId, id_cancion, metodoPago) VALUES (%s, %s, %s, %s, %s, %s)",
                       (id_compra, fecha_compra, precio, user_id, cancion_id, metodo_pago))
        db.commit()
        flash('Compra realizada correctamente', 'success')
        return redirect(url_for('compras')) 
    else:
        cursor.execute('SELECT * FROM compras')
        compras = cursor.fetchall()
        return render_template('compras.html', compras=compras)





if __name__ == '__main__':
    app.run(debug=True, port=5005)