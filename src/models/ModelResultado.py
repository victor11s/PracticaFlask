from.entities.Resultado import Resultado

class ModelResultado():

    @classmethod
    def getResults(self,db,idPaciente):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_resultados_paciente({}) """.format(idPaciente)
            cursor.execute(sql)
            row=cursor.fetchall()
            return row
        except Exception as ex:
            raise Exception(ex)