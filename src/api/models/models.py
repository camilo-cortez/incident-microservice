from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from enum import Enum
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128))
    email = db.Column(db.String(150))
    password = db.Column(db.String(150))
    # incidents = db.relationship('Incident', backref='user', lazy=True)

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    incident_type = db.Column(db.String(25))
    status = db.Column(db.String(25))
    description = db.Column(db.String(150))
    channel = db.Column(db.String(25))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class IncidentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incident
        include_relationships = True
        load_instance = True

    id = fields.String()