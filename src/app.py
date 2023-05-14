import json
from flask import Flask, render_template, request, redirect, url_for, flash, sessions
from flask_mysqldb import MySQL
from config import config

#models
from models.ModelUser import ModelUser
from models.ModelHistorial import ModelHistorial
from models.ModelResultado import ModelResultado
from models.ModelPaciente import ModelPaciente



#entities
from models.entities.User import User
from models.entities.User import UserRegistro
from models.entities.Historial import Historial
from models.entities.Resultado import Resultado
from models.entities.Paciente import Paciente
from models.entities.Paciente import PacienteRegistro


app = Flask(__name__)

db=MySQL(app)


@app.route('/')
def index():
    #cuando se hace una entrada normal, te lleva a la pagina principal
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template('auth/registro.html')

@app.route('/registroUsuario', methods=['GET', 'POST'])
def registroUsuario():
    if request.method == 'POST':
        # Crear objeto UserRegistro y PacienteRegistro
        user = UserRegistro(
            1, 
            request.form['correo'],
            UserRegistro.hash_password(request.form['contraseña']),
            )
        print(UserRegistro)
        print(UserRegistro.hash_password(request.form['contraseña']))
        paciente = PacienteRegistro(
            None,
            request.form['nombre'],
            request.form['apellidoPaterno'],
            request.form['apellidoMaterno'],
            request.form['fechaNacimiento'],
            request.form['sexo'],
            request.form['telefono'],
            )
        print(paciente.idUsuario)
        # Registrar usuario y paciente
        try:
            ModelUser.register(db, user)
            ModelPaciente.register(db, user, paciente)
            flash("Usuario y paciente registrados")
            return render_template('auth/login.html')
        except Exception as ex:
            flash("Error al registrar usuario y paciente: " + str(ex))
            return render_template('auth/registro.html')
    else:
        return render_template('auth/registro.html')

    
#copia del main------------------------------------------------------------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    #pero cuando se hace una peticion post, te lleva a la pagina de login, pero toma los datos del formulario
    if request.method == 'POST':
        #print(request.form['correo'])
        #print(request.form['contraseña'])

        user=User(0,0,request.form['correo'],(request.form['contraseña']))
        logged_user=ModelUser.login(db,user)
        if logged_user != None:
            
            if logged_user.contraseña == True:
                #print('si soy yo')
                #print(logged_user.tipoUsuario)

                datosPaciente= ModelPaciente.obtener_info_Paciente_por_id(db, logged_user.idUsuario)
                #print(datosPaciente)
               
            
                # importa la funcion obtener_id_historial_paciente de ModelHistorial
                idHistorial = ModelHistorial.obtener_id_historial_paciente(db, logged_user.idUsuario)
                historiales = []
                for id in idHistorial:
                    historial = ModelHistorial.obtener_historial_paciente(db, id[0])
                    historial_obj = Historial(historial[0], historial[1], historial[2]) # crea un objeto Historial
                    historiales.append(historial_obj)
                print(historiales)

                resultado = ModelResultado.getResults(db, logged_user.idUsuario)
                resultados = []
                for res in resultado:
                    resultado_obj = Resultado(res[0], res[1], res[2], res[3])
                    resultados.append(resultado_obj)
                print(resultados)


                #agrega un if, para ver que tipo de usuario es, si es 1, es un paciente, si es 2, es un doctor, 3 es un administrador
                if logged_user.tipoUsuario == 1:

                    #print(logged_user.correoElectronico)
                    #print("soy del tipo 1")
                    return redirect(url_for('home', user=logged_user, historiales=historiales, resultados=resultados))
                
                elif logged_user.tipoUsuario == 2:
                    return render_template('homeDoctor.html',user=logged_user)
                elif logged_user.tipoUsuario == 3:
                    return render_template('homeAdmi.html',user=logged_user)
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
    

#---------------------------------------------------------------------------------------------------------------------------------------------
    

#AUN SIN PROBAR ESTA FUNCION DE REQU
@app.route('/home')
def home():
    user = request.args.get('user')
    historiales = request.args.get('historiales')
    resultados = request.args.get('resultados')
    print("resultados: ", resultados)
    return render_template('home.html', user=user, historiales=historiales, resultados=resultados)


@app.route('/homeDoctor')
def homeDoctor():
    return render_template('homeDoctor.html')

@app.route('/homeAdmi')
def homeAdmi():
    return render_template('homeAdmi.html')


@app.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    #esto me sirve para cargar la configuracion de desarrollo
    app.config.from_object(config['development'])
    app.run(debug=True, port=8000)