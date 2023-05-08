from.entities.Paciente import Paciente

class ModelPaciente():
    @classmethod # CAMBIAR PARA QUE FUNCIONEEEEEE
    def registerPaciente(self,db,paciente): 
        #haz el mismo metodo de arriba, pero sin pedir el tipo de usuario, ademas pide el nombre, apellido paterno y materno, sexo, telefono y su correo y contraseña, usando el modelo de UserRegistro
        try:
            cursor = db.connection.cursor()
            sql=""" INSERT INTO infousuarios (idUsuario,nombre, apellidoPaterno, apellidoMaterno,fechaNacimiento, sexo, telefono) VALUES ('{}','{}','{}','{}','{}','{}','{}') """.format(paciente.idUsuario,paciente.nombre,paciente.apellidoPaterno,paciente.apellidoMaterno,paciente.fechaNacimiento,paciente.sexo,paciente.telefono)
            cursor.execute(sql)
            db.connection.commit()
            print("Usuario registrado")
            return True
        except Exception as ex:
            print("No se pudo registrar")
            raise Exception(ex)

        