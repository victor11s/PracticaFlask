from.entities.Historial import Historial

class ModelHistorial():

    @classmethod #para poder usarlo sin instanciarlo
    def obtener_id_historial_paciente(self,db,idPaciente):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_id_historial_paciente({}) """.format(idPaciente)
            cursor.execute(sql)
            row=cursor.fetchall()
            return row
        except Exception as ex:
            raise Exception(ex)

    @classmethod #para poder usarlo sin instanciarlo   
    def obtener_historial_paciente(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_historialmedico({}) """.format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            return row
        except Exception as ex:
            raise Exception(ex)

    