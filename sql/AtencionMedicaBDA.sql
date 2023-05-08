CREATE TABLE infoUsuarios(
    idUsuario int AUTO_INCREMENT,
    nombre varchar(50) NOT NULL,
    apellidoPaterno varchar(50) NOT NULL,
    apellidoMaterno varchar(50),
    fechaNacimiento date,
    sexo varchar(15),
    telefono varchar(50),
    PRIMARY KEY (idUsuario)
);


CREATE TABLE tiposUsuarios(
    codigo varchar(15) NOT NULL,
    tipo varchar(50) NOT NULL,
    PRIMARY KEY (codigo)
);

CREATE TABLE direcciones(
    idDireccion int NOT NULL AUTO_INCREMENT,
    ciudad varchar(50) NOT NULL,
    colonia varchar(50) NOT NULL,
    calle varchar(50),
    numExterior int,
    numinterior varchar(20),
    codigoPostal int,
    PRIMARY KEY (idDireccion)
);

CREATE TABLE usuarios(
    idUsuario int NOT NULL,
    tipoUsuario varchar(15) NOT NULL,
    correoElectronico varchar(50) NOT NULL,
    contrasenia char(150) NOT NULL,
    PRIMARY KEY(idUsuario),
    CONSTRAINT FK_usuarios FOREIGN KEY (idUsuario) REFERENCES infoUsuarios(idUsuario),
    CONSTRAINT FK_usuarios2 FOREIGN KEY (tipoUsuario) REFERENCES tiposUsuarios(codigo)
);

CREATE TABLE direcciones_Pacientes(
    idUsuario int NOT NULL,
    idDireccion int NOT NULL,
    PRIMARY KEY (idUsuario, idDireccion),
    CONSTRAINT FK_direccionesPacientes1 FOREIGN KEY (idUsuario) REFERENCES infoUsuarios(idUsuario),
    CONSTRAINT FK_direccionesPacientes2 FOREIGN KEY (idDireccion) REFERENCES direcciones(idDireccion)
);



CREATE TABLE horarios(
    idHorario int AUTO_INCREMENT,
    diaSemana varchar(50) NOT NULL,
    horaInicio time NOT NULL,
    horaFin time NOT NULL,
    PRIMARY KEY (idHorario)
);

CREATE TABLE horariosMedicos(
    idUsuario int NOT NULL,
    idHorario int NOT NULL,
    PRIMARY KEY (idUsuario, idHorario),
    CONSTRAINT FK_horario1 FOREIGN KEY (idUsuario) REFERENCES infoUsuarios(idUsuario),
    CONSTRAINT FK_horario2 FOREIGN KEY (idHorario) REFERENCES horarios(idHorario)
);

CREATE TABLE especialidades(
    idEspecialidad int AUTO_INCREMENT,
    nombreEspecialidad varchar(50),
    PRIMARY KEY (idEspecialidad)
);

CREATE TABLE especialidadMedico(
    idUsuario int NOT NULL,
    idEspecialidad int NOT NULL,
    PRIMARY KEY (idUsuario, idEspecialidad),
    CONSTRAINT FK_especialidad1 FOREIGN KEY (idUsuario) REFERENCES infoUsuarios(idUsuario),
    CONSTRAINT FK_especialidad2 FOREIGN KEY (idEspecialidad) REFERENCES especialidades(idEspecialidad)
);

CREATE TABLE examenes(
    idExamen int AUTO_INCREMENT,
    tipoExamen varchar(50) NOT NULL,
    PRIMARY KEY (idExamen)
);

CREATE TABLE resultadoExamen(
    idUsuario int NOT NULL,
    idExamen int NOT NULL,
    fechaExamen date NOT NULL,
    resultadosExamen varchar(100) NOT NULL,
    PRIMARY KEY (idUsuario, idExamen, fechaExamen),
    CONSTRAINT FK_resultadoExamen FOREIGN KEY (idUsuario) REFERENCES infoUsuarios(idUsuario),
    CONSTRAINT FK_resultadoExamen2 FOREIGN KEY (idExamen) REFERENCES examenes(idExamen)
);

CREATE TABLE citasReservadas(
    idCita int AUTO_INCREMENT,
    idUsuarioPaciente int NOT NULL,
    idUsuarioMedico int NOT NULL,
    PRIMARY KEY (idCita),
    CONSTRAINT FK_citasReservadas FOREIGN KEY (idUsuarioPaciente) REFERENCES infoUsuarios(idUsuario),
    CONSTRAINT FK_citaReservada2 FOREIGN KEY (idUsuarioMedico) REFERENCES infoUsuarios(idUsuario)
);


CREATE TABLE citaInformacion(
    idCita int NOT NULL,
    fechaCita date,
    horaInicio time,
    horaFin time,
    PRIMARY KEY (idCita),
    CONSTRAINT FK_citaInformacion1 FOREIGN KEY (idCita) REFERENCES citasReservadas(idCita)
);

CREATE TABLE facturaDeCita(
    idFactura int AUTO_INCREMENT,
    idCita int NOT NULL,
    PRIMARY KEY (idFactura),
    CONSTRAINT FK_facturaDeCita1 FOREIGN KEY (idCita) REFERENCES citasReservadas(idCita)
);

CREATE TABLE facturaInformacion(
    idFactura int NOT NULL,
    rfcPaciente varchar(50),
    costo decimal(10,2),
    fechaFactura date,
    PRIMARY KEY(idFactura),
    CONSTRAINT FK_facturaInformacion1 FOREIGN KEY (idFactura) REFERENCES facturaDeCita(idFactura)
);

CREATE TABLE historialMedico(
    idHistorial int NOT NULL,
    numConsulta int NOT NULL,
    enfermedad varchar(50),
    PRIMARY KEY (idHistorial)
);

CREATE TABLE historial_Paciente(
    idUsuario int NOT NULL,
    idHistorial int NOT NULL,
    PRIMARY KEY (idUsuario, idHistorial),
    CONSTRAINT FK_historial1 FOREIGN KEY (idUsuario) REFERENCES infoUsuarios(idUsuario),
    CONSTRAINT FK_historial2 FOREIGN KEY (idHistorial) REFERENCES historialMedico(idHistorial)
);

CREATE TABLE tratamientos(
    idUsuarioPaciente int NOT NULL,
    idUsuarioMedico int NOT NULL,
    idTratamiento int NOT NULL,
    nombre varchar(50) NOT NULL,
    descripcion varchar(150) NOT NULL,
    PRIMARY KEY (idUsuarioPaciente, idUsuarioMedico, idTratamiento),
    CONSTRAINT FK_tratamientos1 FOREIGN KEY (idUsuarioPaciente) REFERENCES infoUsuarios(idUsuario),
    CONSTRAINT FK_tratamientos2 FOREIGN KEY (idUsuarioMedico) REFERENCES infoUsuarios(idUsuario)
);