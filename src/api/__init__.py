from flask import Flask

from src.api.models import db

def create_app(config_name):
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "miso-uniandes"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:miso4501@db:5432/miso4501db'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/postgres'
    db.init_app(app)
    return app

