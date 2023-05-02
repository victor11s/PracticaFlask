from werkzeug.security import check_password_hash, generate_password_hash
#si quiero probar con una contraseña nueva importar funcion ", generate_password_hash"
class User():
    def __init__(self, numPaciente, correoElectronico, contraseña, tipoUsuario):
        self.numPaciente = numPaciente
        self.correoElectronico = correoElectronico
        self.contraseña = contraseña
        self.tipoUsuario = tipoUsuario

    @classmethod #para no instanciar la clase  
    def check_password(self, hashed_password, contraseña):
        return check_password_hash(hashed_password, contraseña)
    
class UserRegistro():
    def __init__(self, nombre, apellidoPaterno, apellidoMaterno, sexo, telefono, correoElectronico, contraseña):
        self.nombre = nombre
        self.apellidoPaterno = apellidoPaterno
        self.apellidoMaterno = apellidoMaterno
        self.sexo = sexo
        self.telefono = telefono
        self.correoElectronico = correoElectronico
        self.contraseña = contraseña
    
    @classmethod
    def hash_password(self, contraseña):
        return generate_password_hash(contraseña)
    
    




#print(generate_password_hash('bigmac'))