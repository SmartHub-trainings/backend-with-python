from flask_restful import Resource,Api
from flask import Blueprint
from controllers.events import SingleEventsResource,EventsResource

events_blueprint=  Blueprint('events',__name__)

api = Api(events_blueprint)



    
api.add_resource(EventsResource,"")
api.add_resource(SingleEventsResource,"/<int:event_id>")