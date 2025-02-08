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