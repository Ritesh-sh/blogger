"""
Keyword extraction service using KeyBERT.
Extracts important keywords and phrases from text using NLP.
"""
from keybert import KeyBERT
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize KeyBERT model (lazy loading)
_keybert_model = None


def get_keybert_model():
    """Get or initialize the KeyBERT model."""
    global _keybert_model
    if _keybert_model is None:
        logger.info("Loading KeyBERT model...")
        _keybert_model = KeyBERT()
        logger.info("KeyBERT model loaded successfully")
    return _keybert_model


class KeywordExtractor:
    """Extracts keywords and key phrases from text using KeyBERT."""
    
    @staticmethod
    def extract_keywords(text, top_n=10, use_ngrams=True):
        """
        Extract top keywords from text.
        
        Args:
            text (str): Text to extract keywords from
            top_n (int): Number of top keywords to extract
            use_ngrams (bool): Whether to include phrases (bigrams/trigrams)
            
        Returns:
            list: List of tuples (keyword, score)
        """
        if not text or len(text) < 50:
            logger.warning("Text too short for keyword extraction")
            return []
        
        try:
            model = get_keybert_model()
            
            # Set n-gram range (1-3 words if ngrams, else single words only)
            keyphrase_ngram_range = (1, 3) if use_ngrams else (1, 1)
            
            # Extract keywords
            keywords = model.extract_keywords(
                text,
                keyphrase_ngram_range=keyphrase_ngram_range,
                stop_words='english',
                top_n=top_n,
                use_mmr=True,  # Use Maximal Marginal Relevance for diversity
                diversity=0.5
            )
            
            logger.info(f"Extracted {len(keywords)} keywords from text")
            return keywords
            
        except Exception as e:
            logger.error(f"Keyword extraction failed: {str(e)}")
            return []
    
    @staticmethod
    def extract_keywords_list(text, top_n=10, use_ngrams=True):
        """
        Extract keywords as a simple list (without scores).
        
        Args:
            text (str): Text to extract keywords from
            top_n (int): Number of top keywords to extract
            use_ngrams (bool): Whether to include phrases
            
        Returns:
            list: List of keyword strings
        """
        keywords_with_scores = KeywordExtractor.extract_keywords(text, top_n, use_ngrams)
        return [keyword for keyword, score in keywords_with_scores]
    
    @staticmethod
    def extract_keywords_by_category(text):
        """
        Extract keywords organized by category (single words vs phrases).
        
        Args:
            text (str): Text to extract keywords from
            
        Returns:
            dict: Dictionary with 'single_words' and 'phrases' lists
        """
        try:
            # Extract all keywords with phrases
            all_keywords = KeywordExtractor.extract_keywords_list(text, top_n=15, use_ngrams=True)
            
            # Separate single words and phrases
            single_words = [kw for kw in all_keywords if ' ' not in kw]
            phrases = [kw for kw in all_keywords if ' ' in kw]
            
            return {
                'single_words': single_words[:8],
                'phrases': phrases[:7],
                'all': all_keywords[:10]
            }
            
        except Exception as e:
            logger.error(f"Categorized keyword extraction failed: {str(e)}")
            return {
                'single_words': [],
                'phrases': [],
                'all': []
            }
