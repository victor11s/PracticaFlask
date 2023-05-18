from.entities.User import User


#-------------COPIAS CON CAMBIOS--------------------------------------------------------------------------------------------------
class ModelUser():

    #haz el mismo metodo de arriba, pero obteniendo ademas su tipoUsuario
    @classmethod #para poder usarlo sin instanciarlo, este se puede quedar igual
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql= """SELECT usuarios.idUsuario, usuarios.tipoUsuario, usuarios.correoElectronico, usuarios.contraseña FROM usuarios WHERE correoElectronico = '{}' """.format(user.correoElectronico)
            cursor.execute(sql)
            row=cursor.fetchone()
            # con este if verifico que exista el usuario y mediante la funcion de user de checak password, verifico que la contraseña sea correcta, se le pasa la correcta con el hash y despues se le pasa la que dio el usuario
            if row != None:
                user=User(row[0],row[1],row[2],User.check_password(row[3],user.contraseña))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def register(self,db,user,userRegistro):
        #haz el mismo metodo de arriba, pero sin pedir el tipo de usuario, ademas pide el nombre, apellido paterno y materno, sexo, telefono y su correo y contraseña, usando el modelo de UserRegistro
        cursor = db.connection.cursor()

        cursor = db.connection.cursor()

        try:
            # Insertamos en la tabla infoUsuarios
            sql_info_usuarios = """INSERT INTO infoUsuarios (nombre, apellidoPaterno, apellidoMaterno, fechaNacimiento, sexo, telefono)
                                VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(
                userRegistro.nombre, userRegistro.apellidoPaterno, userRegistro.apellidoMaterno, userRegistro.fechaNacimiento, userRegistro.sexo, userRegistro.telefono)
            cursor.execute(sql_info_usuarios)
            db.connection.commit()

            # Obtenemos el idUsuario autoincrementado generado en la tabla infoUsuarios
            idUsuario = cursor.lastrowid

            # Insertamos en la tabla Usuarios
            sql_usuarios = """INSERT INTO Usuarios (idUsuario, tipoUsuario, correoElectronico, contraseña)
                            VALUES ('{}', '{}', '{}', '{}')""".format(
                user.idUsuario, user.tipoUsuario, user.correoElectronico, user.contraseña)
            cursor.execute(sql_usuarios)
            db.connection.commit()
        except Exception as e:
            db.connection.rollback()  # Deshacer cambios en caso de error
            print("Error: ", str(e))
        finally:
            cursor.close()

        
    @classmethod
    def get_by_id(cls, db, numPaciente):
        try:
            cursor = db.connection.cursor()
            sql=""" SELECT paciente.numPaciente, paciente.correoElectronico, paciente.contraseña, paciente.tipoUsuario FROM paciente WHERE numPaciente = '{}' """.format(numPaciente)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=User(row[0],row[1],row[2],row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)


#----------------------------------------------------------------------------------------------------------------------------------