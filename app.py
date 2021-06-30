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
    _nombre = ""
    _marca = ""
    _codigo = ""
    _categoria= ""
    _medida= ""
    _genero = ""
    _color = ""
    _uv = ""
    _tipoluna = ""
    _tipomaterial = ""
    _tipofiltro = ""
    _tipocontacto = ""
    # RECEPCION DE CATEGORIA
    _nombre = request.form['nombre-pro']
    _marca = request.form['marca-pro']
    _codigo = request.form['codigo-pro']
    # CONTROL DE categoria
    _categoria = request.form['option']
    if _categoria == '1': #moNTURA
        _uv = ""
        _genero = request.form['genero-pro']
        _color = request.form['color-pro']
        _calibre = request.form['calibre-pro']
        _puente = request.form['puente-pro']
        _ancho = request.form['ancho-pro']
        _medida = _calibre+"-"+_puente+"-"+_ancho
    if _categoria == '2': #luna
        _uv = request.form['uv-pro']
        _tipoluna = request.form['tipoluna'] 
        _tipomaterial = request.form['tipomaterial'] 
        if _tipomaterial == 'Organico':
            _tipofiltro = request.form['tipo-filtro-organico'] 
        if _tipomaterial == 'Vidrio':
            _tipofiltro = request.form['tipo-filtro-vidrio'] 
        if _tipomaterial == 'Policarbonato':
            _tipofiltro = request.form['tipo-filtro-policarbonato']                        
    if _categoria == '3': #lente de contacto
        _uv = ""
        _tipocontacto = request.form['tipocontacto'] 
        if _tipocontacto == 'Cosmetico':
            _color = request.form['tipocontacto-color']
    if _categoria == '4':
        _uv = ""                            

    # recepcion de datos        
    _stock = request.form['stock-pro']    
    _precio = request.form['precio-pro']
    _foto = request.files['imagen-pro']
    
 # recepcion de datos
    sql = "INSERT INTO `PRODUCTO` (`pro_cat_fk`, `pro_stock`, `pro_color`, `pro_material`, `pro_precio`, `pro_marca`, `pro_codigo`, `pro_proteccionuv`, `pro_genero`, `pro_nombre`, `pro_imagen`, `pro_tipoluna`, `pro_filtro`, `pro_lentecontacto`,`pro_medida`) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
    # los parametros segun el orden de datos
    datos = (_categoria,_stock,_color,_tipomaterial,_precio,_marca,_codigo,_uv,_genero,_nombre,_foto.filename,_tipoluna,_tipofiltro,_tipocontacto,_medida)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()  # Commit hace que la conexion se termine
    return render_template('inventario/index.html')


if __name__ == '__main__':  # para empezar la aplicacion
    app.run(debug=True)
