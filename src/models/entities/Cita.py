
class Cita():
    def __init__(self,idCita,fechaCita,horaInicio,horaFin):
        self.idCita = idCita
        self.fechaCita = fechaCita
        self.horaInicio = horaInicio
        self.horaFin = horaFin


class CitaReservar():
    def __init__(self, horaInicio, horaFin, idUsuarioMedico, idUsuarioPaciente, fechaCita):
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.idUsuarioMedico = idUsuarioMedico
        self.idUsuarioPaciente = idUsuarioPaciente
        self.fechaCita = fechaCita

