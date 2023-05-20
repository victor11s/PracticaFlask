
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL


#models
from models.ModelUser import ModelUser
from models.ModelHistorial import ModelHistorial
from models.ModelResultado import ModelResultado
from models.ModelPaciente import ModelPaciente
from models.ModelMedico import ModelMedico
from models.ModelAdministrador import ModelAdministrador
from models.ModelCita import ModelCita


#entities
from models.entities.User import User
from models.entities.User import UserRegistro
from models.entities.Historial import Historial
from models.entities.Resultado import Resultado
from models.entities.Paciente import Paciente
from models.entities.Paciente import PacienteRegistro
from models.entities.Medico import Medico
from models.entities.Administrador import Administrador
from models.entities.Cita import Cita
from models.entities.Cita import CitaReservar
from models.entities.Cita import CitaMedico
from models.entities.Paciente import PacienteCita


class Config:
    SECRET_KEY = '4335'


# Iniciar el servidor en modo de depuración
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'mediapp2.ctoyvdu4lxpi.us-east-2.rds.amazonaws.com'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = 'Cx5mlp4335'
    MYSQL_DB = 'mediapp2'

app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
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
        user = UserRegistro(0,
            1, 
            request.form['correo'],
            UserRegistro.hash_password(request.form['contraseña']),
            )
        print(UserRegistro)
        print(UserRegistro.hash_password(request.form['contraseña']))
        paciente = PacienteRegistro(
            0,
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
            idUsuario = ModelUser.register(db, user, paciente)
            # idUsuario ahora contiene el ID del usuario recién creado.
            
            flash("Usuario y paciente registrados", "success")
            return render_template('auth/login.html')
        except Exception as ex:
            flash("Error al registrar usuario y paciente: " + str(ex), "danger")
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

                # datosMedicos= ModelMedico.obtener_info_Medicos(db)
                # medicos=[]
                # for medico in datosMedicos:
                #     medico_obj = Medico(medico[0], medico[1], medico[2], medico[3], medico[4], medico[5], medico[6])
                #     medicos.append(medico_obj)
                # print(medicos)


                # datosPaciente= ModelPaciente.obtener_info_Pacientes(db)
                # pacientes=[]
                # for paciente in datosPaciente:
                #     paciente_obj = Paciente(paciente[0], paciente[1], paciente[2], paciente[3], paciente[4], paciente[5], paciente[6], paciente[7])
                #     pacientes.append(paciente_obj)
                # print(pacientes)


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



                    return redirect(url_for('homeAdmi' ))
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

@app.route('/citasPaciente')
def citasPaciente():
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    paciente_dict = session.get('paciente')
    paciente = Paciente(paciente_dict['idPaciente'], paciente_dict['nombre'], paciente_dict['apellidoPaterno'], paciente_dict['apellidoMaterno'], paciente_dict['fechaNacimiento'], paciente_dict['sexo'], paciente_dict['telefono'])

    citas = ModelPaciente.obtenerCitas(db, session['user']['idUsuario'])
    print(citas)
    citas_obj=[]
    for cita in citas:
        cita_obj= PacienteCita(cita[0],cita[1],cita[2],cita[3],cita[4],cita[5],cita[6])
        print(cita_obj)
        citas_obj.append(cita_obj)

    print(citas_obj)

    return render_template('citasPaciente.html', user=user, citas=citas_obj, paciente=paciente)

@app.route('/homeDoctor')
def homeDoctor():
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    medico_dict = session.get('medico')
    medico = Medico(medico_dict['idMedico'], medico_dict['nombre'], medico_dict['apellidoPaterno'], medico_dict['apellidoMaterno'], medico_dict['fechaNacimiento'], medico_dict['sexo'], medico_dict['telefono'])

    citas = ModelCita.obtenerCitasPorDoctor(db, session['user']['idUsuario'])
    citas_obj=[]
    for cita in citas:
        cita_obj= CitaMedico(cita[0],cita[1],cita[2],cita[3],cita[4], cita[5], cita[6], cita[7],cita[8])
        citas_obj.append(cita_obj)
    print (citas_obj)

    
    return render_template('homeDoctor.html', user=user, medico=medico, citas=citas_obj)

@app.route('/homeAdmi')
def homeAdmi():
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    admin_dict = session.get('admin')
    admin = Administrador(admin_dict['idAdmin'], admin_dict['nombre'], admin_dict['apellidoPaterno'], admin_dict['apellidoMaterno'], admin_dict['fechaNacimiento'], admin_dict['sexo'], admin_dict['telefono'])
    
    datosMedicos = ModelAdministrador.obtener_todos_medicos(db)
    medicos = []
    for medico in datosMedicos:
        medico_obj = Medico(medico[0], medico[1], medico[2], medico[3], medico[4], medico[5], medico[6])
        medicos.append(medico_obj)

    datosPaciente = ModelAdministrador.obtener_todos_pacientes(db)
    pacientes = []
    for paciente in datosPaciente:
        paciente_obj = Paciente(paciente[0], paciente[1], paciente[2], paciente[3], paciente[4], paciente[5], paciente[6])
        pacientes.append(paciente_obj)

    return render_template('homeAdmi.html', user=user, admin=admin,medicos=medicos, pacientes=pacientes)




#----Agendar Citas------------------------------------------------------------------------------------------------------------------------------
@app.route('/agendar')
def agendar():
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    paciente_dict = session.get('paciente')
    paciente = Paciente(paciente_dict['idPaciente'], paciente_dict['nombre'], paciente_dict['apellidoPaterno'], paciente_dict['apellidoMaterno'], paciente_dict['fechaNacimiento'], paciente_dict['sexo'], paciente_dict['telefono'])

    datosEspecialidad = ModelCita.obtenerEspecialidades(db)
    print("soy las especilidades",datosEspecialidad)

    #hago diccionario de especialidades
    especializacion_dict = [{'idEspecialidad': datosEspecialidad[0], 'nombreEspecialidad': datosEspecialidad[1]} for datosEspecialidad in datosEspecialidad]
    session['especializacion'] = especializacion_dict

    #recupero la informacion de la sesion
    


    return render_template('agendar.html', user=user, paciente=paciente, especialidad=especializacion_dict)



@app.route('/agendar_cita', methods=['POST'])
def agendar_cita():

    #recupero la informacion de la sesion
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    paciente_dict = session.get('paciente')
    paciente = Paciente(paciente_dict['idPaciente'], paciente_dict['nombre'], paciente_dict['apellidoPaterno'], paciente_dict['apellidoMaterno'], paciente_dict['fechaNacimiento'], paciente_dict['sexo'], paciente_dict['telefono'])
    id_paciente = paciente_dict['idPaciente']
    print("soy el id del paciente",id_paciente)
    

    # Recuperar los datos del formulario
    if request.method == 'POST':

        horaInicioForm=request.form['horario']
        if horaInicioForm == "":
            flash("No se selecciono una hora de inicio")
            return redirect(url_for('agendar'))
        elif horaInicioForm == "1":
            horaInicio = "13:00:00"
            horaFin = "14:00:00"
        elif horaInicioForm == "2":
            horaInicio = "14:00:00"
            horaFin = "15:00:00"
        elif horaInicioForm == "3":
            horaInicio = "15:00:00"
            horaFin = "16:00:00"
        elif horaInicioForm == "4":
            horaInicio = "16:00:00"
            horaFin = "17:00:00"
        elif horaInicioForm == "5":
            horaInicio = "17:00:00"
            horaFin = "18:00:00"
            
        #recuperar el id del medico
        idUsuarioMedico = int(request.form.get('doctor'))
        print("soy el id del doctor",idUsuarioMedico)

        


        cita = CitaReservar(horaInicio, horaFin, idUsuarioMedico, id_paciente, request.form['fecha'])
        cita_agendada = ModelCita.crearCita(db, cita)
        if cita_agendada:
            flash("Cita agendada con éxito", "success")
            return redirect(url_for('agendar'))
        else:
            flash("No se pudo agendar la cita, selecciona otra fecha u horario", "danger")
            return redirect(url_for('agendar'))

        






    """ # Recuperar los datos del formulario
    exito = agendar_cita_funcion()  # Esta función debe retornar True si la cita fue agendada con éxito y False en caso contrario.
    
    if exito:
        flash('Cita agendada con éxito', 'success')
    else:
        flash('Hubo un error al agendar la cita', 'danger')
    return redirect(url_for('ruta_donde_se_muestra_el_mensaje_flash'))
 """

#con esta ruta recibo los datos del formulario de agendar, sobre todo el id de la especialidad que ocupo para obtener los doctores
@app.route('/doctores/<int:id_especialidad>', methods=['GET'])
def get_doctores(id_especialidad):
    data = ModelCita.obtenerDoctoresPorEspecialidad(db, id_especialidad)
    doctores = []
    for item in data:
        doctor = {
            'idUsuario': item[0],
            'nombre': item[1],
            'apellidoPaterno': item[2]
        }
        doctores.append(doctor)
    return jsonify(doctores)



#----Termina Agendar Citas------------------------------------------------------------------------------------------------------------------------------



#----Mi Perfil Paciente------------------------------------------------------------------------------------------------------------------------------
@app.route('/perfilPaciente')
def perfilPaciente():
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    paciente_dict = session.get('paciente')
    paciente = Paciente(paciente_dict['idPaciente'], paciente_dict['nombre'], paciente_dict['apellidoPaterno'], paciente_dict['apellidoMaterno'], paciente_dict['fechaNacimiento'], paciente_dict['sexo'], paciente_dict['telefono'])
    return render_template('perfilPaciente.html', user=user, paciente=paciente)

@app.route('/actualizar_perfil', methods=['POST'])
def actualizar_perfil():
    user_dict = session.get('user')
    idUsuario = user_dict['idUsuario']
    
    # Obtener los nuevos datos desde la solicitud HTTP
    nombreNuevo = request.form.get('nombre')
    apellidoPaternoNuevo = request.form.get('apellidoPaterno')
    apellidoMaternoNuevo = request.form.get('apellidoMaterno')
    fechaNacimientoNuevo = request.form.get('fechaNacimiento')
    sexoNuevo = request.form.get('sexo')
    telefonoNuevo = request.form.get('telefono')

    if ModelPaciente.actualizarPerfil(db, idUsuario, nombreNuevo, apellidoPaternoNuevo, apellidoMaternoNuevo, fechaNacimientoNuevo, sexoNuevo, telefonoNuevo):
        # Actualizar los datos en la sesión
        user_dict['nombre'] = nombreNuevo
        user_dict['apellidoPaterno'] = apellidoPaternoNuevo
        user_dict['apellidoMaterno'] = apellidoMaternoNuevo
        user_dict['fechaNacimiento'] = fechaNacimientoNuevo
        user_dict['sexo'] = sexoNuevo
        user_dict['telefono'] = telefonoNuevo
        
        # Guardar el objeto de sesión actualizado
        session['user'] = user_dict
        
        flash('Perfil actualizado con éxito,porfavor vuelva a iniciar sesion para ver los cambios', 'success')
    else:
        flash('Hubo un error al actualizar el perfil', 'danger')

    # Depuración: Imprimir el objeto de sesión actualizado
    print(session['user'])

    return redirect(url_for('perfilPaciente'))



#----Termina Mi Perdil Paciente------------------------------------------------------------------------------------------------------------------------------

#----Mi Perdil Doctor------------------------------------------------------------------------------------------------------------------------------
@app.route('/perfilDoctor')
def perfilDoctor():
    user_dict = session.get('user')
    user = User(user_dict['idUsuario'], user_dict['tipoUsuario'], user_dict['correoElectronico'], user_dict['contraseña'])

    medico_dict = session.get('medico')
    medico = Medico(medico_dict['idMedico'], medico_dict['nombre'], medico_dict['apellidoPaterno'], medico_dict['apellidoMaterno'], medico_dict['fechaNacimiento'], medico_dict['sexo'], medico_dict['telefono'])


    return render_template('perfilMedico.html', user=user, medico=medico)

@app.route('/actualizar_perfilDoctor', methods=['POST'])
def actualizar_perfilDoctor():
    user_dict = session.get('user')
    idUsuario = user_dict['idUsuario']
    

    nombreNuevo = request.form.get('nombre')
    apellidoPaternoNuevo = request.form.get('apellidoPaterno')
    apellidoMaternoNuevo = request.form.get('apellidoMaterno')
    fechaNacimientoNuevo = request.form.get('fechaNacimiento')
    sexoNuevo = request.form.get('sexo')
    telefonoNuevo = request.form.get('telefono')

    if ModelMedico.actualizarPerfil(db, idUsuario, nombreNuevo, apellidoPaternoNuevo, apellidoMaternoNuevo, fechaNacimientoNuevo, sexoNuevo, telefonoNuevo):
        # Actualizar los datos en la sesión
        user_dict['nombre'] = nombreNuevo
        user_dict['apellidoPaterno'] = apellidoPaternoNuevo
        user_dict['apellidoMaterno'] = apellidoMaternoNuevo
        user_dict['fechaNacimiento'] = fechaNacimientoNuevo
        user_dict['sexo'] = sexoNuevo
        user_dict['telefono'] = telefonoNuevo
        
        # Guardar el objeto de sesión actualizado
        session['user'] = user_dict
        
        flash('Perfil actualizado con éxito,porfavor vuelva a iniciar sesion para ver los cambios', 'success')
    else:
        flash('Hubo un error al actualizar el perfil', 'danger')


    print(session['user'])

    return redirect(url_for('perfilDoctor'))


@app.route('/ruta-para-editar-paciente', methods=['POST'])
def editar_paciente():
    id_paciente = request.form['idPaciente']
    paciente = db.session.query(Paciente).get(id_paciente)
    if paciente:

        return redirect(url_for('homeAdmi'))
    else:
        # Manejar el caso en que el paciente no se encuentra
        return "Paciente no encontrado", 404

@app.route('/ruta-para-editar-medico', methods=['POST'])
def editar_medico():
    id_medico = request.form['idMedico']
    medico = db.session.query(Medico).get(id_medico)
    if medico:
        

        return redirect(url_for('homeAdmi'))
    else:
        return "Medico no encontrado", 404
    

#----Termina Mi Perdil Doctor------------------------------------------------------------------------------------------------------------------------------



@app.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
