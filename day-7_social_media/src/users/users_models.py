from configs.extensions import db

ROLES={
    "USER":"user",
    "ADMIN":"admin"
}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String,nullable=False)
    is_verified= db.Column(db.Boolean, default=False)
    role= db.Column(db.String,default=ROLES["USER"])
    phone = db.Column(db.String,nullable=False)