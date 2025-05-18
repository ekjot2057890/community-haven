from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId
from functools import wraps
from App import mongo
from App.utils.mongo_utils import (
    serialize_id, serialize_ids, get_user_by_id, get_event_by_id
)
from App.services.notification_service import send_event_status_notification

admin_bp = Blueprint('admin', __name__)

# Admin authorization decorator
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return fn(*args, **kwargs)
    
    return wrapper

@admin_bp.route('/events/pending', methods=['GET'])
@admin_required
def pending_events():
    """Get all pending events for admin approval"""
    events = list(mongo.db.events.find({"status": "pending"}).sort("created_at", 1))
    
    return jsonify(serialize_ids(events)), 200

@admin_bp.route('/events/<event_id>/approve', methods=['PUT'])
@admin_required
def approve_event(event_id):
    """Approve a pending event"""
    event = get_event_by_id(event_id)
    
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    if event.get('status') != 'pending':
        return jsonify({'error': 'Event is not pending approval'}), 400
    
    # Update event status
    result = mongo.db.events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"status": "approved"}}
    )
    
    if result.modified_count == 0:
        return jsonify({'error': 'Failed to approve event'}), 500
    
    # Get updated event
    updated_event = get_event_by_id(event_id)
    
    # Notify the organizer
    send_event_status_notification(event_id, 'approved')
    
    return jsonify({
        'message': 'Event approved successfully',
        'event': serialize_id(updated_event)
    }), 200

@admin_bp.route('/events/<event_id>/reject', methods=['PUT'])
@admin_required
def reject_event(event_id):
    """Reject a pending event"""
    event = get_event_by_id(event_id)
    
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    
    if event.get('status') != 'pending':
        return jsonify({'error': 'Event is not pending approval'}), 400
    
    # Get rejection reason
    data = request.get_json()
    reason = data.get('reason', 'No reason provided')
    
    # Update event status
    result = mongo.db.events.update_one(
        {"_id": ObjectId(event_id)},
        {"$set": {"status": "rejected", "rejection_reason": reason}}
    )
    
    if result.modified_count == 0:
        return jsonify({'error': 'Failed to reject event'}), 500
    
    # Get updated event
    updated_event = get_event_by_id(event_id)
    
    # Notify the organizer with reason
    send_event_status_notification(event_id, 'rejected', reason)
    
    return jsonify({
        'message': 'Event rejected successfully',
        'event': serialize_id(updated_event)
    }), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users (admin only)"""
    users = list
