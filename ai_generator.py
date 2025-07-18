import time
import google.generativeai as genai
from google.generativeai.generative_models import GenerativeModel
from google.generativeai.client import configure
from config import GOOGLE_API_KEY

def generate_email_with_retry(model, prompt: str, max_retries: int = 3) -> str:
    """Generate email content with retry logic."""
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text
            else:
                raise Exception("Empty response from AI model")
        except Exception as e:
            if attempt == max_retries - 1:
                return f"⚠️ Could not generate email content after {max_retries} attempts. Error: {str(e)}"
            time.sleep(2 ** attempt)
    return "⚠️ Failed to generate email content"

def create_email_prompt(sender_name: str, sender_email: str, subject: str, 
                       email_tone: str, content_length: str, additional_context: str = "") -> str:
    """Create a comprehensive prompt for email generation."""
    
    tone_mapping = {
        "Professional & Formal": "professional and formal",
        "Friendly & Conversational": "friendly and conversational",
        "Enthusiastic & Energetic": "enthusiastic and energetic",
        "Informative & Direct": "informative and direct"
    }
    
    length_mapping = {
        "Short & Concise (300-400 words)": "300-400 words, concise and to the point",
        "Medium Length (400-700 words)": "400-700 words, well-balanced detail",
        "Detailed Content (700-1500 words)": "700-1500 words, comprehensive and detailed",
        "Comprehensive (1500+ words)": "1500+ words, extremely comprehensive and thorough"
    }
    
    cleaned_context = additional_context.strip()
    final_context = f"Additional Context: {cleaned_context}" if cleaned_context else "No additional context."
    
    prompt = f"""
Generate a {tone_mapping[email_tone]} email with the following specifications:

FROM: {sender_name} ({sender_email})
Subject: {subject}
Content Length: {length_mapping[content_length]}
{final_context}

Requirements:
1. Write a complete, engaging, and well-structured email.
2. Include appropriate greetings and closings.
3. Personalize the email using the [RECIPIENT_NAME] placeholder for recipient names.
4. Match the specified tone: {email_tone}.
5. Provide relevant and valuable content throughout.
6. Use proper email formatting with clear paragraphs.
7. Add a professional signature with:
   - Name: {sender_name}
   - Email: {sender_email}
8. Do NOT use generic placeholders like "Your Name" or "Your Email".
9. Ensure the email feels authentic and personal from {sender_name}.
10. Do NOT include instructional or template placeholders (e.g., [Elaborate...], [Insert Topic]).
11. Do NOT use any brackets, placeholders, or incomplete sentences—write all content fully and ready to send.
12. If any detail is missing, make a plausible, professional guess—never leave blanks or instructions.
"""
    return prompt

def initialize_ai_model():
    """Initialize the Gemini AI model."""
    try:
        configure(api_key=GOOGLE_API_KEY)
        model = GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        raise Exception(f"Failed to initialize AI model: {str(e)}")

def generate_email_content(sender_name: str, sender_email: str, subject: str,
                          email_tone: str, content_length: str, additional_context: str = "") -> str:
    """Main function to generate email content using AI."""
    try:
        model = initialize_ai_model()
        prompt = create_email_prompt(sender_name, sender_email, subject, 
                                   email_tone, content_length, additional_context)
        return generate_email_with_retry(model, prompt)
    except Exception as e:
        return f"❌ Error generating email: {str(e)}" 