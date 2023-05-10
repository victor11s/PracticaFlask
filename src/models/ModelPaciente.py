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