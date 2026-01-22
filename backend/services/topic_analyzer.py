"""
Topic analyzer service.
Analyzes text to understand main topics and intent.
"""
from collections import Counter
import re
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TopicAnalyzer:
    """Analyzes text to extract topics and understand intent."""
    
    @staticmethod
    def analyze_topics(text, keywords):
        """
        Analyze text to understand main topics.
        
        Args:
            text (str): Text to analyze
            keywords (list): Extracted keywords
            
        Returns:
            dict: Analysis results containing topics, intent, and summary
        """
        try:
            # Get text statistics
            word_count = len(text.split())
            sentence_count = len(re.split(r'[.!?]+', text))
            
            # Determine content type/intent
            intent = TopicAnalyzer._determine_intent(text, keywords)
            
            # Generate topic summary
            topic_summary = TopicAnalyzer._generate_topic_summary(keywords)
            
            # Get content category
            category = TopicAnalyzer._categorize_content(keywords)
            
            result = {
                'intent': intent,
                'topic_summary': topic_summary,
                'category': category,
                'word_count': word_count,
                'sentence_count': sentence_count,
                'main_topics': keywords[:5] if len(keywords) > 5 else keywords
            }
            
            logger.info(f"Topic analysis complete: {result['category']} - {result['intent']}")
            return result
            
        except Exception as e:
            logger.error(f"Topic analysis failed: {str(e)}")
            return {
                'intent': 'informational',
                'topic_summary': 'General content',
                'category': 'general',
                'word_count': 0,
                'sentence_count': 0,
                'main_topics': []
            }
    
    @staticmethod
    def _determine_intent(text, keywords):
        """
        Determine the intent of the content.
        
        Args:
            text (str): Text to analyze
            keywords (list): Extracted keywords
            
        Returns:
            str: Intent type (informational, commercial, educational, etc.)
        """
        text_lower = text.lower()
        
        # Check for commercial intent
        commercial_words = ['buy', 'purchase', 'price', 'cost', 'deal', 'discount', 'sale']
        if any(word in text_lower for word in commercial_words):
            return 'commercial'
        
        # Check for educational intent
        educational_words = ['learn', 'tutorial', 'guide', 'how to', 'course', 'training']
        if any(word in text_lower for word in educational_words):
            return 'educational'
        
        # Check for review/comparison intent
        review_words = ['review', 'comparison', 'vs', 'versus', 'best', 'top']
        if any(word in text_lower for word in review_words):
            return 'review'
        
        # Default to informational
        return 'informational'
    
    @staticmethod
    def _generate_topic_summary(keywords):
        """
        Generate a natural language summary of topics.
        
        Args:
            keywords (list): List of keywords
            
        Returns:
            str: Topic summary
        """
        if not keywords:
            return "General content"
        
        if len(keywords) == 1:
            return f"Content about {keywords[0]}"
        elif len(keywords) == 2:
            return f"Content about {keywords[0]} and {keywords[1]}"
        else:
            top_keywords = keywords[:3]
            return f"Content covering {', '.join(top_keywords[:-1])}, and {top_keywords[-1]}"
    
    @staticmethod
    def _categorize_content(keywords):
        """
        Categorize content based on keywords.
        
        Args:
            keywords (list): List of keywords
            
        Returns:
            str: Content category
        """
        # Combine all keywords into a single string
        keywords_text = ' '.join(keywords).lower()
        
        # Technology category
        tech_terms = ['software', 'technology', 'programming', 'code', 'app', 'digital', 'web', 'api']
        if any(term in keywords_text for term in tech_terms):
            return 'technology'
        
        # Business category
        business_terms = ['business', 'marketing', 'sales', 'strategy', 'management', 'enterprise']
        if any(term in keywords_text for term in business_terms):
            return 'business'
        
        # Health category
        health_terms = ['health', 'medical', 'wellness', 'fitness', 'nutrition', 'healthcare']
        if any(term in keywords_text for term in health_terms):
            return 'health'
        
        # Education category
        education_terms = ['education', 'learning', 'course', 'training', 'teaching', 'student']
        if any(term in keywords_text for term in education_terms):
            return 'education'
        
        # Finance category
        finance_terms = ['finance', 'money', 'investment', 'banking', 'insurance', 'credit']
        if any(term in keywords_text for term in finance_terms):
            return 'finance'
        
        # Default category
        return 'general'
