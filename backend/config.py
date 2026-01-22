"""
Configuration module for the Flask application.
Loads environment variables and provides configuration classes.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/blogger')
    MONGODB_DB_NAME = 'blogger'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Google Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = 'gemini-2.5-flash'  # Fast and cost-effective model
    
    # Content Extraction Configuration
    REQUEST_TIMEOUT = 10  # seconds
    MAX_CONTENT_LENGTH = 50000  # characters
    
    # Blog Generation Configuration
    MIN_BLOG_LENGTH = 500  # words
    MAX_BLOG_LENGTH = 3000  # words
    DEFAULT_BLOG_LENGTH = 1000  # words
    
    # Server Configuration
   # HOST = os.getenv('HOST', '0.0.0.0')
    #PORT = int(os.getenv('PORT', 5000))


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
