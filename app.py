from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import os
import mysql.connector
from werkzeug.utils import secure_filename
import traceback
import logging
from flask_paginate import Pagination, get_page_args

logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistemchip'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def principal():
    return render_template('principal.html')

@app.route('/productos-tienda', methods=['GET'])
def tienda():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 9

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto")
    producto = cur.fetchall()
    cur.close()
    conn.close()

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = producto[start_index:end_index]

    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')

    return render_template('tienda.html', producto=producto_pagina, pagination=pagination)

@app.route('/productos', methods=['GET'])
def principalAdmin():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 9

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto")
    producto = cur.fetchall()
    cur.close()
    conn.close()

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = producto[start_index:end_index]

    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')

    return render_template('principalAdmin.html', producto=producto_pagina, pagination=pagination)

@app.route('/shop')
def shop():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto")
    producto = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('shop.html', producto=producto)

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/admin2')
def admin2():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM producto')
    producto = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin2.html', producto=producto)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form and 'txtNombre' in request.form and 'txtApellido' in request.form:
        _nombre = request.form['txtNombre']
        _apellido = request.form['txtApellido']
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM usuarios WHERE nombre = %s AND apellido = %s AND correo = %s AND password = %s', (_nombre, _apellido, _correo, _password))

        account = cur.fetchone()
        cur.close()
        conn.close()

        if account:
            session['logueado'] = True
            session['id'] = account['id']
            session['nombre'] = account['nombre']
            session['apellido'] = account['apellido']
            session['id_rol'] = account['id_rol']

            if session['id_rol'] == 1:
                return render_template("principalAdmin.html")
            elif session['id_rol'] == 2:
                return render_template("principal.html")
        else:
            return render_template('error401.html', mensaje='Necesita Loguearse'), 401
    return render_template('login.html')

@app.route('/usuarioRegistrado', methods=['GET', 'POST'])
def usuarioRegistrado():
    if 'logueado' in session and session['logueado']:
        print(session)
        return render_template('usuarioRegistrado.html', session=session)
    else:
        return redirect('/login')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear-registro', methods = ["GET", "POST"])
def crear_registro():
    nombre = request.form['txtNombreR']
    apellido = request.form['txtApellidoR']
    correo = request.form['txtCorreoR']
    password = request.form['txtPasswordR']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (nombre, apellido, correo, password, id_rol) VALUES (%s, %s, %s, %s, '2')", (nombre, apellido, correo, password))
    conn.commit()
    cur.close()
    conn.close()

    return render_template("principal.html", mensaje2='Usuario Registrado')

@app.route('/cerrar-sesion', methods=['POST', 'GET'])
def cerrar_sesion():
    session.clear()
    return redirect('/')

@app.route('/computadores')
def computadores():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'computadores'")
    producto = cur.fetchall()
    cur.close()
    conn.close()

    productos_computadores = [producto for producto in producto if producto['categoria'] == 'computadores']

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = productos_computadores[start_index:end_index]

    pagination = Pagination(page=page, total=len(productos_computadores), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('computadores.html', producto=producto_pagina, pagination=pagination)

@app.route('/celulares')
def celulares():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'celulares'")
    producto = cur.fetchall()
    cur.close()
    conn.close()

    productos_celulares = [producto for producto in producto if producto['categoria'] == 'celulares']

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = productos_celulares[start_index:end_index]

    pagination = Pagination(page=page, total=len(productos_celulares), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('celulares.html', producto=producto_pagina, pagination=pagination)

@app.route('/camaras')
def camaras():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'camaras'")
    producto = cur.fetchall()
    cur.close()
    conn.close()

    productos_camaras = [producto for producto in producto if producto['categoria'] == 'camaras']

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = productos_camaras[start_index:end_index]

    pagination = Pagination(page=page, total=len(productos_camaras), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('camaras.html', producto=producto_pagina, pagination=pagination)

@app.route('/impresoras')
def impresoras():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'impresoras'")
    producto = cur.fetchall()
    cur.close()
    conn.close()

    productos_impresoras = [producto for producto in producto if producto['categoria'] == 'impresoras']

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = productos_impresoras[start_index:end_index]

    pagination = Pagination(page=page, total=len(productos_impresoras), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('impresoras.html', producto=producto_pagina, pagination=pagination)

@app.route('/accesorios')
def accesorios():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'accesorios'")
    producto = cur.fetchall()
    cur.close()
    conn.close()

    productos_accesorios = [producto for producto in producto if producto['categoria'] == 'accesorios']

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = productos_accesorios[start_index:end_index]

    pagination = Pagination(page=page, total=len(productos_accesorios), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('accesorios.html', producto=producto_pagina, pagination=pagination)

@app.route('/crear')
def crear():
    return render_template('productos/crear.html')

@app.route('/editar')
def editar():
    return render_template('productos/editar.html')

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    _nombre = request.form['txtNombre']
    _precio = request.form['txtPrecio']
    _stock = request.form['txtStock']
    _categoria = request.form['txtCategoria']
    _imagen = request.files['txtImagen']

    if _imagen:
        imagen_filename = secure_filename(_imagen.filename)
        _imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
        _imagen_url = f'img/{imagen_filename}'
    else:
        _imagen_url = None

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO producto (nombre, precio, stock, categoria, imagen) VALUES (%s, %s, %s, %s, %s)",
                (_nombre, _precio, _stock, _categoria, _imagen_url))
    conn.commit()
    cur.close()
    conn.close()

    return redirect('/productos')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM producto WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/productos')

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE id=%s", (id,))
    producto = cur.fetchone()
    cur.close()
    conn.close()

    if request.method == 'POST':
        _nombre = request.form['txtNombre']
        _precio = request.form['txtPrecio']
        _stock = request.form['txtStock']
        _categoria = request.form['txtCategoria']
        _imagen = request.files['txtImagen']

        if _imagen:
            imagen_filename = secure_filename(_imagen.filename)
            _imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], imagen_filename))
            _imagen_url = f'img/{imagen_filename}'
        else:
            _imagen_url = producto['imagen']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE producto
            SET nombre = %s,
                precio = %s,
                stock = %s,
                categoria = %s,
                imagen = %s
            WHERE id = %s
        """, (_nombre, _precio, _stock, _categoria, _imagen_url, id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/productos')

    return render_template('productos/editar.html', producto=producto)

@app.route('/usuarios', methods=['GET'])
def usuarios():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM usuarios")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
    usuario = cur.fetchone()
    cur.close()
    conn.close()

    if request.method == 'POST':
        _nombre = request.form['txtNombre']
        _apellido = request.form['txtApellido']
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']
        _id_rol = request.form['txtRol']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE usuarios
            SET nombre = %s,
                apellido = %s,
                correo = %s,
                password = %s,
                id_rol = %s
            WHERE id = %s
        """, (_nombre, _apellido, _correo, _password, _id_rol, id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/usuarios')

    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/usuarios')

@app.route('/usuarios/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        _nombre = request.form['txtNombre']
        _apellido = request.form['txtApellido']
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']
        _id_rol = request.form['txtRol']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuarios (nombre, apellido, correo, password, id_rol) VALUES (%s, %s, %s, %s, %s)",
                    (_nombre, _apellido, _correo, _password, _id_rol))
        conn.commit()
        cur.close()
        conn.close()

        return redirect('/usuarios')

    return render_template('agregar_usuario.html')

@app.route('/logout')
def logout():
    session.pop('logueado', None)
    session.pop('id', None)
    session.pop('nombre', None)
    session.pop('apellido', None)
    session.pop('id_rol', None)
    return redirect(url_for('login'))

# Carrito de Compras
@app.route('/agregar_carrito/<int:id>')
def agregar_carrito(id):
    if 'carrito' not in session:
        session['carrito'] = {}
    carrito = session['carrito']

    if id not in carrito:
        carrito[id] = 1
    else:
        carrito[id] += 1

    session['carrito'] = carrito
    return redirect('/ver_carrito')

@app.route('/ver_carrito')
def ver_carrito():
    if 'carrito' not in session:
        session['carrito'] = {}
    carrito = session['carrito']

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    if carrito:
        producto_ids = ','.join(map(str, carrito.keys()))
        cur.execute(f"SELECT * FROM producto WHERE id IN ({producto_ids})")
        productos = cur.fetchall()
        for producto in productos:
            producto['cantidad'] = carrito[str(producto['id'])]
    else:
        productos = []

    cur.close()
    conn.close()
    return render_template('carrito.html', productos=productos)

@app.route('/eliminar_carrito/<int:id>')
def eliminar_carrito(id):
    if 'carrito' in session:
        carrito = session['carrito']
        if str(id) in carrito:
            del carrito[str(id)]
            session['carrito'] = carrito
    return redirect('/ver_carrito')

@app.route('/vaciar_carrito')
def vaciar_carrito():
    session.pop('carrito', None)
    return redirect('/ver_carrito')

if __name__ == '__main__':
    app.secret_key = 'secret_key'
    app.run(debug=True)
