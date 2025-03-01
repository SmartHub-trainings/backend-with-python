
from flask_restful import Resource
class LoginResource(Resource):
    def post(self):
        return {"message":"All working"}
    
class RegistrationResource(Resource):
    def post(self):
        return {"message":"Register route: working"}