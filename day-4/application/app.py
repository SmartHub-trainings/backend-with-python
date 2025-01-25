from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended  import JWTManager,create_access_token,jwt_required,get_jwt_identity


app= Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///blogDB.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["JWT_SECRET_KEY"] = "gggjjsjkkkkdkkd"

db= SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt= JWTManager(app)
def serialize_user(user_data:tuple):
    article ={"id":user_data.id,
                              "firstName":user_data.first_name,
                              "lastName":user_data.last_name,
                              "password":f"{user_data.password}",
                              "phone":user_data.phone,
                              "email":user_data.email,
                              }
    return article

def serialize_users(users:tuple):
    return [serialize_user(user) for user in users]



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String,nullable=False)
    phone = db.Column(db.String,nullable=False)
    

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    content = db.Column(db.Text,nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    is_deleted = db.Column(db.Boolean,nullable=True,default=False)
    deleted_at = db.Column(db.DateTime,nullable=True)
    
    

@app.route("/")
def home():
    return "Welcome to my blog!"

@app.route("/users/register",methods=["POST"])
def register_user():
    body = request.json
    hashed_password = bcrypt.generate_password_hash(body.get("password")).decode("utf-8")
    new_user = User(first_name=body.get("firstName"),
                    last_name=body.get("lastName"),
                    email=body.get("email"),
                    password=hashed_password,
                    phone=body.get("phone"))
    db.session.add(new_user)
    db.session.commit()

    serialized_user = serialize_user(new_user)
    return {"message":"created a user",
            "data":serialized_user},201
    
@app.route("/users/login",methods=["POST"])
def login_user():
    body = request.json
    email = body.get("email")
    password = body.get("password")
    user = User.query.filter_by(email=email).first()
    is_password = bcrypt.check_password_hash(user.password,password)
    if not is_password:
        return {"message":"Invalid credentials",
            "data":None},400
    
    access_token = create_access_token(str(user.id))    
    return {"message":"Login successful",
            "data":{'access_token':access_token}}
    
@app.route("/users")
@jwt_required()
def get_all_users():
    current_user = get_jwt_identity()
    print(current_user)
    users = User.query.all()
    serialized_users = serialize_users(users)
    return {"message":"obtained all users",
            "data":serialized_users}
    

if __name__ == "__main__":
    # Create tables before running the app
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)