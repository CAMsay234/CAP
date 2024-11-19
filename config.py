import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))

def get_db_path():
    # Si estás corriendo dentro de un ejecutable PyInstaller
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(os.path.expanduser("~"), "Documents")
    else:
        base_path = basedir

    # Crear la carpeta instance en la ubicación correcta si no existe
    instance_path = os.path.join(base_path, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)

    db_path = os.path.join(instance_path, 'CAP.db')
    return db_path

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + get_db_path()
    SQLALCHEMY_TRACK_MODIFICATIONS = False


