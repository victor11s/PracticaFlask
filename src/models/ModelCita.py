from.entities.Cita import Cita

class ModelCita():
    @classmethod
    def crearCita(self,db,cita):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL crear_cita('{}','{}','{}','{}') """.format(cita.fechaCita,cita.horaInicio,cita.horaFin,cita.idUsuarioMedico)
            cursor.execute(sql)
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