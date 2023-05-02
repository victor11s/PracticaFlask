from.entities.User import User

class ModelUser():

    #haz el mismo metodo de arriba, pero obteniendo ademas su tipoUsuario
    @classmethod #para poder usarlo sin instanciarlo
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql= """ SELECT paciente.numPaciente, paciente.correoElectronico, paciente.contraseña, paciente.tipoUsuario FROM paciente WHERE correoElectronico = '{}' """.format(user.correoElectronico)
            cursor.execute(sql)
            row=cursor.fetchone()
            # con este if verifico que exista el usuario y mediante la funcion de user de checak password, verifico que la contraseña sea correcta, se le pasa la correcta con el hash y despues se le pasa la que dio el usuario
            if row != None:
                user=User(row[0],row[1], User.check_password(row[2],user.contraseña), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def register(self,db,user):
        #haz el mismo metodo de arriba, pero sin pedir el tipo de usuario, ademas pide el nombre, apellido paterno y materno, sexo, telefono y su correo y contraseña, usando el modelo de UserRegistro
        try:
            cursor = db.connection.cursor()
            sql=""" INSERT INTO paciente (nombre, apellidoPaterno, apellidoMaterno, sexo, telefono, correoElectronico, contraseña) VALUES ('{}','{}','{}','{}','{}','{}','{}') """.format(user.nombre,user.apellidoPaterno,user.apellidoMaterno,user.sexo,user.telefono,user.correoElectronico,user.contraseña)
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
        
