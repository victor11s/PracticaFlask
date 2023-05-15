from.entities.Administrador import Administrador


class ModelAdministrador():
    @classmethod
    def obtener_info_Administrador_por_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql=""" CALL obtener_info_administrador_por_id({}) """.format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            return row
        except Exception as ex:
            raise Exception(ex)
