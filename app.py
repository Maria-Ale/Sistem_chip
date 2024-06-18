from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import os
import mysql.connector
from werkzeug.utils import secure_filename
import traceback
import logging
from flask_paginate import Pagination, get_page_args

logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'bljr0vq6jy8iuwxtyunr-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'ufu46vgsoygusygy'
app.config['MYSQL_PASSWORD'] = '9c0J9t2qPTs2vifvEFQ1'
app.config['MYSQL_DB'] = 'sistemchip'
app.config['UPLOAD_FOLDER'] = 'static/img'
app.secret_key = 'alejandra_da'

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

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
        return render_template('usuarioRegistrado.html', session=session)
    else:
        return redirect('/login')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear-registro', methods=["GET", "POST"])
def crear_registro():
    nombre = request.form['txtNombreR']
    apellido = request.form['txtApellidoR']
    correo = request.form['txtCorreoR']
    password = request.form['txtPasswordR']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (nombre, apellido, correo, password, id_rol) VALUES (%s, %s, %s, %s, '2')", (nombre, apellido, correo, password))
    conn.commit()
    conn.close()

    return render_template("principal.html", mensaje2='Usuario Registrado')

@app.route('/cerrar-sesion', methods=['POST', 'GET'])
def cerrar_sesion():
    session.clear()
    return redirect('/')

# Seleccionar productos

@app.route('/computadores')
def computadores():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'computadores'")
    producto = cur.fetchall()
    conn.close()

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = producto[start_index:end_index]
    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('computadores.html', producto=producto_pagina, pagination=pagination)

@app.route('/celulares')
def celulares():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'celulares'")
    producto = cur.fetchall()
    conn.close()

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = producto[start_index:end_index]
    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('celulares.html', producto=producto_pagina, pagination=pagination)

@app.route('/camaras')
def camaras():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'camaras'")
    producto = cur.fetchall()
    conn.close()

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = producto[start_index:end_index]
    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('camaras.html', producto=producto_pagina, pagination=pagination)

@app.route('/impresoras')
def impresoras():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'impresoras'")
    producto = cur.fetchall()
    conn.close()

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = producto[start_index:end_index]
    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('impresoras.html', producto=producto_pagina, pagination=pagination)

@app.route('/accesorios')
def accesorios():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'accesorios'")
    producto = cur.fetchall()
    conn.close()

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = producto[start_index:end_index]
    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('accesorios.html', producto=producto_pagina, pagination=pagination)

@app.route('/relojes')
def relojes():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'relojes'")
    producto = cur.fetchall()
    conn.close()

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = producto[start_index:end_index]
    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('relojes.html', producto=producto_pagina, pagination=pagination)

@app.route('/audifonos')
def audifonos():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM producto WHERE categoria = 'audifonos'")
    producto = cur.fetchall()
    conn.close()

    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page
    producto_pagina = producto[start_index:end_index]
    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('audifonos.html', producto=producto_pagina, pagination=pagination)

@app.route('/producto', methods=['GET'])
def producto():
    id_producto = request.args.get('id', default=None, type=int)

    if id_producto is not None:
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute('SELECT * FROM producto WHERE id_producto = %s', (id_producto,))
        producto = cur.fetchone()
        conn.close()

        if producto:
            return render_template('producto.html', producto=producto)
    return render_template('producto.html')

@app.route('/registroproducto')
def registroproducto():
    return render_template('registroproducto.html')

@app.route('/create', methods=['POST'])
def create():
    codigo = request.form['txtCodigo']
    nombre = request.form['txtNombre']
    precio = request.form['txtPrecio']
    stock = request.form['txtStock']
    descripcion = request.form['txtDescripcion']
    especificacion = request.form['txtEspecificacion']
    categoria = request.form['txtCategoria']
    imagen = request.files['txtImagen']

    if imagen:
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO producto (codigo, nombre, precio, stock, descripcion, especificacion, categoria, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                (codigo, nombre, precio, stock, descripcion, especificacion, categoria, filename))
    conn.commit()
    conn.close()

    return redirect(url_for('admin2'))

@app.route('/edit/<int:id>')
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute('SELECT * FROM producto WHERE id_producto = %s', (id,))
    producto = cur.fetchone()
    conn.close()

    if producto:
        return render_template('edit.html', producto=producto)
    return redirect(url_for('admin2'))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    codigo = request.form['txtCodigo']
    nombre = request.form['txtNombre']
    precio = request.form['txtPrecio']
    stock = request.form['txtStock']
    descripcion = request.form['txtDescripcion']
    especificacion = request.form['txtEspecificacion']
    categoria = request.form['txtCategoria']
    imagen = request.files['txtImagen']

    conn = get_db_connection()
    cur = conn.cursor()
    if imagen:
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cur.execute('UPDATE producto SET codigo = %s, nombre = %s, precio = %s, stock = %s, descripcion = %s, especificacion = %s, categoria = %s, imagen = %s WHERE id_producto = %s', 
                    (codigo, nombre, precio, stock, descripcion, especificacion, categoria, filename, id))
    else:
        cur.execute('UPDATE producto SET codigo = %s, nombre = %s, precio = %s, stock = %s, descripcion = %s, especificacion = %s, categoria = %s WHERE id_producto = %s', 
                    (codigo, nombre, precio, stock, descripcion, especificacion, categoria, id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin2'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM producto WHERE id_producto = %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin2'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
