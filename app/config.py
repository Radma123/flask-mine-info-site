import os

class Config(object):
    APPNAME = 'app'
    ROOT = os.path.abspath(APPNAME)
    UPLOAD_PATH = '/static/uploads/'
    SERVER_PATH = ROOT+UPLOAD_PATH

    USER = os.environ.get('POSTGRES_USER')
    PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    
    # ДОБАВИТЬ ПОСЛЕ РАЗРАБОТКИ .ENV
    HOST = '127.0.0.1'
    PORT = os.environ.get('POSTGRES_PORT')
    DB = os.environ.get('POSTGRES_DB')
    SECRET_KEY = os.urandom(24)

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}/{DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
