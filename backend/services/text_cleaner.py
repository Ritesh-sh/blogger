"""
Text cleaning service.
Cleans and normalizes extracted text content.
"""
import re
from utils.logger import setup_logger

logger = setup_logger(__name__)


class TextCleaner:
    """Cleans and normalizes text content."""
    
    @staticmethod
    def clean_text(text, max_length=None):
        """
        Clean and normalize text content.
        
        Args:
            text (str): Raw text to clean
            max_length (int, optional): Maximum length to truncate to
            
        Returns:
            str: Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove multiple consecutive dots
        text = re.sub(r'\.{3,}', '...', text)
        
        # Remove URLs from text
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\-\'"()&]', '', text)
        
        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace("'", "'").replace("'", "'")
        
        # Remove multiple spaces again
        text = re.sub(r'\s+', ' ', text)
        
        # Trim whitespace
        text = text.strip()
        
        # Truncate if needed
        if max_length and len(text) > max_length:
            text = text[:max_length]
            # Try to end at a word boundary
            last_space = text.rfind(' ')
            if last_space > max_length * 0.9:
                text = text[:last_space]
            text += '...'
        
        logger.debug(f"Cleaned text: {len(text)} characters")
        return text
    
    @staticmethod
    def remove_stop_words(text, language='english'):
        """
        Remove common stop words from text.
        
        Args:
            text (str): Text to process
            language (str): Language for stop words
            
        Returns:
            str: Text with stop words removed
        """
        # Simple English stop words list
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'this', 'but', 'they', 'have', 'had',
            'what', 'when', 'where', 'who', 'which', 'why', 'how'
        }
        
        # Split into words
        words = text.split()
        
        # Filter out stop words
        filtered_words = [word for word in words if word.lower() not in stop_words]
        
        return ' '.join(filtered_words)
    
    @staticmethod
    def extract_sentences(text, min_length=10):
        """
        Extract valid sentences from text.
        
        Args:
            text (str): Text to process
            min_length (int): Minimum sentence length
            
        Returns:
            list: List of sentences
        """
        # Split by sentence endings
        sentences = re.split(r'[.!?]+', text)
        
        # Filter and clean sentences
        valid_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) >= min_length:
                valid_sentences.append(sentence)
        
        return valid_sentences
    
    @staticmethod
    def normalize_whitespace(text):
        """
        Normalize whitespace in text.
        
        Args:
            text (str): Text to normalize
            
        Returns:
            str: Normalized text
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple newlines with double newline
        text = re.sub(r'\n+', '\n\n', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
