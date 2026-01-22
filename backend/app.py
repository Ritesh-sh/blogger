"""
Main Flask application entry point.
Sets up the Flask app, configures middleware, and registers routes.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config
from utils.logger import setup_logger
from utils.db import init_db

# Import routes
from routes.auth import auth_bp
from routes.blog import blog_bp

logger = setup_logger(__name__)


def create_app(config_name='default'):
    """
    Application factory pattern.
    Creates and configures the Flask application.
    
    Args:
        config_name (str): Configuration name ('development', 'production', or 'default')
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(blog_bp, url_prefix='/api/blog')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint for monitoring."""
        return jsonify({
            'status': 'healthy',
            'message': 'Blog Generator API is running'
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    logger.info(f"Flask app created with config: {config_name}")
    return app


if __name__ == '__main__':
    # Create app with development configuration
    app = create_app('development')
    
    # Run the application
    logger.info(f"Starting Flask server on {app.config['HOST']}:{app.config['PORT']}")
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
