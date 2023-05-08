from.entities.Paciente import Paciente

class ModelPaciente():
    @classmethod # CAMBIAR PARA QUE FUNCIONEEEEEE
    def register(self,db,user): 
        #haz el mismo metodo de arriba, pero sin pedir el tipo de usuario, ademas pide el nombre, apellido paterno y materno, sexo, telefono y su correo y contraseña, usando el modelo de UserRegistro
        try:
            cursor = db.connection.cursor()
            sql=""" INSERT INTO paciente (nombre, apellidoPaterno, apellidoMaterno, sexo, telefono, correoElectronico, contraseña) VALUES ('{}','{}','{}','{}','{}','{}','{}') """.format(user.nombre,user.apellidoPaterno,user.apellidoMaterno,user.sexo,user.telefono,user.correoElectronico,user.contraseña)
            cursor.execute(sql)
            db.connection.commit()
            print("Usuario registrado")
            return True
        except Exception as ex:
            print("No se pudo registrar")
            raise Exception(ex)