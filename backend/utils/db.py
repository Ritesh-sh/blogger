"""
Database connection and initialization module.
Handles MongoDB connection setup and provides database instance.
"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Global database client and database instance
_client = None
_db = None


def init_db(app):
    """
    Initialize MongoDB connection.
    
    Args:
        app (Flask): Flask application instance
        
    Returns:
        Database: MongoDB database instance
    """
    global _client, _db
    
    try:
        # Create MongoDB client
        mongodb_uri = app.config['MONGODB_URI']
        _client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        
        # Test connection
        _client.admin.command('ping')
        
        # Get database
        db_name = app.config['MONGODB_DB_NAME']
        _db = _client[db_name]
        
        # Create indexes for better performance
        _create_indexes()
        
        logger.info(f"Successfully connected to MongoDB database: {db_name}")
        return _db
        
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise


def get_db():
    """
    Get the database instance.
    
    Returns:
        Database: MongoDB database instance
    """
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db first.")
    return _db


def _create_indexes():
    """Create database indexes for better query performance."""
    try:
        # Users collection indexes
        _db.users.create_index("email", unique=True)
        _db.users.create_index("created_at")
        
        # Blog history collection indexes
        _db.blog_history.create_index("user_id")
        _db.blog_history.create_index("created_at")
        _db.blog_history.create_index([("user_id", 1), ("created_at", -1)])
        
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.warning(f"Error creating indexes: {str(e)}")


def close_db():
    """Close database connection."""
    global _client
    if _client:
        _client.close()
        logger.info("Database connection closed")
