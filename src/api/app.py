from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from src.api import create_app, db

from src.api.views.views import ViewIncidents
from src.api.views import (
    ViewRegister,
    ViewLogin,
    ViewIncident,
    ViewPing
)

app = create_app('incidents-api')

app_context = app.app_context()
app_context.push()
db.create_all()

cors = CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app)
api.add_resource(ViewRegister, "/user-register")
api.add_resource(ViewLogin, "/login")
api.add_resource(ViewIncident, "/incident/<int:id_incident>")
api.add_resource(ViewIncidents, "/incidents")
api.add_resource(ViewPing, "/ping")
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)