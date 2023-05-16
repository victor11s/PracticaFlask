from.entities.Cita import Cita

class ModelCita():
    #Inserta una cita en la base de datos
    @classmethod
    def crearCita(self, db, cita):
        try:
            cursor = db.connection.cursor()

            # Primero insertamos en la tabla CitasReservadas
            sql_citas_reservadas = """INSERT INTO citasreservadas (idUsuarioPaciente, idUsuarioMedico)
                                    VALUES ('{}', '{}')""".format(cita.idUsuarioPaciente, cita.idUsuarioMedico)
            cursor.execute(sql_citas_reservadas)
            db.connection.commit()

            # Obtenemos el idCita autoincrementado generado en la tabla CitasReservadas
            id_cita = cursor.lastrowid

            # Verificamos si hay alguna cita existente con la misma fecha, horario y médico
            sql_verificar_citas = """SELECT COUNT(*) FROM citainformacion
                                    WHERE fechacita = '{}' AND 
                                    (horaInicio <= '{}' AND horaFin >= '{}')""".format(
                cita.fechaCita, cita.horaFin, cita.horaInicio)
            cursor.execute(sql_verificar_citas)
            count = cursor.fetchone()[0]

            if count > 0:
                # Si hay citas que se superponen, no realizamos la inserción y retornamos False
                return False

            # Insertamos en la tabla CitaInformacion
            sql_cita_informacion = """INSERT INTO citainformacion (idCita, fechacita, horaInicio, horaFin)
                                    VALUES ('{}', '{}', '{}', '{}')""".format(
                id_cita, cita.fechaCita, cita.horaInicio, cita.horaFin)
            cursor.execute(sql_cita_informacion)
            db.connection.commit()

            return True
        except Exception as ex:
            raise Exception(ex)


        
    @classmethod
    def obtenerEspecialidades(self,db):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_todas_especialidades() """
            cursor.execute(sql)
            row=cursor.fetchall()
            return row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def obtenerDoctoresPorEspecialidad(self, db, especialidad_id):
        try:
            cursor = db.connection.cursor()
            sql = """ CALL obtener_doctores_por_especialidad({}) """.format(especialidad_id)
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except Exception as ex:
            raise Exception(ex)