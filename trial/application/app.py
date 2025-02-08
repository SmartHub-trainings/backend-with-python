from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended  import JWTManager,create_access_token,jwt_required,get_jwt_identity
from schema.auth_schema import registration_schema, login_schema

from serializers.users_serializers import serialize_user , serialize_users


app= Flask(__name__)



app.config["SQLALCHEMY_DATABASE_URI"] ="sqlite:///blogDB.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["JWT_SECRET_KEY"] = "gggjjsjkkkkdkkd"

db= SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt= JWTManager(app)

@app.before_request
def before_request():
    print("This is coming in good")
    print(f"Incoming request: {request.method} {request.path}")
    
    
@app.after_request
def after_request(response):
    print(f"Response status: {response.status_code}")
    return response

def auth_required(f):
    def wrapper(*args, **kwargs):
        print("This is a custom middleware for a route")
        api_key = request.headers.get("X-API-KEY")
        if api_key != "secret-key":
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__  # Preserve function name
    return wrapper

def role_required(allowed_roles):
    def decorator(f):
        def wrapper(*args, **kwargs):
            user_role = request.headers.get("X-User-Role")  # Read user role from headers
            if user_role not in allowed_roles:
                return jsonify({"error": "Access denied"}), 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

#Data base tables
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

# @app.route("/users/register",methods=["POST"])
# def register_user():
#     body = request.json
#     errors=[]
#     required_fileds= ["firstName", "lastName","email","password","repeatPassword"]
#     for field in required_fileds:
#         if not body.get(field):
#             errors.append(f"{field} is required")
    
#     if len(body.get("phone"))!=11:
#         errors.append("Phone number must be 8 characters")
#     if body.get("password")!= body.get("repeatPassword"):
#         errors.append("Passwords do not match")
#     if errors:
#         return {"message":"Validation error",
#                 "errors":errors},400
        

    
#     hashed_password = bcrypt.generate_password_hash(body.get("password")).decode("utf-8")
#     new_user = User(first_name=body.get("firstName"),
#                     last_name=body.get("lastName"),
#                     email=body.get("email"),
#                     password=hashed_password,
#                     phone=body.get("phone"))
#     db.session.add(new_user)
#     db.session.commit()

#     serialized_user = serialize_user(new_user)
#     return {"message":"created a user",
#             "data":serialized_user},201

@app.route("/users/register",methods=["POST"])
def register_user():
    body = request.json
    print({"body":body})
    try:
        validate_data = registration_schema.load(body)
        print(validate_data)
    except Exception as e:
        # print({"e":e.messages})
        # for error in dict(e).values():
        #     print(error)
        return jsonify({"message":"Validation error","errors":e.messages}),400
        
        

        
        

    
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
    try:
        body = login_schema.load(request.json)
       
    except Exception as e:
        return jsonify({"message":"Validation error","errors":e.messages}),400
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
    
@app.route("/articles")
@role_required(["admin"])
@auth_required
def all_articles_route():
    return {"msg":"This is cool"}
    

if __name__ == "__main__":
    # Create tables before running the app
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5000)