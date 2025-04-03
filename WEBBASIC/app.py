from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import csv
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
  ocio = (int)(request.form['social'])
  personal = (int)(request.form['espiritual'])
  dinero = (int)(request.form['exito'])
  trabajo = (int)(request.form['familia'])
  fisica = (int)(request.form['profesion'])
  familiar = (int)(request.form['fisico'])
  social = (int)(request.form['financiero'])
  espiritual = (int)(request.form['crecimiento'])

  # Procesar los datos (por ejemplo, guardarlos en una base de datos)
  # Aquí simplemente los imprimimos por el momento
  print(f'Nombre: {nombre}')

  totalMavIa = [nombre, apellido, ocio, personal, dinero, trabajo, fisica, familiar, social, espiritual]
  Promedio = {
    'ocio': [ocio], 
    'personal': [personal], 
    'dinero': [dinero], 
    'trabajo': [trabajo],
    'fisica': [fisica],
    'familiar': [familiar],
    'social': [social],
    'espiritual': [espiritual]
  }
  df = pd.DataFrame(Promedio)
  
  Total_mean = np.mean(df[['ocio', 'personal', 'dinero', 'trabajo', 'fisica', 'familiar', 'social', 'espiritual']])
  print(Total_mean)
  
  areas = ['ocio', 'personal', 'dinero', 'trabajo', 'fisica', 'familiar', 'social', 'espiritual']
  total = [ocio, personal, dinero, trabajo, fisica, familiar, social, espiritual]
  plt.bar(areas, total, color='cyan')
  plt.title(f'Balance de rueda de la vida de: {nombre}')
  plt.xlabel('Area')
  plt.ylabel('Altura')
  # Guardar la imagen en un archivo
  plt.savefig('static/uploads/balance.png')  # Guarda en la carpeta 'static'
  plt.close()  # Cierra la figura para liberar memoria
  
      # Guardar los datos en la base de datos MySQL
  cur = mysql.connection.cursor()
  cur.execute("""
    INSERT INTO formulario (nombre, apellido, social, espiritual, exito, familia, profesion, fisico, financiero, crecimiento) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nombre, apellido, ocio, personal, dinero, trabajo, fisica, familiar, social, espiritual))
  mysql.connection.commit()
  cur.close()
  
  with open("datos.csv", "a+", newline ='') as csvfile:
    wr = csv.writer(csvfile, dialect='excel', delimiter=',')
    wr.writerow(totalMavIa)
  
  return redirect(url_for('mostDatosIng'))
            
def leer_csv():
    datos = []
    with open('datos.csv', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        encabezado = next(lector)  # Leer la primera fila como encabezado
        for fila in lector:
            datos.append(fila)
    return encabezado, datos

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