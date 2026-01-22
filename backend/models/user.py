"""
User model for MongoDB.
Handles user data and authentication.
"""
from datetime import datetime
from bson import ObjectId
import bcrypt
from utils.db import get_db
from utils.logger import setup_logger

logger = setup_logger(__name__)


class User:
    """User model for authentication and user management."""
    
    collection_name = 'users'
    
    @staticmethod
    def create_user(email, password):
        """
        Create a new user with hashed password.
        
        Args:
            email (str): User's email address
            password (str): Plain text password
            
        Returns:
            dict: Created user document (without password)
            
        Raises:
            ValueError: If user already exists
        """
        db = get_db()
        
        # Check if user already exists
        if db[User.collection_name].find_one({'email': email}):
            raise ValueError("User with this email already exists")
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user document
        user_doc = {
            'email': email,
            'password_hash': password_hash,
            'created_at': datetime.utcnow()
        }
        
        # Insert into database
        result = db[User.collection_name].insert_one(user_doc)
        
        # Return user without password
        user_doc['_id'] = result.inserted_id
        user_doc.pop('password_hash')
        
        logger.info(f"User created: {email}")
        return user_doc
    
    @staticmethod
    def find_by_email(email):
        """
        Find a user by email.
        
        Args:
            email (str): User's email address
            
        Returns:
            dict or None: User document if found, None otherwise
        """
        db = get_db()
        return db[User.collection_name].find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        """
        Find a user by ID.
        
        Args:
            user_id (str): User's ID
            
        Returns:
            dict or None: User document if found, None otherwise
        """
        db = get_db()
        try:
            return db[User.collection_name].find_one({'_id': ObjectId(user_id)})
        except Exception:
            return None
    
    @staticmethod
    def verify_password(email, password):
        """
        Verify user password.
        
        Args:
            email (str): User's email address
            password (str): Plain text password to verify
            
        Returns:
            dict or None: User document (without password) if valid, None otherwise
        """
        user = User.find_by_email(email)
        
        if not user:
            return None
        
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            # Return user without password
            user.pop('password_hash')
            logger.info(f"User authenticated: {email}")
            return user
        
        return None
    
    @staticmethod
    def to_dict(user_doc):
        """
        Convert user document to dictionary (safe for API response).
        
        Args:
            user_doc (dict): User document from database
            
        Returns:
            dict: Safe user data for API response
        """
        if not user_doc:
            return None
        
        return {
            'id': str(user_doc['_id']),
            'email': user_doc['email'],
            'created_at': user_doc['created_at'].isoformat()
        }
