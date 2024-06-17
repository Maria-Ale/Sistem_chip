from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import os
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import traceback
import logging
from flask_paginate import Pagination, get_page_args
logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sistemchip'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def principal():
    return render_template('principal.html')




@app.route('/productos-tienda', methods=['GET'])
def tienda():
    page = request.args.get('page', 1, type=int)

    # Definir la cantidad de productos por página
    producto_per_page = 9

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto")
    producto = cur.fetchall()

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page

    # Seleccionar los productos correspondientes a la página actual
    producto_pagina = producto[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')

    return render_template('tienda.html', producto=producto_pagina, pagination=pagination)


@app.route('/productos', methods=['GET'])
def principalAdmin():
    page = request.args.get('page', 1, type=int)

    # Definir la cantidad de productos por página
    producto_per_page = 9

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto")
    producto = cur.fetchall()

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page

    # Seleccionar los productos correspondientes a la página actual
    producto_pagina = producto[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(producto), per_page=producto_per_page, css_framework='bootstrap4')

    return render_template('principalAdmin.html', producto=producto_pagina, pagination=pagination)




from flask import request

@app.route('/shop')
def shop():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto")
    producto = cur.fetchall()
    return render_template('shop.html', producto=producto)

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/contacto')
def contacto():
    
    return render_template('contacto.html')

@app.route('/admin2')
def admin2():
    
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM producto')
        producto = cur.fetchall()

        return render_template('admin2.html', producto=producto)

    

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form and 'txtNombre' in request.form and 'txtApellido' in request.form:
        _nombre = request.form['txtNombre']
        _apellido = request.form['txtApellido']
        _correo = request.form['txtCorreo']
        _password = request.form['txtPassword']

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE nombre = %s AND apellido = %s AND correo = %s AND password = %s', (_nombre, _apellido, _correo, _password))

        account = cur.fetchone()
        cur.close()

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
    # Verifica si el usuario está logueado antes de mostrar la página
    if 'logueado' in session and session['logueado']:
        print(session)
        return render_template('usuarioRegistrado.html', session=session)
    else:
        return redirect('/login')  # Redirige al login si el usuario no está logueado

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/crear-registro', methods = ["GET", "POST"])
def crear_registro():
    nombre = request.form['txtNombreR']
    apellido = request.form['txtApellidoR']
    correo = request.form['txtCorreoR']
    password = request.form['txtPasswordR']

    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO usuarios (nombre, apellido, correo, password, id_rol) VALUES (%s, %s, %s, %s, '2')", (nombre, apellido, correo, password))
    mysql.connection.commit()

    return render_template("principal.html", mensaje2='Usuario Registrado') 

@app.route('/cerrar-sesion', methods=['POST', 'GET'])
def cerrar_sesion():
    # Limpiar la sesión y redirigir al inicio
    session.clear()
    return redirect('/')

# Seleccionar productos -------------------------

@app.route('/computadores')
def computadores():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto WHERE categoria = 'computadores'")
    producto = cur.fetchall()

    # Filtra los productos de la categoría 'dulceria'
    productos_computadores = [producto for producto in producto if producto['categoria'] == 'computadores']

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page

    # Seleccionar los productos correspondientes a la página actual
    producto_pagina = productos_computadores[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(productos_computadores), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('computadores.html', producto=producto_pagina, pagination=pagination)


@app.route('/celulares')
def celulares():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto WHERE categoria = 'celulares'")
    producto = cur.fetchall()

    # Filtra los productos de la categoría 'dulceria'
    productos_celulares = [producto for producto in producto if producto['categoria'] == 'celulares']

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page

    # Seleccionar los productos correspondientes a la página actual
    producto_pagina = productos_celulares[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(productos_celulares), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('celulares.html', producto=producto_pagina, pagination=pagination)

@app.route('/camaras')
def camaras():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto WHERE categoria = 'celulares'")
    producto = cur.fetchall()

    # Filtra los productos de la categoría 'dulceria'
    productos_camaras = [producto for producto in producto if producto['categoria'] == 'camaras']

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page

    # Seleccionar los productos correspondientes a la página actual
    producto_pagina = productos_camaras[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(productos_camaras), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('camaras.html', producto=producto_pagina, pagination=pagination)

@app.route('/impresoras')
def impresoras():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto WHERE categoria = 'impresoras'")
    producto = cur.fetchall()

    # Filtra los productos de la categoría 'dulceria'
    productos_impresoras = [producto for producto in producto if producto['categoria'] == 'impresoras']

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page

    # Seleccionar los productos correspondientes a la página actual
    producto_pagina = productos_impresoras[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(productos_impresoras), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('impresoras.html', producto=producto_pagina, pagination=pagination)

@app.route('/accesorios')
def accesorios():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto WHERE categoria = 'accesorios'")
    producto = cur.fetchall()

    # Filtra los productos de la categoría 'dulceria'
    productos_accesorios = [producto for producto in producto if producto['categoria'] == 'accesorios']

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page

    # Seleccionar los productos correspondientes a la página actual
    producto_pagina = productos_accesorios[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(productos_accesorios), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('accesorios.html', producto=producto_pagina, pagination=pagination)

@app.route('/relojes')
def relojes():
    page = request.args.get('page', 1, type=int)
    producto_per_page = 8
        
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto WHERE categoria = 'relojes'")
    producto = cur.fetchall()

    # Filtra los productos de la categoría 'dulceria'
    productos_relojes = [producto for producto in producto if producto['categoria'] == 'relojes']

    # Calcular el índice de inicio y fin para los productos en la página actual
    start_index = (page - 1) * producto_per_page
    end_index = start_index + producto_per_page

    # Seleccionar los productos correspondientes a la página actual
    producto_pagina = productos_relojes[start_index:end_index]

    # Configurar la paginación
    pagination = Pagination(page=page, total=len(productos_relojes), per_page=producto_per_page, css_framework='bootstrap4')
    return render_template('relojes.html', producto=producto_pagina, pagination=pagination)

#---------------------------------- AGREGAR PRODUCTOS--------------------------------------------



@app.route('/agregarProducto', methods=['GET'])
def prod():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM producto")
    producto = cur.fetchall()

    return render_template('agregarProducto.html', producto=producto)

@app.route('/agregar-productos', methods=['POST'])
def agregarPro():
    try:
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']

        # Guarda la imagen en tu directorio de imágenes estáticas
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(imagen.filename)))

        # Obtén la ruta de la imagen para almacenarla en la base de datos
        imagen_path = secure_filename(imagen.filename)

        cur = mysql.connection.cursor()
        sql = "INSERT INTO producto (nombre, categoria, descripcion, precio, imagen) VALUES (%s, %s, %s, %s, %s)"
        data = (nombre, categoria, descripcion, precio, imagen_path)
        cur.execute(sql, data)
        mysql.connection.commit()
        
        return redirect('/admin2')
    
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        logging.error(f"Error inesperado: {str(e)}", exc_info=True)  # Loggea el error
        # Añade un mensaje de error en la respuesta para ayudar con la depuración
    return render_template('error500.html', mensaje='Error inesperado'), 500



@app.route("/eliminar-producto", methods=['POST'])
def borraProducto():
    cur = mysql.connection.cursor()
    producto_id = request.form['producto_id']
    sql = "DELETE FROM producto WHERE producto_id = %s"
    data = (producto_id,)
    cur.execute(sql,data)
    mysql.connection.commit()
    return redirect('/admin2')

#---------------------------------- AGREGAR PRODUCTOS--------------------------------------------

#-------------CARRITO DE COMPRAS------------
from flask import jsonify


@app.route('/ver-carrito')
def ver_carrito():

    if 'id' not in session:
        return redirect(url_for('login'))

    id_usuario = session['id']

    cur = mysql.connection.cursor()
    cur.execute("SELECT carrito.id_carrito, producto.nombre, producto.precio, producto.imagen, carrito.cantidad FROM carrito INNER JOIN producto ON carrito.id_producto = producto.producto_id WHERE carrito.id_usuario = %s", (id_usuario,))
    carrito = cur.fetchall()
    cur.close()

    return render_template('carrito.html', carrito=carrito)


@app.route('/agregar-al-carrito/<int:producto_id>', methods=['POST'])
def agregar_al_carrito(producto_id):
    if 'id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 401

    id_usuario = session['id']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO carrito (id_usuario, id_producto, cantidad) VALUES (%s, %s, 1)", (id_usuario, producto_id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Producto agregado al carrito exitosamente'})

@app.route('/eliminar-del-carrito/<int:id_carrito>', methods=['POST'])
def eliminar_del_carrito(id_carrito):
    try:
        if 'id' not in session:
            return jsonify({'error': 'Usuario no autenticado'}), 401

        id_usuario = session['id']

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM carrito WHERE id_carrito = %s AND id_usuario = %s", (id_carrito, id_usuario))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Producto eliminado del carrito exitosamente'})

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return jsonify({'error': 'Error al eliminar producto del carrito'}), 500



# Errores

@app.route('/generar_error_500')
def generar_error_500():
    # Intenta ejecutar una consulta incorrecta a propósito
    try:
        cursor = mysql.get_db().cursor()
        cursor.execute("SELECT * FROM tabla_inexistente")
    except Exception as e:
        # Genera un error 500 con el mensaje de la excepción
        return render_template('error500.html', error=str(e)), 500

@app.route('/generar_error_400')
def generar_error_400():
    # Genera un error 400 con un mensaje específico
    error_message = "Esta es una solicitud incorrecta. Verifica los parámetros y vuelve a intentarlo."
    return render_template('error400.html', error=error_message), 400

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html'), 404

@app.errorhandler(401)
def error_401_handler(e):
    return render_template('error401.html'), 401



if __name__ == '__main__':
    app.secret_key = 'alejandra_da'
    app.run(debug=True)
