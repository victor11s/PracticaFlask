from flask import Flask, render_template, request, redirect, url_for
from config import config
app = Flask(__name__)

@app.route('/')
def index():
    #cuando se hace una entrada normal, te lleva a la pagina principal
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    #pero cuando se hace una peticion post, te lleva a la pagina de login, pero toma los datos del formulario
    if request.method == 'POST':
        print(request.form['correo'])
        print(request.form['contraseña'])
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

if __name__ == '__main__':
    #esto me sirve para cargar la configuracion de desarrollo
    app.config.from_object(config['development'])
    app.run(debug=True, port=8000)