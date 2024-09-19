import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Esta es la ruta correcta, que apunta a la base de datos cap.db en la carpeta instance
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'CAP.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

