"""
URL validation service.
Validates URL format and checks if the URL is reachable.
"""
import re
import requests
from utils.logger import setup_logger

logger = setup_logger(__name__)


class URLValidator:
    """Validates URLs for proper format and reachability."""
    
    # URL regex pattern
    URL_PATTERN = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    @staticmethod
    def is_valid_format(url):
        """
        Check if URL has valid format.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if URL format is valid, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        return bool(URLValidator.URL_PATTERN.match(url.strip()))
    
    @staticmethod
    def is_reachable(url, timeout=5):
        """
        Check if URL is reachable (returns HTTP 200-399).
        
        Args:
            url (str): URL to check
            timeout (int): Request timeout in seconds
            
        Returns:
            tuple: (bool: is_reachable, str: status_message)
        """
        try:
            response = requests.head(
                url,
                timeout=timeout,
                allow_redirects=True,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code < 400:
                logger.info(f"URL is reachable: {url} (Status: {response.status_code})")
                return True, "URL is reachable"
            else:
                logger.warning(f"URL returned error: {url} (Status: {response.status_code})")
                return False, f"URL returned status code {response.status_code}"
                
        except requests.exceptions.Timeout:
            logger.warning(f"URL timeout: {url}")
            return False, "Request timeout - URL took too long to respond"
        except requests.exceptions.ConnectionError:
            logger.warning(f"Connection error: {url}")
            return False, "Connection error - Could not reach the URL"
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            return False, f"Request error: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error validating {url}: {str(e)}")
            return False, "Unexpected error occurred"
    
    @staticmethod
    def validate(url):
        """
        Perform full URL validation (format + reachability).
        
        Args:
            url (str): URL to validate
            
        Returns:
            tuple: (bool: is_valid, str: message)
        """
        # Check format
        if not URLValidator.is_valid_format(url):
            return False, "Invalid URL format"
        
        # Check reachability
        is_reachable, message = URLValidator.is_reachable(url)
        
        return is_reachable, message
