from App.models import db
from datetime import datetime

class Interest(db.Model):
    """Model for storing user interest in events"""
    __tablename__ = 'interests'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    attendees_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert interest object to dictionary"""
        return {
            'id': self.id,
            'event_id': self.event_id,
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'attendees_count': self.attendees_count,
            'created_at': self.created_at.isoformat()
        }
