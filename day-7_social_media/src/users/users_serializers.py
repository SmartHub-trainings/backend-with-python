def serialize_user(user_data:tuple):
    user ={"id":user_data.id,
                              "firstName":user_data.first_name,
                              "lastName":user_data.last_name,
                              "password":user_data.password,
                              "phone":user_data.phone,
                              "email":user_data.email,
                              "is_verified":user_data.is_verified,
                              "role":user_data.role
                              }
    return user

def serialize_users(users:tuple):
    return [serialize_user(user) for user in users]