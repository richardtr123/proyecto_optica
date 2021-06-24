from re import template
from flask import Flask
# Referencia a herramientas y librerias
from flask import render_template, request
from flaskext.mysql import MySQL  # Base del modulo de Mysql
# TODO: DETALLES BD
app = Flask(__name__)  # *Aca creamos la aplicacion

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Optica'

mysql = MySQL()
mysql.init_app(app)

# TODO: DETALLES BD


@app.route('/')  # Recibe solicitudes mediante la url
def index():  # def index()<--- nombre de la funcion
    return render_template('inventario/index.html')

# si clonaste esto es porque ya aprendiste a actulizar desde la master


@app.route('/insertar_producto')
def insertar_producto():
    return render_template('inventario/insertar_producto.html')


@app.route('/almacenar_pro', methods=['POST'])
def almacenarproducto():
    # recepcion de datos
    _nombre = request.form['nombre-pro']
    _marca = request.form['marca-pro']
    _material = request.form['material-pro']
    _forma = request.form['forma']
    _codigo = request.form['codigo-pro']
    _categoria = request.form['categoria-pro']
    _stock = request.form['stock-pro']
    _genero = request.form['genero-pro']
    _color = request.form['color-pro']
    _precio = request.form['precio-pro']
    _foto = request.files['imagen-pro']
    _uv = request.form['uv-pro']
 # recepcion de datos
    sql = "INSERT INTO `Optica`.`PRODUCTO` (`pro_nombre`,`pro_cat_fk`, `pro_stock`, `pro_color`, `pro_material`, `pro_precio`, `pro_marca`, `pro_num`, `pro_proteccionuv`, `pro_forma`, `pro_genero`,`pro_imagen`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # los parametros segun el orden de datos
    datos = (_nombre, _categoria, _stock, _color, _material,
             _precio, _marca, _codigo, _uv, _forma, _genero, _foto.filename)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()  # Commit hace que la conexion se termine
    return render_template('inventario/index.html')


if __name__ == '__main__':  # para empezar la aplicacion
    app.run(debug=True)
