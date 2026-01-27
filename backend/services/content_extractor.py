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
            
            # Extract content using Trafilatura with progressive fallbacks
            downloaded = trafilatura.extract(
                response.content,
                include_comments=False,
                include_tables=False,
                favor_precision=True,
                with_metadata=True,
                output_format='json'
            )

            # If primary extraction fails, try a more permissive extraction
            if not downloaded:
                logger.info(f"Primary trafilatura extract failed for {url}, trying permissive mode")
                downloaded = trafilatura.extract(
                    response.text,
                    include_comments=True,
                    include_tables=True,
                    favor_precision=False,
                    with_metadata=True,
                    output_format='json'
                )

            # Parse the JSON response if we have it
            import json
            content_data = None
            if downloaded:
                content_data = json.loads(downloaded) if isinstance(downloaded, str) else downloaded
            else:
                # Try plain-text extraction (no metadata)
                plain_text = trafilatura.extract(response.content)
                if plain_text:
                    content_data = {'text': plain_text, 'title': '', 'description': '', 'author': '', 'date': ''}
                else:
                    # Final fallback: BeautifulSoup visible text
                    try:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(response.content, "html.parser")
                        visible = soup.get_text(separator="\n")
                        visible = visible.strip() if visible else ""
                        if visible:
                            content_data = {'text': visible, 'title': '', 'description': '', 'author': '', 'date': ''}
                    except Exception:
                        content_data = None

            if not content_data:
                raise ValueError("Could not extract content from the page")
            
            # Extract and clean data (use safe fallback when metadata is None)
            def _safe_strip(value):
                return (value or '').strip()

            result = {
                'text': _safe_strip(content_data.get('text')),
                'title': _safe_strip(content_data.get('title')),
                'description': _safe_strip(content_data.get('description')),
                'author': _safe_strip(content_data.get('author')),
                'date': _safe_strip(content_data.get('date')),
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
