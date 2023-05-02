from.entities.User import User

class ModelUser():

    @classmethod #para poder usarlo sin instanciarlo 
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql= """ SELECT paciente.numPaciente, paciente.correoElectronico, paciente.contraseña FROM paciente WHERE correoElectronico = '{}' """.format(user.correoElectronico)
            cursor.execute(sql)
            row=cursor.fetchone()
            # con este if verifico que exista el usuario y mediante la funcion de user de checak password, verifico que la contraseña sea correcta, se le pasa la correcta con el hash y despues se le pasa la que dio el usuario
            if row != None:
                user=User(row[0],row[1], User.check_password(row[2],user.contraseña))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
