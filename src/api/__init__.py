from flask import Flask

from models import db

def create_app(config_name):
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "miso-uniandes"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:miso4501@db:5432/miso4501db'
    db.init_app(app)
    return app

