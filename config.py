import os


DEBUG = True

SECRET_KEY = os.urandom(24)

#database_config
DIALECT = 'mysql'
DRIVER  = 'pymysql'
USERNAME = 'root'
PASSWORD = 'zz683986'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'online_edu'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True