import ssl
import smtplib
import time
from typing import List, Tuple, Dict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from utils import test_smtp_connection, send_single_email
from config import EMAIL_PROVIDERS

class EmailSender:
    def __init__(self, provider: str, sender_email: str, sender_password: str):
        self.provider = provider
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.provider_config = EMAIL_PROVIDERS[provider]
        
    def test_connection(self) -> Tuple[bool, str]:
        """Test SMTP connection."""
        return test_smtp_connection(self.provider_config, self.sender_email, self.sender_password)
    
    def send_bulk_emails(self, names_list: List[str], emails_list: List[str], 
                        subject: str, email_content: str, file_attachment=None,
                        rate_limit: int = 2, max_retries: int = 3) -> Dict[str, Tuple[str, str]]:
        """Send emails to multiple recipients with progress tracking."""
        
        # Test connection first
        connection_success, connection_message = self.test_connection()
        if not connection_success:
            return {"connection_error": ("error", connection_message)}
        
        email_status = {}
        success_count = 0
        failed_count = 0
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.provider_config["server"], self.provider_config["port"]) as server:
                if self.provider_config["use_tls"]:
                    server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                
                for i, (name, email) in enumerate(zip(names_list, emails_list)):
                    try:
                        # Personalize content
                        personalized_content = email_content.replace("[RECIPIENT_NAME]", name)
                        
                        # Create message
                        msg = MIMEMultipart()
                        msg['From'] = self.sender_email
                        msg['To'] = email
                        msg['Subject'] = subject
                        
                        msg.attach(MIMEText(personalized_content, 'plain'))
                        
                        # Add attachment if provided
                        if file_attachment:
                            file_attachment.seek(0)  # Reset file pointer
                            attachment = MIMEApplication(file_attachment.read())
                            attachment.add_header(
                               'Content-Disposition',
                                'attachment',
                                filename=file_attachment.name
                            )
                            msg.attach(attachment)

                        # Send email
                        success, message = send_single_email(server, msg, email, max_retries)

                        if success:
                            success_count += 1
                            email_status[email] = ("success", "Sent successfully")
                        else:
                            failed_count += 1
                            email_status[email] = ("error", message)

                        # Rate limiting
                        if i < len(names_list) - 1:
                            time.sleep(rate_limit)

                    except Exception as e:
                        failed_count += 1
                        email_status[email] = ("error", f"Unexpected error: {str(e)}")

        except Exception as e:
            return {"smtp_error": ("error", f"SMTP connection error: {str(e)}")}
        
        # Add summary
        email_status["summary"] = ("info", f"Success: {success_count}, Failed: {failed_count}")
        return email_status
    
    def send_single_email(self, to_email: str, to_name: str, subject: str, 
                         email_content: str, file_attachment=None) -> Tuple[bool, str]:
        """Send a single email to one recipient."""
        
        # Test connection first
        connection_success, connection_message = self.test_connection()
        if not connection_success:
            return False, connection_message
        
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.provider_config["server"], self.provider_config["port"]) as server:
                if self.provider_config["use_tls"]:
                    server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                
                # Personalize content
                personalized_content = email_content.replace("[RECIPIENT_NAME]", to_name)
                
                # Create message
                msg = MIMEMultipart()
                msg['From'] = self.sender_email
                msg['To'] = to_email
                msg['Subject'] = subject
                
                msg.attach(MIMEText(personalized_content, 'plain'))
                
                # Add attachment if provided
                if file_attachment:
                    file_attachment.seek(0)
                    attachment = MIMEApplication(file_attachment.read())
                    attachment.add_header(
                       'Content-Disposition',
                        'attachment',
                        filename=file_attachment.name
                    )
                    msg.attach(attachment)

                # Send email
                return send_single_email(server, msg, to_email)
                
        except Exception as e:
            return False, f"SMTP connection error: {str(e)}" 