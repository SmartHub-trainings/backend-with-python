

from flask import request ,Blueprint
from users.users_serializers import serialize_user
from flask_jwt_extended  import create_access_token,jwt_required,get_jwt_identity
from configs.extensions import db, bcrypt
from users.users_models import User,ROLES
from utils.index import is_authorized

users_bp = Blueprint("users", __name__)

def authorize_user(roles:list):
    def outer_wrapper(route_handler):
        def wrapper():
            # print("You are about to call this route")
            current_user_id=get_jwt_identity()
            current_user = User.query.get(current_user_id)
            user_is_authorised= is_authorized(roles,current_user.role)
            db.session.commit()
            if not user_is_authorised:
                return {"message":"Unauthorized"},403
            return route_handler()
        return wrapper
    return outer_wrapper


@users_bp.route("/users/register",methods=["POST"])
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
    
    
@users_bp.route("/users/login",methods=["POST"])
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
    
    
@users_bp.route("/admin/users/verify-user",methods=["PATCH"])
@jwt_required()
@authorize_user(["user"])
def verify_user_route():
    try:
        user_id = request.json.get("user_id")
        user = User.query.filter_by(id=user_id).first()
        user.is_verified =True
        db.session.commit()
        
        
        
          
        return {"message":"User verified","user":serialize_user(user)}
    except Exception as e:
        print(e)
        return {"message":"error"},500




    
    