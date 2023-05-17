class Config():
    SECRET_KEY = '4335'

#iniciar el servidor en modo de depuracion
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'mediapp2.ctoyvdu4lxpi.us-east-2.rds.amazonaws.com'
    MYSQL_USER = 'admin'
    MYSQL_PASSWORD = 'Cx5mlp4335'
    MYSQL_DB = 'mediapp2'

config = {
    'development': DevelopmentConfig
}