from app import ma
from app.models.user import User

class UserSchema(ma.SQLAlchemySchema):
    """Schema for serializing User objects"""
    class Meta:
        model = User
        load_instance = True
    
    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    full_name = ma.auto_field()
    phone = ma.auto_field()
    location = ma.auto_field()
    created_at = ma.auto_field()
    is_verified_organizer = ma.auto_field()
    is_admin = ma.auto_field()
    is_banned = ma.auto_field()

user_schema = UserSchema()
users_schema = UserSchema(many=True)
