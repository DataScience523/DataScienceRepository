from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

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
  
  df['promedio'] = np.mean(df[['ocio', 'personal', 'dinero', 'trabajo', 'fisica', 'familiar', 'social', 'espiritual']])
  print(df)
  
  areas = ['ocio', 'personal', 'dinero', 'trabajo', 'fisica', 'familiar', 'social', 'espiritual']
  total = [ocio, personal, dinero, trabajo, fisica, familiar, social, espiritual]
  plt.bar(areas, total, color='cyan')
  plt.title(f'Balance de rueda de la vida de: {nombre}')
  plt.xlabel('Area')
  plt.ylabel('Altura')
  # Guardar la imagen en un archivo
  plt.savefig('static/uploads/balance.png')  # Guarda en la carpeta 'static'
  plt.close()  # Cierra la figura para liberar memoria
  
  print(df.dtypes)
  print(df.shape)  # (filas, columnas)

  # Crear la variable objetivo (estado general: 1 = Bien, 0 = Mal)
  df['estado_general'] = (df['promedio'] >= 6).astype(int)

  # Separar variables predictoras y objetivo
  X = df[['promedio']]
  y = df['estado_general']

  # Dividir en conjunto de entrenamiento y prueba
  X_train = pd.DataFrame({'promedio': np.random.randint(1, 11, size=50)})
  y_train = (X_train['promedio'] >= 6).astype(int)

  # Entrenar el modelo
  model = LogisticRegression()
  model.fit(X_train, y_train)

  # Hacer predicción con la única muestra real
  estado_predicho = model.predict(df[['promedio']])

  plt.figure(figsize=(6, 4))
  plt.bar(['Promedio'], [df['promedio'].values[0]], color='blue', alpha=0.7)
  plt.axhline(y=6, color='red', linestyle='--', label='Límite de Bienestar')
  plt.xlabel("Indicador")
  plt.ylabel("Valor")
  plt.ylim(0, 10)
  plt.title(f"Estado General: {'Bien' if estado_predicho == 1 else 'Mal'}")
  plt.legend()
  plt.savefig('static/uploads/regresion.png')  # Guarda en la carpeta 'static'
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