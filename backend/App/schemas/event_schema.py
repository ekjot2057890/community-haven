from app import ma
from app.models.event import Event

class EventSchema(ma.SQLAlchemySchema):
    """Schema for serializing Event objects"""
    class Meta:
        model = Event
        load_instance = True
    
    id = ma.auto_field()
    title = ma.auto_field()
    description = ma.auto_field()
    category = ma.auto_field()
    location = ma.auto_field()
    latitude = ma.auto_field()
    longitude = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    created_at = ma.auto_field()
    updated_at = ma.auto_field()
    status = ma.auto_field()
    user_id = ma.auto_field()

event_schema = EventSchema()
events_schema = EventSchema(many=True)
