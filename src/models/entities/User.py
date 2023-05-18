from werkzeug.security import check_password_hash, generate_password_hash
#si quiero probar con una contraseña nueva importar funcion ", generate_password_hash"
    
print(generate_password_hash('bigmac'))

#modificaciones a user desde aqui ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class User():
    def __init__(self, idUsuario,tipoUsuario, correoElectronico, contraseña ):
        self.idUsuario = idUsuario
        self.tipoUsuario = tipoUsuario
        self.correoElectronico = correoElectronico
        self.contraseña = contraseña

    @classmethod #para no instanciar la clase  
    def check_password(self, hashed_password, contraseña):
        return check_password_hash(hashed_password, contraseña)
    
    
    
class UserRegistro():
    def __init__(self,idUsuario,tipoUsuario, correoElectronico, contraseña ):
        self.idUsuario = idUsuario
        self.tipoUsuario = tipoUsuario
        self.correoElectronico = correoElectronico
        self.contraseña = contraseña
    
    @classmethod
    def hash_password(self, contraseña):
        return generate_password_hash(contraseña)




#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------