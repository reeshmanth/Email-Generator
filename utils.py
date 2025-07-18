import re
import ssl
import smtplib
import time
import logging
from typing import List, Tuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_email(email: str) -> bool:
    """Validate email format using regex pattern."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def clean_and_validate_inputs(names: str, emails: str) -> Tuple[List[str], List[str], List[str]]:
    """Clean and validate recipient names and emails."""
    errors = []
    names_list = [name.strip() for name in names.split('\n') if name.strip()]
    emails_list = [email.strip().lower() for email in emails.split('\n') if email.strip()]
    
    if len(names_list) != len(emails_list):
        errors.append(f"Number of names ({len(names_list)}) doesn't match number of emails ({len(emails_list)})")
    
    invalid_emails = [email for email in emails_list if not validate_email(email)]
    if invalid_emails:
        errors.append(f"Invalid email formats: {', '.join(invalid_emails)}")
    
    duplicate_emails = list(set([email for email in emails_list if emails_list.count(email) > 1]))
    if duplicate_emails:
        errors.append(f"Duplicate emails found: {', '.join(duplicate_emails)}")
    
    return names_list, emails_list, errors

def test_smtp_connection(provider_config: dict, sender_email: str, sender_password: str) -> Tuple[bool, str]:
    """Test SMTP connection with given credentials."""
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(provider_config["server"], provider_config["port"]) as server:
            if provider_config["use_tls"]:
                server.starttls(context=context)
            server.login(sender_email, sender_password)
            return True, "Connection successful"
    except smtplib.SMTPAuthenticationError:
        return False, "Authentication failed. Check your email and password/app password."
    except smtplib.SMTPConnectError:
        return False, "Could not connect to email server. Check your internet connection."
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def send_single_email(smtp_server, msg: MIMEMultipart, to_email: str, max_retries: int = 3) -> Tuple[bool, str]:
    """Send a single email with retry logic."""
    for attempt in range(max_retries):
        try:
            smtp_server.send_message(msg)
            return True, "Sent successfully"
        except smtplib.SMTPRecipientsRefused:
            return False, f"Invalid recipient email: {to_email}"
        except smtplib.SMTPException as e:
            if attempt == max_retries - 1:
                return False, f"SMTP error after {max_retries} attempts: {str(e)}"
            time.sleep(2 ** attempt)
        except Exception as e:
            if attempt == max_retries - 1:
                return False, f"Unexpected error: {str(e)}"
            time.sleep(2 ** attempt)
    return False, "Failed after maximum retries"

def extract_name_from_email(email: str) -> str:
    """Extract a readable name from email address."""
    try:
        local_part = email.split('@')[0]
        local_part = re.sub(r'[^a-zA-Z._]', '', local_part)

        if '.' in local_part:
            parts = local_part.split('.')
            name = ' '.join(part.capitalize() for part in parts if part)
        elif '_' in local_part:
            parts = local_part.split('_')
            name = ' '.join(part.capitalize() for part in parts if part)
        elif any(char.isupper() for char in local_part):
            name = re.sub(r'([a-z])([A-Z])', r'\1 \2', local_part)
            name = name.title()
        else:
            name = local_part.capitalize()
        
        return name if name.strip() else "User"
    except:
        return "User"

def format_email_content(content: str) -> str:
    """Format plain email content into clean HTML for preview."""
    # Normalize line endings
    content = content.strip().replace('\r\n', '\n').replace('\r', '\n')
    
    # Split content by double newlines into paragraphs
    paragraphs = content.split('\n\n')
    
    # Wrap each paragraph in <p> tags and replace single newlines with <br> inside paragraphs
    formatted_paragraphs = ['<p>' + p.replace('\n', '<br>') + '</p>' for p in paragraphs]
    
    return ''.join(formatted_paragraphs)

def strip_html_tags(text: str) -> str:
    """Remove all HTML tags and markdown code blocks from a string."""
    import re
    # Remove code blocks (triple backticks)
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()
