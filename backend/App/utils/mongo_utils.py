from bson import ObjectId
from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from App import mongo

def serialize_id(obj):
    """Convert MongoDB ObjectId to string for JSON serialization"""
    if obj and '_id' in obj:
        obj['id'] = str(obj['_id'])
        del obj['_id']
    return obj

def serialize_ids(objects):
    """Convert MongoDB ObjectIds to strings for a list of objects"""
    return [serialize_id(obj) for obj in objects]

def get_user_by_id(user_id):
    """Get a user by ID"""
    try:
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})
    except:
        return None

def get_user_by_email(email):
    """Get a user by email"""
    return mongo.db.users.find_one({"email": email})

def get_user_by_username(username):
    """Get a user by username"""
    return mongo.db.users.find_one({"username": username})

def create_user(user_data):
    """Create a new user"""
    user = {
        "username": user_data["username"],
        "email": user_data["email"],
        "password_hash": generate_password_hash(user_data["password"]),
        "full_name": user_data.get("full_name", ""),
        "phone": user_data.get("phone", ""),
        "location": user_data.get("location", ""),
        "is_verified_organizer": False,
        "is_admin": False,
        "is_banned": False,
        "created_at": datetime.utcnow()
    }
    result = mongo.db.users.insert_one(user)
    user["_id"] = result.inserted_id
    return user

def check_password(user, password):
    """Check if password matches user's password hash"""
    return check_password_hash(user["password_hash"], password)

def get_event_by_id(event_id):
    """Get an event by ID"""
    try:
        return mongo.db.events.find_one({"_id": ObjectId(event_id)})
    except:
        return None

def create_event(event_data, user_id):
    """Create a new event"""
    # Convert coordinates to GeoJSON format
    if "latitude" in event_data and "longitude" in event_data:
        location = {
            "type": "Point",
            "coordinates": [event_data["longitude"], event_data["latitude"]]
        }
    else:
        location = None
    
    event = {
        "title": event_data["title"],
        "description": event_data["description"],
        "category": event_data["category"],
        "address": event_data["location"],
        "location": location,
        "start_date": datetime.fromisoformat(event_data["start_date"]),
        "end_date": datetime.fromisoformat(event_data["end_date"]),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "status": event_data.get("status", "pending"),
        "user_id": ObjectId(user_id)
    }
    result = mongo.db.events.insert_one(event)
    event["_id"] = result.inserted_id
    return event

def update_event(event_id, event_data):
    """Update an existing event"""
    try:
        event_id_obj = ObjectId(event_id)
    except:
        return None
    
    update_fields = {}
    
    # Update basic fields if provided
    for field in ["title", "description", "category", "status"]:
        if field in event_data:
            update_fields[field] = event_data[field]
    
    # Update address if provided
    if "location" in event_data:
        update_fields["address"] = event_data["location"]
    
    # Convert coordinates to GeoJSON format if provided
    if "latitude" in event_data and "longitude" in event_data:
        update_fields["location"] = {
            "type": "Point",
            "coordinates": [event_data["longitude"], event_data["latitude"]]
        }
    
    # Update dates if provided
    if "start_date" in event_data:
        update_fields["start_date"] = datetime.fromisoformat(event_data["start_date"])
    if "end_date" in event_data:
        update_fields["end_date"] = datetime.fromisoformat(event_data["end_date"])
    
    # Set updated timestamp
    update_fields["updated_at"] = datetime.utcnow()
    
    # Update the event
    result = mongo.db.events.update_one(
        {"_id": event_id_obj},
        {"$set": update_fields}
    )
    
    if result.modified_count > 0:
        return mongo.db.events.find_one({"_id": event_id_obj})
    return None

def create_interest(interest_data):
    """Create a new interest record"""
    interest = {
        "event_id": ObjectId(interest_data["event_id"]),
        "user_id": ObjectId(interest_data["user_id"]),
        "name": interest_data["name"],
        "email": interest_data["email"],
        "phone": interest_data.get("phone", ""),
        "attendees_count": interest_data.get("attendees_count", 1),
        "created_at": datetime.utcnow()
    }
    result = mongo.db.interests.insert_one(interest)
    interest["_id"] = result.inserted_id
    return interest

def get_interest(event_id, user_id):
    """Get interest record for a specific event and user"""
    try:
        return mongo.db.interests.find_one({
            "event_id": ObjectId(event_id),
            "user_id": ObjectId(user_id)
        })
    except:
        return None

def delete_interest(event_id, user_id):
    """Delete interest record for a specific event and user"""
    try:
        result = mongo.db.interests.delete_one({
            "event_id": ObjectId(event_id),
            "user_id": ObjectId(user_id)
        })
        return result.deleted_count > 0
    except:
        return False
