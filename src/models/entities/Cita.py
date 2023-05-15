
class Cita():
    def __init__(self,idCita,fechaCita,horaInicio,horaFin):
        self.idCita = idCita
        self.fechaCita = fechaCita
        self.horaInicio = horaInicio
        self.horaFin = horaFin


class CitaReserva():
    def __init__(self, idCita, idUsuarioPaciente, idUsuarioMedico):
        self.idCita = idCita
        self.idUsuarioPaciente = idUsuarioPaciente
        self.idUsuarioMedico = idUsuarioMedico
        