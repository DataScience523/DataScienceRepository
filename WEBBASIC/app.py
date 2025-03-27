from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import csv

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root' 
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'proyectodatascience' 

# Inicializar MySQL
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Persona')
def Persona():
    return render_template('Persona.html')

@app.route('/enviar', methods=['POST'])
def enviar_datos():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    ocio = request.form['social']
    personal = request.form['espiritual']
    dinero = request.form['exito']
    trabajo = request.form['familia']
    fisica = request.form['profesion']
    familiar = request.form['fisico']
    social = request.form['financiero']
    espiritual = request.form['crecimiento']

    # Guardar los datos en la base de datos MySQL
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO formulario (nombre, apellido, social, espiritual, exito, familia, profesion, fisico, financiero, crecimiento) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nombre, apellido, ocio, personal, dinero, trabajo, fisica, familiar, social, espiritual))
    mysql.connection.commit()
    cur.close()

    # Guardar los datos en un archivo CSV
    with open("datos.csv", "a+", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Si el archivo está vacío, escribir el encabezado
        if csvfile.tell() == 0:
            writer.writerow(["nombre", "apellido", "social", "espirituall", "exito", "familia", "profesion", "fisico", "financiero", "crecimiento"])
        
        # Escribir la fila de datos
        writer.writerow([nombre, apellido, ocio, personal, dinero, trabajo, fisica, familiar, social, espiritual])

    return redirect(url_for('mostDatosIng'))

@app.route('/mostDatosIng')
def mostDatosIng():
    # Consultar los datos de la base de datos
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM formulario")
    datos = cur.fetchall()  # Obtener todos los registros
    cur.close()
    
    return render_template('mostDatosIng.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)