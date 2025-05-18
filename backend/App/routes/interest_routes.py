from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId
from app import mongo
from app.utils.mongo_utils import (
    serialize_id, serialize_ids, get_user_by_id,
    get_event_by_id, get_interest, create_interest, delete_interest
)
from app.services.notification_service import schedule_event_reminder

interest_bp = Blueprint('interest', __name__)

@interest_bp.route('/events/<event_id>/interest', methods=['POST'])
@jwt_required()
def express_interest(event_id):
    """Express interest in attending an event"""
    current_user_id = get_jwt_identity()
    user = get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if event exists and is approved
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    if event.get('status') != 'approved':
        return jsonify({'error': 'Cannot express interest in an unapproved event'}), 400
    
    # Check if user already expressed interest
    existing_interest = get_interest(event_id, current_user_id)
    if existing_interest:
        return jsonify({'error': 'You have already expressed interest in this event'}), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create interest data
    interest_data = {
        'event_id': event_id,
        'user_id': current_user_id,
        'name': data['name'],
        'email': data['email'],
        'phone': data.get('phone', user.get('phone', '')),
        'attendees_count': data.get('attendees_count', 1)
    }
    
    # Create new interest record
    new_interest = create_interest(interest_data)
    
    # Schedule reminder for this user
    schedule_event_reminder(event_id, current_user_id)
    
    return jsonify({
        'message': 'Interest expressed successfully',
        'interest': serialize_id(new_interest)
    }), 201

@interest_bp.route('/events/<event_id>/interests', methods=['GET'])
@jwt_required()
def get_interests(event_id):
    """Get all interests for an event (for organizers or admins)"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    
    # Check if event exists
    event = get_event_by_id(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    # Check if user is authorized to view interests
    if str(event.get('user_id')) != current_user_id and not is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        interests = list(mongo.db.interests.find({"event_id": ObjectId(event_id)}))
        return jsonify(serialize_ids(interests)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interest_bp.route('/my-interests', methods=['GET'])
@jwt_required()
def get_my_interests():
    """Get events the current user is interested in"""
    current_user_id = get_jwt_identity()
    
    try:
        # Find all interests for this user
        interests = list(mongo.db.interests.find({"user_id": ObjectId(current_user_id)}))
        
        # Get the associated events
        event_ids = [interest.get('event_id') for interest in interests]
        events = list(mongo.db.events.find({"_id": {"$in": event_ids}}))
        
        return jsonify(serialize_ids(events)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interest_bp.route('/events/<event_id>/interest', methods=['DELETE'])
@jwt_required()
def remove_interest(event_id):
    """Remove interest in an event"""
    current_user_id = get_jwt_identity()
    
    # Check if interest exists
    existing_interest = get_interest(event_id, current_user_id)
    if not existing_interest:
        return jsonify({'error': 'Interest record not found'}), 404
    
    # Delete the interest
    if delete_interest(event_id, current_user_id):
        return jsonify({'message': 'Interest removed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to remove interest'}), 500
