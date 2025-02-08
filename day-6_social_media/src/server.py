from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from users.users_serializers import serialize_user
from flask_jwt_extended  import JWTManager,create_access_token,jwt_required,get_jwt_identity
from utils.index import is_authorized

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///socilaMediaDb.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["JWT_SECRET_KEY"]="HJJJJJJDGGBBD"
bcrypt =Bcrypt(app)

db= SQLAlchemy(app)
jwt=JWTManager(app)

POST_STATUS={
    "DRAFT":"draft",
    "PUBLISH":"publish"
}

ROLES={
    "USER":"user",
    "ADMIN":"admin"
}

@app.before_request
def before_request():
    # return {"messages":"Come back later"}
    print("This will run before anything else")
    
@app.after_request
def after_request(response):
    print(response.status_code)
    # response.status_code = 401
    return response
    

    
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
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String,nullable=False)
    is_verified= db.Column(db.Boolean, default=False)
    role= db.Column(db.String,default=ROLES["USER"])
    phone = db.Column(db.String,nullable=False)
    
    
# app.register_blueprint(users_bp)



@app.route("/")
def index():
    return {"message":"ApI is running just fine."}


@app.route("/users/register",methods=["POST"])
def register_user():
    
    body = request.json
    print(body)
    password = bcrypt.generate_password_hash(body.get("password")).decode("utf-8")
    new_user = User(last_name=body.get("last_name"),
                    first_name=body.get("first_name"),
                    password=password,
                    email=body.get("email"),
                    phone=body.get("phone")
                    # role = body.get("role")
                    )
    db.session.add(new_user)
    db.session.commit()
    serialized_user = serialize_user(new_user)
    return {"message":"created a user",
        "data":serialized_user},201
    
    
@app.route("/users/login",methods=["POST"])
def login_user():
    try:
        body = request.json
       
    except Exception as e:
        return {"message":"Validation error","errors":e.messages},400
    email = body.get("email")
    password = body.get("password")
    user = User.query.filter_by(email=email).first()
    
    is_password = bcrypt.check_password_hash(user.password,password)
    if not is_password:
        return {"message":"Invalid credentials",
            "data":None},400
        
    is_verified = user.is_verified
    if user.role!= ROLES["ADMIN"]:
        if not is_verified:
            return {"message":"Your account is not verified yet. You will receiev an email once your accout is verified",
                "data":None},400
    
    access_token = create_access_token(str(user.id))    
    return {"message":"Login successful",
            "data":{'access_token':access_token}}
    
    
@app.route("/admin/users/verify-user",methods=["PATCH"])
@jwt_required()
def verify_user_route():
    try:
        user_id = request.json.get("user_id")
        current_user_id=get_jwt_identity()
        print(current_user_id) 
        current_user = User.query.filter_by(id=current_user_id).first()
        user_is_authorised= is_authorized(["admin","super-admin"],current_user.role)
        db.session.commit()
        user = User.query.filter_by(id=user_id).first()
        if not user_is_authorised:
            return {"message":"Unauthorized"},403
        
        user.is_verified =True
        db.session.commit()
        
        
        print(user)
        
          
        return {"message":"User verified","user":serialize_user(user)}
    except Exception as e:
        print(e)
        return {"message":"error"},500






if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=6002)