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

    # TODO: CONEXION BD y QUERIES
    #sql="consulta, insercion eliminacion, visualizacion, sintaxis mysql"
    sql = "INSERT INTO `Optica`.`CLIENTE` (`cli_nombre`, `cli_apellido1`, `cli_apellido2`, `cli_correo`, `cli_dni_o_ruc`, `cli_fechanac`, `cli_genero`, `cli_telefono`, `cli_direccion`) VALUES ('Alexander', 'Tarqui', 'Rondon', 'alextr.t1@hotmail.com', '70848524', '2006-06-16', 'Masculino', '938290325', 'Alto Alianza');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()  # Commit hace que la conexion se termine
    # TODO: CONEXION BD y QUERIES
    # luego de la insercion nos dirige a la siguiente pagina
    return render_template('inventario/index.html')

# si clonaste esto es porque ya aprendiste a actulizar desde la master


if __name__ == '__main__':  # para empezar la aplicacion
    app.run(debug=True)
