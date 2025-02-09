from flask import Flask
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_jwt_extended  import JWTManager
from configs.extensions import db
from users.users_routes import users_bp


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///socilaMediaDb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["JWT_SECRET_KEY"]="HJJJJJJDGGBBD"
bcrypt =Bcrypt(app)

db.init_app(app)
jwt=JWTManager(app)

POST_STATUS={
    "DRAFT":"draft",
    "PUBLISH":"publish"
}



app.register_blueprint(users_bp)
    

    
class POST(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String,nullable=False)
    image_url= db.Column(db.String,nullable=True)
    video_url= db.Column(db.String,nullable=True)
    status= db.Column(db.String,default=POST_STATUS["DRAFT"])
    is_comment=db.Column(db.Boolean,default=False)
    parent_post_id= db.Column(db.Integer,nullable=True)
    likes_count   = db.Column(db.Integer,nullable=False,default=0)
    is_deleted = db.Column(db.Boolean,default=False)
    
class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer,nullable=False)
    follower_id = db.Column(db.Integer,nullable=False)
    created_at = db.Column(db.Date,nullable=False,default=datetime.utcnow())
    updated_at = db.Column(db.Date,nullable=False,default=datetime.utcnow())
    

@app.route("/")
def index():
    return {"message":"ApI is running just fine."}



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=6002)