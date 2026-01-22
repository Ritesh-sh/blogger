"""
Authentication routes for user signup and login.
Handles JWT token generation and validation.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from utils.logger import setup_logger

logger = setup_logger(__name__)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    User signup endpoint.
    Creates a new user account.
    
    Request Body:
        {
            "email": "user@example.com",
            "password": "securepassword"
        }
    
    Returns:
        JSON response with user data and JWT token
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Email and password are required'
            }), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({
                'error': 'Invalid email',
                'message': 'Please provide a valid email address'
            }), 400
        
        # Validate password length
        if len(password) < 6:
            return jsonify({
                'error': 'Weak password',
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        # Create user
        user = User.create_user(email, password)
        
        # Generate JWT token
        access_token = create_access_token(identity=str(user['_id']))
        
        return jsonify({
            'message': 'User created successfully',
            'user': User.to_dict(user),
            'access_token': access_token
        }), 201
        
    except ValueError as e:
        logger.warning(f"Signup failed: {str(e)}")
        return jsonify({
            'error': 'Signup failed',
            'message': str(e)
        }), 409
    except Exception as e:
        logger.error(f"Signup error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': 'An error occurred during signup'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint.
    Authenticates user and returns JWT token.
    
    Request Body:
        {
            "email": "user@example.com",
            "password": "securepassword"
        }
    
    Returns:
        JSON response with user data and JWT token
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Email and password are required'
            }), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # Verify user credentials
        user = User.verify_password(email, password)
        
        if not user:
            return jsonify({
                'error': 'Authentication failed',
                'message': 'Invalid email or password'
            }), 401
        
        # Generate JWT token
        access_token = create_access_token(identity=str(user['_id']))
        
        return jsonify({
            'message': 'Login successful',
            'user': User.to_dict(user),
            'access_token': access_token
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': 'An error occurred during login'
        }), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user.
    Requires valid JWT token.
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        JSON response with current user data
    """
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'User account no longer exists'
            }), 404
        
        return jsonify({
            'user': User.to_dict(user)
        }), 200
        
    except Exception as e:
        logger.error(f"Get user error: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': 'An error occurred while fetching user data'
        }), 500
