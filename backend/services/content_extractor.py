"""
Content extraction service.
Extracts meaningful text content from web pages using Trafilatura.
"""
import requests
import trafilatura
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ContentExtractor:
    """Extracts clean text content from web pages."""
    
    @staticmethod
    def extract_content(url, timeout=10):
        """
        Extract main content from a web page.
        
        Args:
            url (str): URL to extract content from
            timeout (int): Request timeout in seconds
            
        Returns:
            dict: Dictionary containing extracted content
                {
                    'text': str,  # Main text content
                    'title': str,  # Page title
                    'description': str,  # Meta description
                    'author': str,  # Author if available
                    'date': str,  # Publication date if available
                    'url': str  # Original URL
                }
                
        Raises:
            Exception: If content extraction fails
        """
        try:
            # Fetch the web page
            response = requests.get(
                url,
                timeout=timeout,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            response.raise_for_status()
            
            # Extract content using Trafilatura
            downloaded = trafilatura.extract(
                response.content,
                include_comments=False,
                include_tables=False,
                favor_precision=True,
                with_metadata=True,
                output_format='json'
            )
            
            if not downloaded:
                raise ValueError("Could not extract content from the page")
            
            # Parse the JSON response
            import json
            content_data = json.loads(downloaded) if isinstance(downloaded, str) else downloaded
            
            # Extract and clean data
            result = {
                'text': content_data.get('text', '').strip(),
                'title': content_data.get('title', '').strip(),
                'description': content_data.get('description', '').strip(),
                'author': content_data.get('author', '').strip(),
                'date': content_data.get('date', '').strip(),
                'url': url
            }
            
            # Validate that we have meaningful content
            if not result['text'] or len(result['text']) < 100:
                raise ValueError("Extracted content is too short or empty")
            
            logger.info(f"Successfully extracted content from: {url} ({len(result['text'])} chars)")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch URL {url}: {str(e)}")
            raise Exception(f"Failed to fetch URL: {str(e)}")
        except ValueError as e:
            logger.error(f"Content extraction failed for {url}: {str(e)}")
            raise Exception(f"Content extraction failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error extracting content from {url}: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")
    
    @staticmethod
    def get_summary(content_text, max_length=500):
        """
        Get a short summary of the content.
        
        Args:
            content_text (str): Full text content
            max_length (int): Maximum length of summary
            
        Returns:
            str: Summary text
        """
        if not content_text:
            return ""
        
        # Take first few sentences or max_length characters
        summary = content_text[:max_length]
        
        # Try to end at a sentence boundary
        last_period = summary.rfind('.')
        if last_period > max_length * 0.7:  # If we have at least 70% of desired length
            summary = summary[:last_period + 1]
        
        return summary.strip()
