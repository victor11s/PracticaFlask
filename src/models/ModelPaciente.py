from.entities.Paciente import Paciente
from.ModelUser import ModelUser

class ModelPaciente():
    @classmethod # CAMBIAR PARA QUE FUNCIONEEEEEE
    def register(cls, db, user, paciente):
        # Registrar usuario primero
        ModelUser.register(db, user)

        # Obtener idUsuario generado automáticamente
        cursor = db.connection.cursor()
        idUsuario = cursor.lastrowid

        # Insertar registro de paciente
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO pacientes (idUsuario, fechaNacimiento, peso, estatura) 
            VALUES ({},'{}',{},'{}') """.format(idUsuario, paciente.fechaNacimiento, paciente.peso, paciente.estatura)
            cursor.execute(sql)
            db.connection.commit()
            print("Paciente registrado")
        except Exception as ex:
            print("No se pudo registrar el paciente")
            raise Exception(ex)
        
    @classmethod
    def obtener_info_Paciente_por_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_info_paciente_por_id({}) """.format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            return row
        except Exception as ex:
            raise Exception(ex)
        
   
    @classmethod
    def actualizarPerfil(cls, db, idUsuario, nombreNuevo, apellidoPaternoNuevo, apellidoMaternoNuevo, fechaNacimientoNuevo, sexoNuevo, telefonoNuevo):
        try:
            cursor = db.connection.cursor()
            sql = "CALL actualizar_perfil_paciente(%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (idUsuario, nombreNuevo, apellidoPaternoNuevo, apellidoMaternoNuevo, fechaNacimientoNuevo, sexoNuevo, telefonoNuevo))
            db.connection.commit()
            print("Perfil del paciente actualizado")
            return True
        except Exception as ex:
            print("No se pudo actualizar el perfil del paciente")
            print(ex)
            return False


     #--------------por ver si jalan o no-----------------------------------------------------------   
    #llamar a store procedure, que obtiene los id de los paciente que han sido atendidos por ese medico
    @classmethod
    def obtener_infoPaciente_atendido_por_Medico(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_infoPaciente_atendido_por_Medico({}) """.format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            return row
        except Exception as ex:
            raise Exception(ex)
        
     #llamar a metodo que me trae la informacion de esos pacientes del historial   
    @classmethod
    def obtener_infoPaciente_atendido_por_Medico_historial(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_infoPaciente_atendido_por_Medico_historial({}) """.format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            return row
        except Exception as ex:
            raise Exception(ex)
    
    #llamar a metodo que me trae la informacion de esos pacientes de resultados
    @classmethod
    def obtener_infoPaciente_atendido_por_Medico_resultados(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_infoPaciente_atendido_por_Medico_resultados({}) """.format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            return row
        except Exception as ex:
            raise Exception(ex)