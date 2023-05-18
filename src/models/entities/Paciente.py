

class Paciente():
    def __init__(self, idUsuario, nombre,apellidoPaterno,apellidoMaterno,fechaNacimiento,sexo,telefono):
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.apellidoPaterno = apellidoPaterno
        self.apellidoMaterno = apellidoMaterno
        self.fechaNacimiento = fechaNacimiento
        self.sexo = sexo
        self.telefono = telefono
    
class PacienteRegistro():
    def __init__(self,idUsuario ,nombre,apellidoPaterno,apellidoMaterno,fechaNacimiento,sexo,telefono):
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.apellidoPaterno = apellidoPaterno
        self.apellidoMaterno = apellidoMaterno
        self.fechaNacimiento = fechaNacimiento
        self.sexo = sexo
        self.telefono = telefono

class PacienteCita():
    def __init__(self,idCita,idMedico,nombre,apellidoPaterno,fecha,horaInicio,horaFin):
        self.idCita = idCita
        self.idMedico = idMedico
        self.nombre = nombre
        self.apellidoPaterno = apellidoPaterno
        self.fecha = fecha
        self.horaInicio = horaInicio
        self.horaFin = horaFin

