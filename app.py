from re import template
from flask import Flask, url_for, redirect
# Referencia a herramientas y librerias
from flask import render_template, request
from  datetime import datetime
from flaskext.mysql import MySQL  # Base del modulo de Mysql
from datetime import date #para la hora :v
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
    _forma = ""
    _nombre = ""
    _marca = ""
    _codigo = ""
    # RECEPCION DE CATEGORIA
    _nombre = request.form['nombre-pro']
    _codigo = request.form['codigo-pro']
    
    # CONTROL DE categoria
    _categoria = request.form['option']
    if _categoria == '1': #moNTURA
        _marca = request.form['marca-pro-montura']
        _uv = ""
        _genero = request.form['genero-pro']
        _color = request.form['color-pro']
        _calibre = request.form['calibre-pro']
        _puente = request.form['puente-pro']
        _ancho = request.form['ancho-pro']
        _forma = request.form['forma-montura']
        _medida = _calibre+"-"+_puente+"-"+_ancho #medida cuando sea una montura
    if _categoria == '2': #luna
        _marca = request.form['marca-pro-luna']
        _tipoluna = request.form['tipoluna'] 
        _tipomaterial = request.form['tipomaterial'] 
        if _tipomaterial == 'Organico':
            _tipofiltro = request.form['tipo-filtro-organico'] 
        if _tipomaterial == 'Vidrio':
            _tipofiltro = request.form['tipo-filtro-vidrio'] 
        if _tipomaterial == 'Policarbonato':
            _tipofiltro = request.form['tipo-filtro-policarbonato']                        
    if _categoria == '3': #lente de contacto
        _marca = request.form['marca-pro-lentecontacto']
        _uv = ""
        _tipocontacto = request.form['tipocontacto'] 
        if _tipocontacto == 'Cosmetico':
            _color = request.form['tipocontacto-color']
        if _tipocontacto == 'Miopia':
            _medida = request.form['medida-contacto'] #medida cuando sea un lente de contacto
    if _categoria == '4':
        _uv = ""                            

    
    # recepcion de datos        
    _stock = request.form['stock-pro']    
    _precio = request.form['precio-pro']
    _foto = request.files['imagen-pro']
    now=datetime.now()
    tiempo=now.strftime("%Y%Y%M%S")
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
    
    
 # recepcion de datos
    sql = "INSERT INTO `PRODUCTO` (`pro_cat_fk`, `pro_stock`, `pro_color`, `pro_material`, `pro_precio`, `pro_marca`, `pro_codigo`, `pro_proteccionuv`, `pro_genero`, `pro_nombre`, `pro_imagen`, `pro_tipoluna`, `pro_filtro`, `pro_lentecontacto`,`pro_medida`,`pro_forma`) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s)"
    # los parametros segun el orden de datos
    datos = (_categoria,_stock,_color,_tipomaterial,_precio,_marca,_codigo,_uv,_genero,_nombre,_foto.filename,_tipoluna,_tipofiltro,_tipocontacto,_medida,_forma)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)

    sql = "INSERT INTO `Optica`.`KARDEX` (\
        `kar_det_fk`,\
        `kar_movimiento`,\
        `kar_det_pro_fk`,\
        `kar_cantidad`,\
        `kar_entra`,\
        `kar_sale`,\
        `kar_total`,\
        `kar_queda`,\
        `kar_cop_fk`,\
        `kar_cop_pro_fk`,\
        `kar_fecha`) \
        VALUES (NULL,%s,NULL,%s,%s,%s,%s,%s,NULL,NULL,%s)"
#! INSERCION AL KARDEX
    _kar_det_fk=""
    _kar_movimiento=1
    _kar_det_pro_fk=""  
    _kar_cantidad=_stock
    _kar_entra=_stock
    _kar_sale=""
    _kar_total=_stock
    _kar_queda=""
    _kar_cop_fk=""
    _kar_cop_pro_fk=""
    _kar_fecha=date.today()
    datos = (_kar_movimiento,_kar_cantidad,_kar_entra,_kar_sale,_kar_total,_kar_queda,_kar_fecha)
    cursor.execute(sql, datos)
        #*el valor kar_queda se utilizara cuando se hagan las ventas
    conn.commit()  # commit hace que la conexion se termine
    return render_template('inventario/index.html')


if __name__ == '__main__':  # para empezar la aplicacion
    app.run(debug=True)
