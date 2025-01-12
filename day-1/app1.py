from flask import Flask

app =Flask(__name__)

@app.route("/home")
def hello():
    return "I'm working fine!!!"

@app.route("/login")
def user_login():
    return "You are logged in\nCongrats!!!"
@app.route("/register")
def register_login():
    return "You have been registered."

@app.route("/profile")
def user_profile():
    return {
        'name':"Georg,Boma Smith",
        "age":70,
        "State":"Rivers",
        "ismarried":False,
    }


users =[
    {
        "name":"Favour",
        "id":1
    },
    {"name":"George",
     "id":3}
]

@app.route("/users")
def get_all_users():
    return {"users":users,"message":"Successfully fetched all users","status":"success"}
@app.route("/users/<int:user_id>")
def get_a_user(user_id):
    try:
    
        return {"data":users[user_id-1]}
    except IndexError:
        return {
            "error":f"No user in the position {user_id}"
        }
    
# if __name__=="__main__":
#     app.run()


if __name__=="__main__":
    app.run(debug=True)


