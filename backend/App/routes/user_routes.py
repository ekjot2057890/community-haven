from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId
from app import mongo
from app.utils.mongo_utils import (
    serialize_id, serialize_ids, get_user_by_id
)

user_bp = Blueprint('user', __name__)

@user_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user details"""
    current_user_id = get_jwt_identity()
    user = get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(serialize_id(user)), 200

@user_bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get a specific user's details (admin only or self)"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    
    # Only allow admins or the user themselves to access user details
    if not is_admin and current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(serialize_id(user)), 200

@user_bp.route('/users/search', methods=['GET'])
@jwt_required()
def search_users():
    """Search for users by username or email (admin only)"""
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)
    
    if not is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    query = request.args.get('q', '')
    if not query or len(query) < 3:
        return jsonify({'error': 'Search query must be at least 3 characters'}), 400
    
    try:
        users = list(mongo.db.users.find({
            "$or": [
                {"username": {"$regex": query, "$options": "i"}},
                {"email": {"$regex": query, "$options": "i"}},
                {"full_name": {"$regex": query, "$options": "i"}}
            ]
        }))
        return jsonify(serialize_ids(users)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current user details"""
    current_user_id = get_jwt_identity()
    user = get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    update_data = {}
    
    # Update fields if provided
    if 'full_name' in data:
        update_data['full_name'] = data['full_name']
    if 'phone' in data:
        update_data['phone'] = data['phone']
    if 'location' in data:
        update_data['location'] = data['location']
    
    # Update the user
    result = mongo.db.users.update_one(
        {"_id": ObjectId(current_user_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0 and update_data:
        return jsonify({'error': 'Failed to update user'}), 500
    
    # Get updated user
    updated_user = get_user_by_id(current_user_id)
    
    return jsonify({
        'message': 'User updated successfully',
        'user': serialize_id(updated_user)
    }), 200
