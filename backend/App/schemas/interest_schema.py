from App import ma
from App.models.interest import Interest

class InterestSchema(ma.SQLAlchemySchema):
    """Schema for serializing Interest objects"""
    class Meta:
        model = Interest
        load_instance = True
    
    id = ma.auto_field()
    event_id = ma.auto_field()
    user_id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
    attendees_count = ma.auto_field()
    created_at = ma.auto_field()

interest_schema = InterestSchema()
interests_schema = InterestSchema(many=True)
