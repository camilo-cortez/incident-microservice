from flask import Flask
from src.api.models import db
import os

def create_app(config_name):
    app = Flask(__name__)
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')

    db_connection = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    app.config["JWT_SECRET_KEY"] = "miso-uniandes"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
    db.init_app(app)
    return app

