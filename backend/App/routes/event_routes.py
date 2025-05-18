from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId
from datetime import datetime
from App import mongo
from App.utils.mongo_utils import (
    serialize_id, serialize_ids, get_user_by_id, 
    get_event_by_id, create_event, update_event
)
from App.services.location_service import geocode_address
from App.services.notification_service import send_event_update_notification

event_bp = Blueprint('event', __name__)

@event_bp.route('/events', methods=['GET'])
def get_events():
    """Get all approved events with optional filtering"""
    # Get query parameters
    category = request.args.get('category')
    location = request.args.get('location')
    start_date = request.args.get('start_date')
    
    # Base query for approved events
    query = {"status": "approved"}
    
    # Apply filters if provided
    if category:
        query["category"] = category
    if location:
        query["address"] = {"$regex": location, "$options": "i"}
    if start_date:
        try:
            date_obj = datetime.fromisoformat(start_date)
            query["start_date"] = {"$gte": date_obj}
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
    
    # Execute query and return results
    events = list(mongo.db.events.find(query).sort("start_date", 1))
    return jsonify(serialize_ids(events)), 200

@event_bp.route('/events', methods=['POST'])
@jwt_required()
def create_new_event():
    """Create a new event"""
    current_user_id = get_jwt_identity()
    user = get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if user is banned
    if user.get('is_banned', False):
        return jsonify({'error': 'You are banned from creating events'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'category', 'location', 'start_date', 'end_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Parse dates
    try:
        start_date = datetime.fromisoformat(data['start_date'])
        end_date = datetime.fromisoformat(data['end_date'])
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Validate date logic
    if start_date >= end_date:
        return jsonify({'error': 'End date must be after start date'}), 400
    
    # Get coordinates from address
    try:
        lat, lng = geocode_address(data['location'])
        data['latitude'] = lat
        data['longitude'] = lng
    except Exception as e:
        # If geocoding fails, continue without coordinates
        pass
    
    # Set status based on user role
    if user.get('is_verified_organizer', False):
        data['status'] = 'approved'
    else:
        data['status'] = 'pending'
    
    # Create new event
    event = create_event(data, current_user_id)
    
    return jsonify({
        'message': 'Event created successfully' if user.get('is_verified_organizer', False) else 'Event submitted for approval',
        'event': serialize_id(event)
    }), 201

@event_bp.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    """Get a specific event by ID"""
    event = get_event_by_id(event_id)
    
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    # Only return approved events unless user is admin or the organizer
    if event.get('status') != 'approved':
        # Check if user is authenticated
        try:
            claims = get_jwt()
            current_user_id = get_jwt_identity()
            is_admin = claims.get('is_admin', False)
            
            # If not admin or organizer, don't show the event
            if not is_admin and str(event.get('user_id')) != current_user_id:
                return jsonify({'error': 'Event not found'}), 404
        except:
            # If not authenticated, don't show non-approved events
            return jsonify({'error': 'Event not found'}), 404
    
    return jsonify(serialize_id(event)), 200

@event_bp.route('/events/<event_id>', methods=['PUT'])
@jwt_required()
def update_existing_event(event_id):
    """Update an existing event"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    
    event = get_event_by_id(event_id)
    
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    # Check if user is authorized to update the event
    if str(event.get('user_id')) != current_user_id and not is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    old_location = event.get('address')
    old_start_date = event.get('start_date')
    
    # Get coordinates if location changed
    if 'location' in data and data['location'] != old_location:
        try:
            lat, lng = geocode_address(data['location'])
            data['latitude'] = lat
            data['longitude'] = lng
        except:
            pass
    
    # If non-admin user makes significant changes, reset approval status
    user = get_user_by_id(current_user_id)
    if not is_admin and not user.get('is_verified_organizer', False):
        if ('location' in data and data['location'] != old_location) or \
           ('start_date' in data and datetime.fromisoformat(data['start_date']) != old_start_date):
            data['status'] = 'pending'
    
    # Update the event
    updated_event = update_event(event_id, data)
    
    if not updated_event:
        return jsonify({'error': 'Failed to update event'}), 500
    
    # Send notifications if event details changed
    if ('location' in data and data['location'] != old_location) or \
       ('start_date' in data and datetime.fromisoformat(data['start_date']) != old_start_date):
        send_event_update_notification(event_id, 'update')
    
    return jsonify({
        'message': 'Event updated successfully',
        'event': serialize_id(updated_event)
    }), 200

@event_bp.route('/events/<event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    """Delete an event"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    
    event = get_event_by_id(event_id)
    
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    # Check if user is authorized to delete the event
    if str(event.get('user_id')) != current_user_id and not is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Send cancellation notification before deleting
    send_event_update_notification(event_id, 'cancel')
    
    # Delete the event
    mongo.db.events.delete_one({'_id': ObjectId(event_id)})
    
    return jsonify({'message': 'Event deleted successfully'}), 200

@event_bp.route('/my-events', methods=['GET'])
@jwt_required()
def get_my_events():
    """Get events created by the current user"""
    current_user_id = get_jwt_identity()
    
    events = list(mongo.db.events.find({"user_id": ObjectId(current_user_id)}).sort("created_at", -1))
    
    return jsonify(serialize_ids(events)), 200
