from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from settings.environment import ENVS
import os
from configs.cloudinary import cloudinary
import cloudinary.uploader
from flask_restful import Api, Resource

app = Flask(__name__)
upload_folder = "uploads"
# os.mkdir(upload_folder,exist_ok=True)
os.makedirs(upload_folder,exist_ok=True)


app.config["SQLALCHEMY_DATABASE_URI"] =ENVS.DATABASE_URI.value
api = Api(app)

ALLOWED_EXTENSIONS ={"png","jpeg","gif"}
@app.route("/upload",methods=["POST"])
def upload_file_handler():
    files =request.files
    image = files.get("image")
    passport = files.get("passport")

    print({'image':image,"passport":passport})
    extension=image.filename.split(".")[-1]
    print(extension)
    if extension not in ALLOWED_EXTENSIONS:
        return {"message":"Invalid file type"}
    # image.save(image.filename)
    # image.save(f"{upload_folder}/{image.filename}")
    # passport.save(f"{upload_folder}/{passport.filename}")
    
    result = cloudinary.uploader.upload(
            passport,
            folder=ENVS.CLOUDINARY_UPLOAD_FOLDER.value
        )
    return {
        "message": "File uploaded successfully",
        "url": result.get("secure_url"),
        "folder": result['folder']
    }
    
class LoginResource(Resource):
    def post(self):
        return {"message":"All working"}
    
    def get(self):
        return {"message":"for get: All working"}
    
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
    
    
api.add_resource(LoginResource,"/login")
api.add_resource(EventsResource,"/events")
api.add_resource(SingleEventsResource,"/events/<int:event_id>")

    


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True,port=6003)