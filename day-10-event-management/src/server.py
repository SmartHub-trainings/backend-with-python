from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from settings.environment import ENVS
import os
from configs.cloudinary import cloudinary
import cloudinary.uploader
from routes.auth import auth_blueprint
from routes.events import events_blueprint


app = Flask(__name__)
upload_folder = "uploads"
# os.mkdir(upload_folder,exist_ok=True)
os.makedirs(upload_folder,exist_ok=True)


app.config["SQLALCHEMY_DATABASE_URI"] =ENVS.DATABASE_URI.value

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
            image,
            folder=ENVS.CLOUDINARY_UPLOAD_FOLDER.value
        )
    return {
        "message": "File uploaded successfully",
        "url": result.get("secure_url"),
        "folder": result['folder']
    }
    
    
"app>routes>controller>services"

app.register_blueprint(auth_blueprint,url_prefix="/auth")
app.register_blueprint(events_blueprint,url_prefix="/events")



    


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True,port=6003)