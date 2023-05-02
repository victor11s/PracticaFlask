from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config

#models
from models.ModelUser import ModelUser


#entities
from models.entities.User import User

app = Flask(__name__)

db=MySQL(app)


@app.route('/')
def index():
    #cuando se hace una entrada normal, te lleva a la pagina principal
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    #pero cuando se hace una peticion post, te lleva a la pagina de login, pero toma los datos del formulario
    if request.method == 'POST':
        #print(request.form['correo'])
        #print(request.form['contraseña'])

        user=User(0,request.form['correo'],request.form['contraseña'])
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            
            if logged_user.contraseña == True:
                flash("Bienvenido {}".format(logged_user.correoElectronico))
                return render_template('home.html')
            else:   
                
                flash("Contraseña incorrecta")
                return render_template('auth/login.html')

        else:
            
            flash("El usuario no existe")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
    
@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    #esto me sirve para cargar la configuracion de desarrollo
    app.config.from_object(config['development'])
    app.run(debug=True, port=8000)