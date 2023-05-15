import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from config import config

#models
from models.ModelUser import ModelUser
from models.ModelHistorial import ModelHistorial
from models.ModelResultado import ModelResultado
from models.ModelPaciente import ModelPaciente
from models.ModelMedico import ModelMedico
from models.ModelAdministrador import ModelAdministrador



#entities
from models.entities.User import User
from models.entities.User import UserRegistro
from models.entities.Historial import Historial
from models.entities.Resultado import Resultado
from models.entities.Paciente import Paciente
from models.entities.Paciente import PacienteRegistro
from models.entities.Medico import Medico
from models.entities.Administrador import Administrador


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


                #TODOS ESTOS SON PARA  PACIENTE----------------------------------------------------------------------------------------------------------------------------
                #MANDO LLAMAR A MI QUERY, QUE ME DEVUELVE LOS DATOS DEL PACIENTE
                datosPaciente= ModelPaciente.obtener_info_Paciente_por_id(db, logged_user.idUsuario)
            
                #Importa la funcion obtener_id_historial_paciente de ModelHistorial
                idHistorial = ModelHistorial.obtener_id_historial_paciente(db, logged_user.idUsuario)
                historiales = []
                #PARA CADA ID DE HISTORIAL, OBTENEMOS LOS DATOS DEL HISTORIAL
                for id in idHistorial:
                    historial = ModelHistorial.obtener_historial_paciente(db, id[0])
                    historial_obj = Historial(historial[0], historial[1], historial[2]) # crea un objeto Historial
                    historiales.append(historial_obj)
                print(historiales)
                #Importa la funcion obtener_id_historial_paciente de ModelHistorial
                resultado = ModelResultado.getResults(db, logged_user.idUsuario)
                resultados = []
                #PARA CADA ID DE HISTORIAL, OBTENEMOS LOS DATOS DEL HISTORIAL
                for res in resultado:
                    resultado_obj = Resultado(res[0], res[1], res[2], res[3])
                    resultados.append(resultado_obj)
                print(resultados)
                #TERMIUNA PACIENTE----------------------------------------------------------------------------------------------------------------------------
                
                #TODOS ESTOS SON PARA  DOCTOR----------------------------------------------------------------------------------------------------------------------------
                datosMedico= ModelMedico.obtener_info_Medico_por_id(db, logged_user.idUsuario)

                #TERMINA DOCTOR----------------------------------------------------------------------------------------------------------------------------

                #TODOS ESTOS SON PARA  ADMINISTRADOR----------------------------------------------------------------------------------------------------------------------------
                datosAdmin= ModelAdministrador.obtener_info_Administrador_por_id(db, logged_user.idUsuario)
                #TERMINA ADMINISTRADOR----------------------------------------------------------------------------------------------------------------------------


                #agrega un if, para ver que tipo de usuario es, si es 1, es un paciente, si es 2, es un doctor, 3 es un administrador
                if logged_user.tipoUsuario == 1:

                    #los transformo en tipo diccionario, antes de almacenarlos en la sesion
                    paciente_dict = {
                    'idPaciente': datosPaciente[0],
                    'nombre': datosPaciente[1],
                    'apellidoPaterno': datosPaciente[2],
                    'apellidoMaterno': datosPaciente[3],
                    'fechaNacimiento': datosPaciente[4],
                    'sexo': datosPaciente[5],
                    'telefono': datosPaciente[6]
                    }
                    #almaceno los datos del paciente en la sesion
                    session['paciente'] = paciente_dict

                    #los transformo en tipo diccionario, antes de almacenarlos en la sesion
                    user_dict = {
                        'idUsuario': logged_user.idUsuario,
                        'tipoUsuario': logged_user.tipoUsuario,
                        'correoElectronico': logged_user.correoElectronico,
                        'contraseña': logged_user.contraseña,
                        }
                    session['user'] = user_dict

                    historiales_dict = [{'idHistorial': hist.idHistorial, 'numConsulta': hist.numConsulta, 'enfermedad': hist.enfermedad} for hist in historiales]
                    session['historiales'] = historiales_dict

                    resultados_dict = [{'numPaciente': res.numPaciente, 'idExamen': res.idExamen, 'fechaExamen': res.fechaExamen, 'resultadosExamen': res.resultadosExamen} for res in resultados]
                    session['resultados'] = resultados_dict

                    return redirect(url_for('home'))
                
                elif logged_user.tipoUsuario == 2:
                    #creacion del diccionario del usuario 
                    user_dict = {
                        'idUsuario': logged_user.idUsuario,
                        'tipoUsuario': logged_user.tipoUsuario,
                        'correoElectronico': logged_user.correoElectronico,
                        'contraseña': logged_user.contraseña,
                        }
                    #almacenamiento del diccionario en la sesion
                    session['user'] = user_dict

                    #creacion del diccionario del medico
                    medico_dict = {
                    'idMedico': datosMedico[0],
                    'nombre': datosMedico[1],
                    'apellidoPaterno': datosMedico[2],
                    'apellidoMaterno': datosMedico[3],
                    'fechaNacimiento': datosMedico[4],
                    'sexo': datosMedico[5],
                    'telefono': datosMedico[6],
                    }
                    #almacenamiento del diccionario en la sesion
                    session['medico'] = medico_dict

                    return redirect(url_for('homeDoctor'))
                    
                elif logged_user.tipoUsuario == 3:
                    
                    #creacion del diccionario del usuario
                    user_dict = {
                        'idUsuario': logged_user.idUsuario,
                        'tipoUsuario': logged_user.tipoUsuario,
                        'correoElectronico': logged_user.correoElectronico,
                        'contraseña': logged_user.contraseña,
                        }
                    session['user'] = user_dict

                    #creacion del diccionario del administrador
                    admin_dict = {
                    'idAdmin': datosAdmin[0],
                    'nombre': datosAdmin[1],
                    'apellidoPaterno': datosAdmin[2],
                    'apellidoMaterno': datosAdmin[3],
                    'fechaNacimiento': datosAdmin[4],
                    'sexo': datosAdmin[5],
                    'telefono': datosAdmin[6],
                    }
                    session['admin'] = admin_dict



                    return redirect(url_for('homeAdmi'))
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
    #los vuelvo a converitr en objetos cuando los recupero de la sesion
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    historiales_dict = session.get('historiales')
    historiales = [Historial(hist_dict['idHistorial'], hist_dict['numConsulta'], hist_dict['enfermedad']) for hist_dict in historiales_dict]

    resultados_dict = session.get('resultados')
    resultados = [Resultado(res_dict['numPaciente'], res_dict['idExamen'], res_dict['fechaExamen'], res_dict['resultadosExamen']) for res_dict in resultados_dict]

    paciente_dict = session.get('paciente')
    paciente = Paciente(paciente_dict['idPaciente'], paciente_dict['nombre'], paciente_dict['apellidoPaterno'], paciente_dict['apellidoMaterno'], paciente_dict['fechaNacimiento'], paciente_dict['sexo'], paciente_dict['telefono'])

    return render_template('home.html', user=user, historiales=historiales, resultados=resultados, paciente=paciente)


@app.route('/homeDoctor')
def homeDoctor():
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    medico_dict = session.get('medico')
    medico = Medico(medico_dict['idMedico'], medico_dict['nombre'], medico_dict['apellidoPaterno'], medico_dict['apellidoMaterno'], medico_dict['fechaNacimiento'], medico_dict['sexo'], medico_dict['telefono'])
    
    return render_template('homeDoctor.html', user=user, medico=medico)

@app.route('/homeAdmi')
def homeAdmi():
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    admin_dict = session.get('admin')
    admin = Administrador(admin_dict['idAdmin'], admin_dict['nombre'], admin_dict['apellidoPaterno'], admin_dict['apellidoMaterno'], admin_dict['fechaNacimiento'], admin_dict['sexo'], admin_dict['telefono'])
    return render_template('homeAdmi.html', user=user, admin=admin)


@app.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    #esto me sirve para cargar la configuracion de desarrollo
    app.config.from_object(config['development'])
    app.run(debug=True, port=8000)