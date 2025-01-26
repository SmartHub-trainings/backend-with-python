from marshmallow import Schema, fields, validate, ValidationError, validates_schema

#Validation schema 


class RegistrationSchema(Schema):
    firstName = fields.String(required=True, error_messages={"required": "First Name is required"})
    lastName = fields.String(required=True, error_messages={"required": "Last Name is required"})
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required", "invalid": "Invalid Email format"}
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=8),
        error_messages={"required": "Password is required", "minlength": "Password must be at least 8 characters long"}
    )
    repeatPassword = fields.String(
        required=True,
        error_messages={"required": "Repeat Password is required"}
    )
    phone = fields.String(
        required=True,
        validate=validate.Length(min=8, max=11),
        error_messages={
            "required": "Phone number is required",
            "minlength": "Phone number must be 8 characters",
            "maxlength": "Phone number must be 11 characters"
        }
    )

    @validates_schema
    def validate_passwords(self, data, **kwargs):
        """Ensure repeatPassword matches password."""
        if data.get("password") != data.get("repeatPassword"):
            raise ValidationError({"repeatPassword": "Passwords must match."})


class LoginSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required", "invalid": "Invalid Email format"}
    )
    password = fields.String(
        required=True,
        error_messages={"required": "Password is required"}
    )
    
    
    
    


login_schema = LoginSchema()
registration_schema = RegistrationSchema()