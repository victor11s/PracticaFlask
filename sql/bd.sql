CREATE TABLE paciente(
    numPaciente int NOT NULL AUTO_INCREMENT,
    nombre varchar(50) NOT NULL,
    apellidoPaterno varchar(50),
    apellidoMaterno varchar(50),
    fechaNacimiento date,
    sexo varchar(15),
    telefono varchar(50),
    correoElectronico varchar(50),
    contraseña char(150) NOT NULL,
    PRIMARY KEY (numPaciente)
);


CREATE TABLE direcciones_Pacientes(
    idDireccion int AUTO_INCREMENT,
    numPaciente int NOT NULL,
    ciudad varchar(50) NOT NULL,
    colonia varchar(50) NOT NULL,
    calle varchar(50),
    numExterior int,
    codigoPostal int,
    PRIMARY KEY (idDireccion),
    CONSTRAINT FK_direccionesPacientes FOREIGN KEY (numPaciente) REFERENCES paciente(numPaciente)
);

CREATE TABLE medico(
    idMedico int NOT NULL,
    rfc varchar(50),
    nombre varchar(50),
    apellidoPaterno varchar(50),
    apellidoMaterno varchar(50),
    fechaNacimiento date,
    sexo varchar(15),
    telefono varchar(50),
    PRIMARY KEY (idMedico)
);

INSERT INTO medico(idMedico, rfc, nombre, apellidoPaterno,apellidoMaterno, fechaNacimiento, sexo, telefono) VALUES (1, 'XAXX010101000', 'Alan', 'Perez', 'Lopez', '1990-05-19', 'Masculino', '52 81 5555 5555');

CREATE TABLE horariosMedicos(
    idMedico int NOT NULL,
    diaSemana varchar(50) NOT NULL,
    horaInicio time NOT NULL,
    horaFin time NOT NULL,
    PRIMARY KEY (idMedico, diaSemana),
    CONSTRAINT FK_horario FOREIGN KEY (idMedico) REFERENCES medico(idMedico)
);

CREATE TABLE especialidades(
    idEspecialidad int AUTO_INCREMENT,
    nombreEspecialidad varchar(50),
    PRIMARY KEY (idEspecialidad)
);

CREATE TABLE especialidadMedico(
    id int AUTO_INCREMENT,
    idMedico int NOT NULL,
    idEspecialidad int NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT FK_especialidad1 FOREIGN KEY (idMedico) REFERENCES medico(idMedico),
    CONSTRAINT FK_especialidad2 FOREIGN KEY (idEspecialidad) REFERENCES especialidades(idEspecialidad)
);

CREATE TABLE examenes(
    idExamen int AUTO_INCREMENT,
    tipoExamen varchar(50) NOT NULL,
    PRIMARY KEY (idExamen)
);

CREATE TABLE resultadoExamen(
    numPaciente int NOT NULL,
    idExamen int NOT NULL,
    fechaExamen date NOT NULL,
    resultadosExamen varchar(100) NOT NULL,
    PRIMARY KEY (numPaciente, idExamen, fechaExamen),
    CONSTRAINT FK_pide1 FOREIGN KEY (numPaciente) REFERENCES paciente(numPaciente),
    CONSTRAINT FK_pide2 FOREIGN KEY (idExamen) REFERENCES examenes(idExamen)
);

CREATE TABLE citasReservadas(
    idCita int AUTO_INCREMENT,
    numPaciente int NOT NULL,
    idMedico int NOT NULL,
    PRIMARY KEY (idCita),
    CONSTRAINT FK_citaReservada1 FOREIGN KEY (numPaciente) REFERENCES paciente(numPaciente),
    CONSTRAINT FK_citaReservada2 FOREIGN KEY (idMedico) REFERENCES medico(idMedico)
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
    idHistorial int AUTO_INCREMENT,
    numConsulta int NOT NULL,
    enfermedad varchar(50),
    PRIMARY KEY (idHistorial)
);

CREATE TABLE historial_Paciente(
    numPaciente int NOT NULL,
    idHistorial int NOT NULL,
    PRIMARY KEY (numPaciente, idHistorial),
    CONSTRAINT FK_historial1 FOREIGN KEY (numPaciente) REFERENCES paciente(numPaciente),
    CONSTRAINT FK_historial2 FOREIGN KEY (idHistorial) REFERENCES historialMedico(idHistorial)
);

CREATE TABLE tratamientos(
    numPaciente int NOT NULL,
    idMedico int NOT NULL,
    idTratamiento int NOT NULL,
    nombre varchar(50) NOT NULL,
    descripcion varchar(150) NOT NULL,
    PRIMARY KEY (numPaciente, idMedico, idTratamiento),
    CONSTRAINT FK_tratamientos1 FOREIGN KEY (numPaciente) REFERENCES paciente(numPaciente),
    CONSTRAINT FK_tratamientos2 FOREIGN KEY (idMedico) REFERENCES medico(idMedico)
);
