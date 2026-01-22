"""
Blog generator service.
Generates blog content using Google Gemini API.
"""
import google.generativeai as genai
import time
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize Gemini API
genai.configure(api_key=Config.GEMINI_API_KEY)


class BlogGenerator:
    """Generates blog content using Google Gemini API."""
    
    @staticmethod
    def generate_blog(prompt, max_tokens=None, temperature=0.7):
        """
        Generate blog content using Google Gemini API.
        
        Args:
            prompt (str): Complete prompt for blog generation
            max_tokens (int, optional): Maximum tokens to generate
            temperature (float): Creativity level (0.0-1.0)
            
        Returns:
            str: Generated blog content
            
        Raises:
            Exception: If blog generation fails
        """
        try:
            logger.info("Generating blog content with Google Gemini...")
            
            # Initialize the model
            model = genai.GenerativeModel(
                model_name=Config.GEMINI_MODEL,
                generation_config={
                    "temperature": temperature,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": max_tokens or 8192,
                }
            )
            
            # Create the full prompt with system instruction
            full_prompt = f"""You are an expert SEO content writer who creates engaging, original, and well-structured blog posts.

{prompt}"""
            
            # Generate content
            response = model.generate_content(full_prompt)
            
            # Extract generated content
            blog_content = response.text.strip()
            
            logger.info(f"Blog generated successfully with Gemini.")
            
            return blog_content
            
        except Exception as e:
            error_msg = str(e)
            
            # Handle specific Gemini API errors
            if "API_KEY_INVALID" in error_msg or "invalid API key" in error_msg.lower():
                logger.error("Gemini API authentication failed. Check API key.")
                raise Exception("Gemini API authentication failed. Please check API key configuration.")
            elif "RATE_LIMIT_EXCEEDED" in error_msg or "quota" in error_msg.lower():
                logger.error("Gemini API rate limit exceeded.")
                raise Exception("API rate limit exceeded. Please try again later.")
            elif "SAFETY" in error_msg or "blocked" in error_msg.lower():
                logger.error("Content was blocked by Gemini safety filters.")
                raise Exception("Content generation blocked by safety filters. Try a different topic or URL.")
            else:
                logger.error(f"Blog generation failed: {error_msg}")
                raise Exception(f"Blog generation failed: {error_msg}")
    
    @staticmethod
    def generate_with_retry(prompt, max_retries=2):
        """
        Generate blog with retry logic for robustness.
        
        Args:
            prompt (str): Complete prompt for blog generation
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            str: Generated blog content
        """
        for attempt in range(max_retries + 1):
            try:
                return BlogGenerator.generate_blog(prompt)
            except Exception as e:
                if attempt < max_retries:
                    logger.warning(f"Generation attempt {attempt + 1} failed, retrying...")
                    time.sleep(2)  # Wait 2 seconds before retry
                    continue
                else:
                    logger.error(f"All generation attempts failed: {str(e)}")
                    raise
