"""
Prompt builder service.
Constructs optimized prompts for blog generation using LLM.
"""
from utils.logger import setup_logger

logger = setup_logger(__name__)


class PromptBuilder:
    """Builds SEO-optimized prompts for blog generation."""
    
    # Tone mappings
    TONE_INSTRUCTIONS = {
        'professional': 'Use a professional, authoritative tone suitable for business readers.',
        'casual': 'Use a friendly, conversational tone that is easy to read and engaging.',
        'technical': 'Use precise technical language suitable for an expert audience.',
        'persuasive': 'Use persuasive language that encourages action and engagement.',
        'educational': 'Use clear, instructive language suitable for teaching and learning.'
    }
    
    @staticmethod
    def build_blog_prompt(website_data, keywords, topic_analysis, blog_config):
        """
        Build a comprehensive prompt for blog generation.
        
        Args:
            website_data (dict): Extracted website content
            keywords (list): Extracted keywords
            topic_analysis (dict): Topic analysis results
            blog_config (dict): Blog generation configuration
                {
                    'length': int (word count),
                    'tone': str,
                    'include_cta': bool
                }
        
        Returns:
            str: Complete prompt for LLM
        """
        # Extract configuration
        target_length = blog_config.get('length', 1000)
        tone = blog_config.get('tone', 'professional')
        include_cta = blog_config.get('include_cta', True)
        
        # Get tone instruction
        tone_instruction = PromptBuilder.TONE_INSTRUCTIONS.get(
            tone,
            PromptBuilder.TONE_INSTRUCTIONS['professional']
        )
        
        # Build the prompt
        prompt = f"""You are an expert SEO content writer. Generate a high-quality, original blog post based on the following information.

SOURCE INFORMATION:
Website URL: {website_data.get('url', 'N/A')}
Website Title: {website_data.get('title', 'N/A')}
Content Summary: {website_data.get('description', 'Content about the topic')}

TOPIC ANALYSIS:
Main Keywords: {', '.join(keywords[:10])}
Content Category: {topic_analysis.get('category', 'general')}
Content Intent: {topic_analysis.get('intent', 'informational')}
Topic Summary: {topic_analysis.get('topic_summary', 'General content')}

BLOG REQUIREMENTS:
- Target Length: Approximately {target_length} words
- Tone: {tone_instruction}
- SEO Optimized: Yes (naturally incorporate keywords)
- Original Content: Do not copy from source, write original analysis and insights

STRUCTURE REQUIREMENTS:
1. Create an engaging, SEO-friendly title (H1)
2. Write a compelling introduction (2-3 paragraphs)
3. Organize content with clear H2 and H3 headings
4. Use short paragraphs (3-4 sentences each)
5. Include relevant examples and explanations
6. Write a strong conclusion
"""
        
        # Add CTA if requested
        if include_cta:
            prompt += "7. End with a call-to-action (CTA) encouraging reader engagement\n"
        
        prompt += """
WRITING GUIDELINES:
- Write naturally and engagingly
- Use transition words for better flow
- Incorporate keywords naturally (avoid keyword stuffing)
- Provide valuable insights and unique perspectives
- Use active voice
- Include specific examples where appropriate
- Make content scannable with bullet points or numbered lists where relevant

Generate the complete blog post now. Use proper markdown formatting for headings.
"""
        
        logger.debug(f"Built prompt for {target_length}-word {tone} blog")
        return prompt
    
    @staticmethod
    def build_meta_description_prompt(blog_content, keywords):
        """
        Build a prompt to generate SEO meta description.
        
        Args:
            blog_content (str): Generated blog content
            keywords (list): Main keywords
            
        Returns:
            str: Prompt for meta description generation
        """
        prompt = f"""Generate a compelling SEO meta description for the following blog post.

Main Keywords: {', '.join(keywords[:5])}

Blog Content Preview:
{blog_content[:500]}...

Requirements:
- Length: 150-160 characters
- Include primary keyword naturally
- Make it compelling and click-worthy
- Summarize the main value proposition
- Use active voice

Generate only the meta description text, nothing else.
"""
        return prompt
