from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/Persona')
def about():
    return render_template('Persona.html')

if __name__ == '__main__':
    app.run(debug=True)
