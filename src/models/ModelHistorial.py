from.entities.Historial import Historial

class ModelHistorial():

    def obtener_id_historial_paciente(self,db,idPaciente):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_id_historial_paciente({}) """.format(idPaciente)
            cursor.execute(sql)
            row=cursor.fetchone()
            return row
        except Exception as ex:
            raise Exception(ex)
        
    def obtener_historial_paciente(self,db,idPaciente):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_historial_paciente({}) """.format(idPaciente)
            cursor.execute(sql)
            row=cursor.fetchone()
            return row
        except Exception as ex:
            raise Exception(ex)

    