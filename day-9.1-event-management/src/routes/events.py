from flask_restful import Resource

class EventsResource(Resource):
    def get(self):
        return {"message":"for get: All events"}
    
    def post(self):
        return {"message":"for post: Create a new event"}
    
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