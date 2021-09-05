from re import template
from flask import Flask, url_for, redirect
# Referencia a herramientas y librerias
from flask import render_template, request, jsonify
from flask_mysqldb import MySQL,MySQLdb
from datetime import datetime
from flaskext.mysql import MySQL  # Base del modulo de Mysql
from datetime import date #para la hora :v

#* declaracion de funciones
def insertarSql(sql,datos):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sql, datos)    
        conn.commit()
    except OSError:
        raise RuntimeError from None

def consultarSql(sql):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    registros=cursor.fetchall()    
    conn.commit()
    return registros



#* funciones




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
    return render_template('/index.html')


# si clonaste esto es porque ya aprendiste a actulizar desde la master
@app.route('/crear_venta')
def crearventa():
    return render_template('venta/crear_venta.html')

@app.route("/insertar_paciente")
def insertar_paciente():
    return render_template('paciente/paciente.html')


@app.route('/almacenar_paciente', methods=['POST'])
def almacenarpaciente():
    _nombre = ""
    _apellido1 = ""
    _apellido2 = ""
    _dnioruc = ""
    _correo = ""
    _telefono = ""
    _fechanac = ""
    _genero = ""
    _direccion = ""
    # RECEPCION DE CATEGORIA
    _nombre = request.form['nombre-pac']
    _apellido = request.form['apellido-pac']
    _dnioruc = request.form['dni_o_ruc-pac']
    _correo = request.form['correo-pac']
    _fechanac = request.form['fechanac-pac']
    _genero = request.form['genero-pac']
    _telefono = request.form['telefono-pac']
    _direccion = request.form['direccion-pac']
                       
    #!revisar luego el apellido OPTICA    
    


    
 # recepcion de datos
    sql = "INSERT INTO `CLIENTE` (`cli_id`, `cli_nombre`, `cli_apellido1`, `cli_apellido2`, `cli_correo`, `cli_dni_o_ruc`, `cli_fechanac`, `cli_genero`, `cli_telefono`, `cli_direccion`) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # los parametros segun el orden de datos
    datos = (_nombre,_apellido,_apellido2,_correo,_dnioruc,_fechanac,_genero,_telefono,_direccion)
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.execute(sql, datos)
    insertarSql(sql,datos)

    return render_template('paciente/paciente.html')
#*Ver registro de paciente
@app.route("/registro_paciente")
def lista_pacientes():
    sql = "SELECT * FROM `CLIENTE`"
    # los parametros segun el orden de datos
    
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.execute(sql, datos)
    resultados=consultarSql(sql)
    return render_template('paciente/paciente_registro.html', resultados=resultados)
#*Eliminar paciente
@app.route('/destruir_paciente/<int:id>')#recibimos un parametro el id
def destroy_paciente(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM CLIENTE WHERE cli_id=%s",(id))
    conn.commit()
    return redirect('/registro_paciente')

#*editar paciente
@app.route("/editar_paciente/<int:id>")
def edit_paciente(id):  
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM CLIENTE WHERE cli_id=%s",(id))
    registros=cursor.fetchall()
    conn.commit()
    return render_template('paciente/paciente_editar.html',registros=registros)

#*actualizar

@app.route("/actualizar_paciente", methods=['POST'])
def actualizar_paciente():
    
    _nombre = request.form['nombre-pac']
    _apellido = request.form['apellido-pac']
    _dnioruc = request.form['dni_o_ruc-pac']
    _correo = request.form['correo-pac']
    _fechanac = request.form['fechanac-pac']
    #_genero = request.form['genero-pac']
    _telefono = request.form['telefono-pac']
    _direccion = request.form['direccion-pac']
    id = request.form['idtxt']
                       
    #!revisar luego el apellido OPTICA 
 # recepcion de datos
    sql = "UPDATE `CLIENTE` SET `cli_nombre`=%s, `cli_apellido1`=%s, `cli_correo`=%s, `cli_dni_o_ruc`=%s, `cli_fechanac`=%s, `cli_telefono`=%s, `cli_direccion`=%s WHERE cli_id=%s;"
    # los parametros segun el orden de datos
    datos = (_nombre,_apellido,_correo,_dnioruc,_fechanac,_telefono,_direccion,id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit() 

    return redirect('/registro_paciente')



#*Ver historial de pacientes
@app.route("/historial_paciente")
def histo_pacientes():
    sql = "SELECT b.his_id,CONCAT(a.cli_nombre,' ',a.cli_apellido1),b.his_ojoizq,b.his_ojoder,b.his_distanciainter,b.his_adicion,b.his_observacion, date_format(b.his_fecha, '%d-%m-%Y') as fecha FROM CLIENTE a INNER JOIN HISTORIAL_OFT b on a.cli_id=b.his_cli_fk;"
    # los parametros segun el orden de datos
    
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.execute(sql, datos)
    resultados=consultarSql(sql)
    return render_template('paciente/paciente_historial.html', resultados=resultados)


@app.route("/insertar_historial/<int:id>")
def insertar_historial(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT cli_id FROM CLIENTE WHERE cli_id=%s",(id))
    registros=cursor.fetchall()
    conn.commit()
    return render_template('paciente/paciente_historialnuevo.html', registros=registros)

@app.route("/almacenar_historial", methods=['POST', 'GET'])
def almacenarhistorial():
   
    ojoder = ""
    distanciainter = ""
    adicion = ""
    observacion = ""
    avl = ""
    id=""
    # RECEPCION DE CATEGORIA
    ojoizq = request.form['ojoizq-his']
    ojoder = request.form['ojoder-his']
    distanciainter = request.form['dpi-his']
    adicion = request.form['adicion-his']
    observacion = request.form['observacion-his']
    avl = request.form['observacion-his']
    id = request.form['id']

 # recepcion de datos
    sql = "INSERT INTO `HISTORIAL_OFT` (`his_id`, `his_ojoizq`, `his_ojoder`, `his_distanciainter`, `his_adicion`, `his_observacion`, `his_cli_fk`, `his_fecha`, `his_avl`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);"
    # los parametros segun el orden de datos
    datos = (ojoizq,ojoder,distanciainter,adicion,observacion,id,date.today(),avl)
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.execute(sql, datos)
    insertarSql(sql,datos)

    return redirect('/registro_paciente')


#*Eliminar historial
@app.route('/destruir_historial/<int:id>')#recibimos un parametro el id
def destroy_historial(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM HISTORIAL_OFT WHERE his_id=%s",(id))
    conn.commit()
    return redirect('/registro_paciente')

#*editar historial
@app.route("/editar_historial/<int:id>")
def edit_historial(id):  
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM HISTORIAL_OFT WHERE his_id=%s",(id))
    registros=cursor.fetchall()
    conn.commit()
    return render_template('paciente/paciente_editar.html',registros=registros)

#*actualizar

@app.route("/actualizar_historial", methods=['POST'])
def actualizar_historial():
    
    _nombre = request.form['nombre-pac']
    _apellido = request.form['apellido-pac']
    _dnioruc = request.form['dni_o_ruc-pac']
    _correo = request.form['correo-pac']
    _fechanac = request.form['fechanac-pac']
    #_genero = request.form['genero-pac']
    _telefono = request.form['telefono-pac']
    _direccion = request.form['direccion-pac']
    id = request.form['idtxt']
                       
    #!revisar luego el apellido OPTICA 
 # recepcion de datos
    sql = "UPDATE `CLIENTE` SET `cli_nombre`=%s, `cli_apellido1`=%s, `cli_correo`=%s, `cli_dni_o_ruc`=%s, `cli_fechanac`=%s, `cli_telefono`=%s, `cli_direccion`=%s WHERE cli_id=%s;"
    # los parametros segun el orden de datos
    datos = (_nombre,_apellido,_correo,_dnioruc,_fechanac,_telefono,_direccion,id)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit() 

    return redirect('/registro_paciente')

# *PRODUCTOS
@app.route('/insertar_producto')
def insertar_producto():
    return render_template('inventario/insertar_producto.html')

# *PRODUCTOS
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
    # conn = mysql.connect()
    # cursor = conn.cursor()
    # cursor.execute(sql, datos)
    insertarSql(sql,datos)
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
    insertarSql(sql,datos)
    # cursor.execute(sql, datos)
        #*el valor kar_queda se utilizara cuando se hagan las ventas
    # conn.commit()  # commit hace que la conexion se termine
    return render_template('index.html')
#* PRODUCTOS

#* CLIENTE



@app.route('/proveedor')
def visualizarP():
    sql="SELECT * FROM `PROVEEDOR`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)

    proveedores=cursor.fetchall()
    #print(proveedores)

    conn.commit()
    return render_template('proveedor/proveedor.html', proveedores=proveedores)

@app.route('/proveedor', methods=['POST'])
def registrarProveedor():

    _nombreP=request.form['nombre']
    _telefonoP=request.form['numero']
    _correoP=request.form['email']
    #_direccionP=request.form['']
    #_dnirucP=request.form['']
    _empresaP=request.form['empre']

    sql="INSERT INTO proveedor (prov_id, prov_nombre, prov_telefono, prov_correo, prov_direccion, prov_dni_o_ruc, prov_empresa) VALUES (NULL, %s, %s, %s, NULL, NULL, %s);"

    datos=(_nombreP, _telefonoP, _correoP,_empresaP) #_direccionP, _dnirucP, 

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, datos)
    conn.commit() 
    return redirect('/proveedor')

@app.route('/borrarP/<int:id>')
def borrarP(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM proveedor WHERE prov_id = %s",(id))
    conn.commit()
    return redirect('/proveedor')

@app.route('/actualizarP', methods=['POST'])
def actualizarP():

    _nombreP=request.form['nombre']
    _telefonoP=request.form['numero']
    _correoP=request.form['email']
    #_direccionP=request.form['']
    #_dnirucP=request.form['']
    _empresaP=request.form['empre']

    _id=request.form['txtid']

    sql="UPDATE proveedor SET prov_nombre = %s, prov_telefono = %s, prov_correo = %s, prov_empresa = %s  WHERE proveedor.prov_id = %s ;" #prov_direccion = NULL, prov_dni_o_ruc = NULL

    datos=(_nombreP, _telefonoP, _correoP,_empresaP,_id) #_direccionP, _dnirucP, 

    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql, datos)
    conn.commit() 

    return redirect('/proveedor')

@app.route('/editarP/<int:id>')
def editarP(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM proveedor WHERE prov_id = %s",(id))
    
    proveedores=cursor.fetchall()
    conn.commit()
    print(proveedores)

    return render_template('proveedor/proveedor_edit.html',proveedores=proveedores)

@app.route("/visualizar_productoss")
def visualizarProducto():
    sql= "SELECT pro_id,pro_imagen,pro_nombre,pro_material,pro_precio FROM `PRODUCTO` "
    productos=consultarSql(sql)
    return render_template('inventario/visualizar_productoss.html')

# VENTA
@app.route("/crear_venta")
def crear_venta():
    sql = "SELECT v.ven_id,v.ven_fecha,pro.pro_nombre,c.cli_nombre,dp.det_cantidad,pro.pro_precio,v.ven_montototal FROM `VENTA` v inner join `PEDIDO` p ON v.ven_id=p.ped_ven_fk INNER JOIN `CLIENTE` c ON c.cli_id=p.ped_cli_fk INNER JOIN `DETALLE_PEDIDO` dp ON p.ped_id=dp.det_ped_fk INNER JOIN `PRODUCTO` pro ON pro.pro_id=dp.det_pro_fk"
    ventas=consultarSql(sql)
    sql2= "SELECT cli_nombre FROM `cliente` "
    clientes=consultarSql(sql2)
    sql3= "SELECT pro_nombre FROM `producto` "
    productos=consultarSql(sql3)
    return render_template('venta/crear_venta.html',ventas=ventas,clientes=clientes, productos=productos)
    

@app.route('/guardar_venta', methods=['POST'])
def guardar():
    _cliente=request.form['cliente_select']
    _producto=request.form['producto_select']
    _cantidad=request.form['formcantidad']
    sql = "INSERT into `venta`(ven_id, ven_emp_fk) values(%s,%s)"
    datos=(8,1)
    insertarSql(sql,datos)
    sql = "INSERT into `pedido`(ped_cli_fk,ped_ven_fk) values((select cli_id from `cliente` where cli_nombre=%s), %s)"
    datos=(_cliente,8)
    insertarSql(sql,datos)
    sql = "INSERT into `detalle_pedido`(`det_pro_fk`, `det_cantidad`,`det_ped_fk`) values((select pro_id from `producto` where pro_nombre=%s), %s,%s)"
    datos=(_producto, _cantidad,8)
    insertarSql(sql,datos)
    return render_template('venta/crear_venta.html')

@app.route('/destruir_venta/<int:id>')#recibimos un parametro el id
def destroy_venta(id):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM venta WHERE ven_id=%s",(id))
    conn.commit()
    return redirect('/crear_venta')

    
if __name__ == '__main__':  # para empezar la aplicacion
    app.run(debug=True)



