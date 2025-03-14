from flask import Flask, redirect, render_template, request, url_for
import csv

app = Flask(__name__)

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

  # Procesar los datos (por ejemplo, guardarlos en una base de datos)
  # Aquí simplemente los imprimimos por el momento
  print(f'Nombre: {nombre}')

  totalMavIa = [nombre, apellido, ocio, personal, dinero, trabajo, fisica, familiar, social, espiritual]

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
    encabezado, datos = leer_csv()
    return render_template('mostDatosIng.html', encabezado=encabezado, datos=datos)

if __name__ == '__main__':
    app.run(debug=True)
