"""
SEO post-processor service.
Enhances generated blog content with SEO optimizations.
"""
import re
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SEOPostProcessor:
    """Post-processes generated blog content for SEO optimization."""
    
    @staticmethod
    def process_blog(blog_content, keywords):
        """
        Apply SEO enhancements to generated blog content.
        
        Args:
            blog_content (str): Raw generated blog content
            keywords (list): Main keywords to optimize for
            
        Returns:
            dict: Processed blog with metadata
                {
                    'content': str,  # Enhanced blog content
                    'meta_description': str,  # SEO meta description
                    'title': str,  # Extracted title
                    'headings': list,  # All headings
                    'word_count': int,  # Total word count
                    'reading_time': int  # Estimated reading time in minutes
                }
        """
        try:
            # Extract title (first H1)
            title = SEOPostProcessor._extract_title(blog_content)
            
            # Extract all headings
            headings = SEOPostProcessor._extract_headings(blog_content)
            
            # Calculate statistics
            word_count = len(blog_content.split())
            reading_time = max(1, word_count // 200)  # Average reading speed: 200 wpm
            
            # Generate meta description
            meta_description = SEOPostProcessor._generate_meta_description(
                blog_content, keywords
            )
            
            # Enhance content formatting
            enhanced_content = SEOPostProcessor._enhance_formatting(blog_content)
            
            result = {
                'content': enhanced_content,
                'meta_description': meta_description,
                'title': title,
                'headings': headings,
                'word_count': word_count,
                'reading_time': reading_time,
                'keywords': keywords[:10]
            }
            
            logger.info(f"SEO post-processing complete. Word count: {word_count}, "
                       f"Reading time: {reading_time} min")
            return result
            
        except Exception as e:
            logger.error(f"SEO post-processing failed: {str(e)}")
            # Return original content with minimal metadata
            return {
                'content': blog_content,
                'meta_description': '',
                'title': 'Blog Post',
                'headings': [],
                'word_count': len(blog_content.split()),
                'reading_time': 5,
                'keywords': keywords
            }
    
    @staticmethod
    def _extract_title(content):
        """Extract the first H1 heading as title."""
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        return "Blog Post"
    
    @staticmethod
    def _extract_headings(content):
        """Extract all headings from content."""
        headings = []
        
        # Find all markdown headings
        heading_pattern = r'^(#{1,6})\s+(.+)$'
        matches = re.finditer(heading_pattern, content, re.MULTILINE)
        
        for match in matches:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append({
                'level': level,
                'text': text
            })
        
        return headings
    
    @staticmethod
    def _generate_meta_description(content, keywords):
        """Generate SEO-friendly meta description."""
        # Extract first paragraph (after title)
        paragraphs = content.split('\n\n')
        
        description = ""
        for para in paragraphs:
            # Skip headings
            if para.strip().startswith('#'):
                continue
            
            # Clean and use this paragraph
            description = para.strip()
            if description:
                break
        
        # Clean markdown formatting
        description = re.sub(r'[#*_`\[\]]', '', description)
        
        # Truncate to ~155 characters
        if len(description) > 155:
            description = description[:152] + '...'
        
        # Ensure primary keyword is included if not present
        if keywords and keywords[0].lower() not in description.lower():
            # Try to naturally insert keyword
            if len(description) < 140:
                description = f"{keywords[0]} - {description}"
        
        return description
    
    @staticmethod
    def _enhance_formatting(content):
        """Enhance content formatting for better readability."""
        # Ensure proper spacing after headings
        content = re.sub(r'(^#{1,6}\s+.+$)\n([^\n])', r'\1\n\n\2', content, flags=re.MULTILINE)
        
        # Ensure proper spacing between paragraphs
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Add emphasis to first paragraph (optional)
        # This is a simple enhancement; more sophisticated formatting can be added
        
        return content.strip()
    
    @staticmethod
    def add_internal_links(content, link_suggestions):
        """
        Add internal links to content (placeholder for future enhancement).
        
        Args:
            content (str): Blog content
            link_suggestions (list): List of suggested links
            
        Returns:
            str: Content with internal links
        """
        # This is a placeholder for future implementation
        # Could be enhanced to intelligently add internal links
        return content
    
    @staticmethod
    def optimize_for_featured_snippet(content):
        """
        Optimize content structure for featured snippets.
        
        Args:
            content (str): Blog content
            
        Returns:
            str: Optimized content
        """
        # This is a placeholder for future implementation
        # Could be enhanced to format content for featured snippets
        return content
