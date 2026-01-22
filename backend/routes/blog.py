"""
Blog generation routes.
Main API endpoints for blog generation and history management.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.blog_history import BlogHistory
from services.url_validator import URLValidator
from services.content_extractor import ContentExtractor
from services.text_cleaner import TextCleaner
from services.keyword_extractor import KeywordExtractor
from services.topic_analyzer import TopicAnalyzer
from services.prompt_builder import PromptBuilder
from services.blog_generator import BlogGenerator
from services.seo_postprocessor import SEOPostProcessor
from utils.logger import setup_logger

logger = setup_logger(__name__)

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/generate', methods=['POST'])
@jwt_required()
def generate_blog():
    """
    Generate a blog post from a website URL.
    
    Request Body:
        {
            "url": "https://example.com",
            "length": 1000,  # Optional, default 1000
            "tone": "professional",  # Optional, default "professional"
            "include_cta": true  # Optional, default true
        }
    
    Returns:
        JSON response with generated blog content
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data or 'url' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'URL is required'
            }), 400
        
        url = data['url'].strip()
        blog_length = data.get('length', 1000)
        tone = data.get('tone', 'professional')
        include_cta = data.get('include_cta', True)
        
        # Validate blog length
        if blog_length < 500 or blog_length > 3000:
            return jsonify({
                'error': 'Invalid length',
                'message': 'Blog length must be between 500 and 3000 words'
            }), 400
        
        # Validate tone
        valid_tones = ['professional', 'casual', 'technical', 'persuasive', 'educational']
        if tone not in valid_tones:
            return jsonify({
                'error': 'Invalid tone',
                'message': f'Tone must be one of: {", ".join(valid_tones)}'
            }), 400
        
        logger.info(f"Starting blog generation for URL: {url}")
        
        # Step 1: Validate URL
        logger.info("Step 1: Validating URL...")
        is_valid, validation_message = URLValidator.validate(url)
        if not is_valid:
            return jsonify({
                'error': 'Invalid URL',
                'message': validation_message
            }), 400
        
        # Step 2: Extract content from URL
        logger.info("Step 2: Extracting content from URL...")
        try:
            website_data = ContentExtractor.extract_content(url)
        except Exception as e:
            return jsonify({
                'error': 'Content extraction failed',
                'message': str(e)
            }), 400
        
        # Step 3: Clean extracted text
        logger.info("Step 3: Cleaning extracted text...")
        cleaned_text = TextCleaner.clean_text(
            website_data['text'],
            max_length=50000  # Limit for processing
        )
        
        if len(cleaned_text) < 100:
            return jsonify({
                'error': 'Insufficient content',
                'message': 'The webpage does not contain enough meaningful content'
            }), 400
        
        # Step 4: Extract keywords using NLP
        logger.info("Step 4: Extracting keywords with NLP...")
        keywords = KeywordExtractor.extract_keywords_list(
            cleaned_text,
            top_n=15,
            use_ngrams=True
        )
        
        if not keywords:
            return jsonify({
                'error': 'Keyword extraction failed',
                'message': 'Could not extract meaningful keywords from content'
            }), 400
        
        # Step 5: Analyze topics and intent
        logger.info("Step 5: Analyzing topics and intent...")
        topic_analysis = TopicAnalyzer.analyze_topics(cleaned_text, keywords)
        
        # Step 6: Build optimized prompt
        logger.info("Step 6: Building optimized prompt...")
        blog_config = {
            'length': blog_length,
            'tone': tone,
            'include_cta': include_cta
        }
        prompt = PromptBuilder.build_blog_prompt(
            website_data,
            keywords,
            topic_analysis,
            blog_config
        )
        
        # Step 7: Generate blog using LLM
        logger.info("Step 7: Generating blog with LLM...")
        try:
            generated_blog = BlogGenerator.generate_with_retry(prompt)
        except Exception as e:
            return jsonify({
                'error': 'Blog generation failed',
                'message': str(e)
            }), 500
        
        # Step 8: Apply SEO post-processing
        logger.info("Step 8: Applying SEO optimizations...")
        processed_blog = SEOPostProcessor.process_blog(generated_blog, keywords)
        
        # Step 9: Save to database
        logger.info("Step 9: Saving to database...")
        blog_entry = BlogHistory.create_blog_entry(
            user_id=user_id,
            website_url=url,
            keywords=keywords,
            generated_blog=processed_blog['content'],
            blog_config=blog_config
        )
        
        logger.info(f"Blog generation complete! ID: {blog_entry['_id']}")
        
        # Return response
        return jsonify({
            'message': 'Blog generated successfully',
            'blog': {
                'id': str(blog_entry['_id']),
                'content': processed_blog['content'],
                'title': processed_blog['title'],
                'meta_description': processed_blog['meta_description'],
                'keywords': keywords,
                'word_count': processed_blog['word_count'],
                'reading_time': processed_blog['reading_time'],
                'website_url': url,
                'topic_analysis': topic_analysis
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in blog generation: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': 'An unexpected error occurred during blog generation'
        }), 500


@blog_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """
    Get user's blog generation history.
    
    Query Parameters:
        limit (int): Number of entries to return (default: 10)
        skip (int): Number of entries to skip (default: 0)
    
    Returns:
        JSON response with blog history
    """
    try:
        user_id = get_jwt_identity()
        
        # Get pagination parameters
        limit = request.args.get('limit', 10, type=int)
        skip = request.args.get('skip', 0, type=int)
        
        # Validate parameters
        if limit < 1 or limit > 50:
            limit = 10
        if skip < 0:
            skip = 0
        
        # Get history from database
        history = BlogHistory.get_user_history(user_id, limit, skip)
        total_count = BlogHistory.count_user_blogs(user_id)
        
        # Convert to API format
        history_list = [BlogHistory.to_dict(entry) for entry in history]
        
        return jsonify({
            'history': history_list,
            'total': total_count,
            'limit': limit,
            'skip': skip
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching history: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': 'An error occurred while fetching history'
        }), 500


@blog_bp.route('/history/<blog_id>', methods=['GET'])
@jwt_required()
def get_blog_by_id(blog_id):
    """
    Get a specific blog entry by ID.
    
    Path Parameters:
        blog_id (str): Blog entry ID
    
    Returns:
        JSON response with blog details
    """
    try:
        user_id = get_jwt_identity()
        
        # Get blog from database
        blog = BlogHistory.get_blog_by_id(blog_id, user_id)
        
        if not blog:
            return jsonify({
                'error': 'Not found',
                'message': 'Blog not found or you do not have access'
            }), 404
        
        return jsonify({
            'blog': BlogHistory.to_dict(blog)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching blog {blog_id}: {str(e)}")
        return jsonify({
            'error': 'Server error',
            'message': 'An error occurred while fetching the blog'
        }), 500


@blog_bp.route('/preview', methods=['POST'])
@jwt_required()
def preview_content():
    """
    Preview extracted content and keywords from a URL without generating blog.
    Useful for users to verify content before generating.
    
    Request Body:
        {
            "url": "https://example.com"
        }
    
    Returns:
        JSON response with extracted content preview and keywords
    """
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'URL is required'
            }), 400
        
        url = data['url'].strip()
        
        # Validate URL
        is_valid, validation_message = URLValidator.validate(url)
        if not is_valid:
            return jsonify({
                'error': 'Invalid URL',
                'message': validation_message
            }), 400
        
        # Extract content
        website_data = ContentExtractor.extract_content(url)
        
        # Clean text
        cleaned_text = TextCleaner.clean_text(website_data['text'], max_length=50000)
        
        # Extract keywords
        keywords = KeywordExtractor.extract_keywords_list(cleaned_text, top_n=10)
        
        # Get summary
        summary = ContentExtractor.get_summary(cleaned_text, max_length=300)
        
        return jsonify({
            'preview': {
                'title': website_data['title'],
                'description': website_data['description'],
                'summary': summary,
                'keywords': keywords,
                'word_count': len(cleaned_text.split()),
                'url': url
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Preview error: {str(e)}")
        return jsonify({
            'error': 'Preview failed',
            'message': str(e)
        }), 400
