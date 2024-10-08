import hashlib
from random import randrange
import time
from flask import request
from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.api.models import (
    db,
    Incident,
    IncidentSchema,
    User
)

incident_schema = IncidentSchema()

class ViewRegister(Resource):
    def post(self):
        email_request = request.json["email"]
        user_request = request.json["user"]

        exist_email = User.query.filter(
            User.email == email_request
        ).first()

        exist_user = User.query.filter(
            User.user == user_request
        ).first()

        if exist_email is None and exist_user is None:
            password_encrypt = hashlib.sha3_512(
                request.json["password"].encode("utf-8")
            ).hexdigest()
            new_user = User(
                user = user_request,
                email = email_request,
                password = password_encrypt,
            )
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User create successful"}, 201
        else:
            return {"message": "User or email already exist"}, 409
        

class ViewLogin(Resource):
    def post(self):
        password_encrypt = hashlib.sha3_512(
            request.json["password"].encode("utf-8")
        ).hexdigest()

        user_email_request = request.json["user"]

        query_email = User.query.filter(
            User.email == user_email_request,
            User.password == password_encrypt,
        ).first()

        query_user = User.query.filter(
            User.user == user_email_request,
            User.password == password_encrypt,
        ).first()

        if query_email != None:
            token_access = create_access_token(identity = query_email.id)
        elif query_user != None:
            token_access = create_access_token(identity = query_user.id)
        else:
            return {"message": "User not found"}, 404

        return {
            "message": "Login success",
            "token": token_access,
        }, 200

#@jwt_required
class ViewIncident(Resource):
    def get(self, id_incident):
        incident = Incident.query.get_or_404(id_incident)
        return incident_schema.dump(Incident.query.get_or_404(incident.id))
    
    def post(self, id_incident):
        incident_type = request.json["type"]
        status = request.json["status"]
        description = request.json["description"]
        channel = request.json["channel"]

        # current_user_id = randrange(10) #get_jwt_identity() 
        time.sleep(1) #mock processing time

        new_incident = Incident(
            incident_type = incident_type,
            status = status,
            description = description,
            channel = channel
        )
        db.session.add(new_incident)
        db.session.commit()
        return incident_schema.dump(new_incident), 201
    
    def delete(self, id_incident):
        try:
            incident = Incident.query.get_or_404(id_incident)
            db.session.delete(incident)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify(error=str(e)), 500
        
class ViewIncidents(Resource):
    def get(self):
        incidents = Incident.query.all()
        return incident_schema.dump(incidents, many=True)


class ViewPing(Resource):
    def get(self):
        return "pong", 200