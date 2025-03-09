from flask_restful import Resource
from models.events import events
from flask import request
from random import choices
from services.events import create_new_event




class EventsResource(Resource):
    def get(self):
        
        return {"message":"for get: All events","data":events}
    
    def post(self):
        body = request.json
        event =create_new_event(body)
        return {"message":"for post: Create a new event",
                "data":event},201
    
class SingleEventsResource(Resource):
    def get(self,event_id):
        print(event_id)
        return {"message":"for get: Single event by id"}
    
    def put(self,event_id):
        print(event_id)
        return {"message":"for put: Update an event by id"}
    
    def delete(self,event_id):
        print(event_id)
        return {"message":"for delete: Delete an event by id"}