

from flask import request ,Blueprint
from users.users_serializers import serialize_user
from configs.extensions import db, bcrypt
from users.users_models import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/users/register",methods=["POST"])
def register_user():
    
    body = request.json
    print(body)
    password = bcrypt.generate_password_hash(body.get("password")).decode("utf-8")
    new_user = User(last_name=body.get("last_name"),
                    first_name=body.get("first_name"),
                    password=password,
                    email=body.get("email")
                    )
    db.session.add(new_user)
    db.session.commit()
    serialized_user = serialize_user(new_user)
    return {"message":"created a user",
        "data":serialized_user},201