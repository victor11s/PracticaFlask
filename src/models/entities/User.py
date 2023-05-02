from werkzeug.security import check_password_hash, generate_password_hash
#si quiero probar con una contraseña nueva importar funcion ", generate_password_hash"
class User():
    def __init__(self, numPaciente, correoElectronico, contraseña):
        self.numPaciente = numPaciente
        self.correoElectronico = correoElectronico
        self.contraseña = contraseña

    @classmethod #para no instanciar la clase  
    def check_password(self, hashed_password, contraseña):
        return check_password_hash(hashed_password, contraseña)

#print(generate_password_hash('bigmac'))