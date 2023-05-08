class Config():
    SECRET_KEY = '4335'

#iniciar el servidor en modo de depuracion
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'mediapp2'

config = {
    'development': DevelopmentConfig
}