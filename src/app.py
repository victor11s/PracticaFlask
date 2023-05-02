from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import config

#models
from models.ModelUser import ModelUser



#entities
from models.entities.User import User
from models.entities.User import UserRegistro

app = Flask(__name__)

db=MySQL(app)


@app.route('/')
def index():
    #cuando se hace una entrada normal, te lleva a la pagina principal
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('auth/registro.html')

def registroUsuario():
    if request.method == 'POST':
        user=UserRegistro(request.form['nombre'],request.form['apellidoPaterno'],request.form['apellidoMaterno'],request.form['sexo'],request.form['telefono'],request.form['correo'],request.form['contraseña'])
        #si el registro es exitoso, te lleva a la pagina de login y le das un flash de usuario registrado, si no solo dar flash de que no se pudo registrar
        if ModelUser.register(db,user):
            flash("Usuario registrado")
            return render_template('auth/login.html')
        else:
            flash("No se pudo registrar")
            return render_template('auth/registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    #pero cuando se hace una peticion post, te lleva a la pagina de login, pero toma los datos del formulario
    if request.method == 'POST':
        #print(request.form['correo'])
        #print(request.form['contraseña'])

        user=User(0,request.form['correo'],request.form['contraseña'],0)
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            
            if logged_user.contraseña == True:
                print(logged_user.tipoUsuario)
                #agrega un if, para ver que tipo de usuario es, si es 1, es un paciente, si es 2, es un doctor, 3 es un administrador
                if logged_user.tipoUsuario == 1:
                    return render_template('home.html')
                elif logged_user.tipoUsuario == 2:
                    return render_template('homeDoctor.html')
                elif logged_user.tipoUsuario == 3:
                    return render_template('homeAdmi.html')
                else:
                    flash("No se encontro el tipo de usuario")
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

@app.route('/homeDoctor')
def homeDoctor():
    return render_template('homeDoctor.html')

@app.route('/homeAdmi')
def homeAdmi():
    return render_template('homeAdmi.html')

if __name__ == '__main__':
    #esto me sirve para cargar la configuracion de desarrollo
    app.config.from_object(config['development'])
    app.run(debug=True, port=8000)