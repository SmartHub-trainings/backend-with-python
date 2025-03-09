from flask_restful import Resource,Api

from flask import Blueprint
from controllers.auth import LoginResource,RegistrationResource

auth_blueprint = Blueprint("auth",__name__)
api =Api(auth_blueprint)

    
    
api.add_resource(LoginResource,"/login")
api.add_resource(RegistrationResource,"/register")
    