import os

class Config(object):
    SECRET_KEY = 'my_secret_key'


class DevelopmentConfig(Config): #el parametro es de donde ereda
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/flask_practicas' #entes del arroba y despues de los : va la clave si tuviera
    SQLALCHEMY_TRACK_MODIFICATIONS = False
