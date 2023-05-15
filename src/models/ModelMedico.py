from.entities.Medico import Medico


class ModelMedico():
    @classmethod
    def obtener_info_Medico_por_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_info_medico_por_id({}) """.format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            return row
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def obtener_info_todos_Medicos(self,db):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_info_todos_medicos() """
            cursor.execute(sql)
            row=cursor.fetchall()
            return row
        except Exception as ex:
            raise Exception(ex)