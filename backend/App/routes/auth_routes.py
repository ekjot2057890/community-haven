from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from App import mongo
from App.utils.mongo_utils import (
    serialize_id, get_user_by_email, get_user_by_username,
    create_user, check_password, get_user_by_id
)
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Check if required fields are provided
    if not all(k in data for k in ('username', 'email', 'password', 'full_name')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if username or email already exists
    if get_user_by_username(data['username']):
        return jsonify({'error': 'Username already exists'}), 409
        
    if get_user_by_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create new user
    user = create_user(data)
    
    return jsonify({
        'message': 'User registered successfully',
        'user': serialize_id(user)
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT token"""
    data = request.get_json()
    
    # Check if required fields are provided
    if not all(k in data for k in ('email', 'password')):
        return jsonify({'error': 'Missing email or password'}), 400
    
    # Find user by email
    user = get_user_by_email(data['email'])
    
    # Check if user exists and password is correct
    if not user or not check_password(user, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Check if user is banned
    if user.get('is_banned', False):
        return jsonify({'error': 'Your account has been banned'}), 403
    
    # Create access token
    access_token = create_access_token(
        identity=str(user['_id']),
        additional_claims={
            'is_admin': user.get('is_admin', False),
            'is_verified_organizer': user.get('is_verified_organizer', False)
        },
        expires_delta=timedelta(days=1)
    )
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': serialize_id(user)
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    current_user_id = get_jwt_identity()
    user = get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    return jsonify(serialize_id(user)), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    current_user_id = get_jwt_identity()
    user = get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update fields if provided
    if 'full_name' in data:
        mongo.db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'full_name': data['full_name']}}
        )
    if 'phone' in data:
        mongo.db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'phone': data['phone']}}
        )
    if 'location' in data:
        mongo.db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'location': data['location']}}
        )
    if 'password' in data:
        hashed_password = generate_password_hash(data['password'])
        mongo.db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'password_hash': hashed_password}}
        )
    
    # Get updated user data
    updated_user = get_user_by_id(current_user_id)
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': serialize_id(updated_user)
    }), 200
