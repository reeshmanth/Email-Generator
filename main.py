import streamlit as st
from config import PAGE_CONFIG, EMAIL_PROVIDERS, RATE_LIMIT_DELAY, MAX_RETRIES
from utils import clean_and_validate_inputs, extract_name_from_email
from ai_generator import generate_email_content
from email_sender import EmailSender
from ui_components import init_session_state, load_css, render_hero_section, render_footer, render_email_preview

# Page configuration
st.set_page_config(
    page_title="AI Email Generator",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

def main():
    # Initialize session state
    init_session_state()
    
    # Load CSS
    load_css()
    
    # Simple line title at the top
    st.markdown('<div style="text-align:center; font-size:2.7rem; font-weight:800; font-family:Montserrat,sans-serif; letter-spacing:-1px; margin-bottom:1.5rem; color:#fff;">✨ AI Email Studio</div>', unsafe_allow_html=True)
    
    # --- Main Layout: Two Columns ---
    left_col, right_col = st.columns([1, 1], gap="large")
    
    # First Row
    with left_col:
        st.markdown('<div style="margin-bottom: 1.2rem;"></div>', unsafe_allow_html=True)
        # Email Configuration
        st.markdown('<div class="section-header" style="font-size:1.5rem; font-weight:700; font-family:Montserrat,sans-serif; color:#fff; margin-bottom:0.7rem;"><div class="section-icon">📧</div>Email Configuration</div>', unsafe_allow_html=True)
        provider_options = ["Gmail", "Outlook", "Yahoo"]
        col_provider, col_sender_name = st.columns([1, 1], gap="small")
        with col_provider:
            email_provider = st.radio(
                "Email Provider",
                options=provider_options,
                key="provider_radio",
                help="Select your email provider"
            )
        with col_sender_name:
            SENDER_NAME = st.text_input(
                "Sender Name",
                placeholder="Your Name",
                help="Enter the name to display as the sender"
            )
        SENDER_EMAIL = st.text_input(
            "Email Address",
            placeholder="your.email@gmail.com",
            help="Enter your email address"
        )
        SENDER_PASSWORD = st.text_input(
            "App Password",
            type="password",
            help="Use App Password for Gmail/Outlook, not your regular password"
        )
        if st.button("🔍 Test Connection"):
            if SENDER_EMAIL and SENDER_PASSWORD and email_provider:
                email_sender = EmailSender(email_provider, SENDER_EMAIL, SENDER_PASSWORD)
                with st.spinner("Testing connection..."):
                    success, message = email_sender.test_connection()
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")
            else:
                st.warning("Please enter email, password, and select a provider first")
    
    with right_col:
        st.markdown('<div style="margin-bottom: 1.2rem;"></div>', unsafe_allow_html=True)
        # Recipients & Content
        st.markdown('<div class="section-header" style="font-size:1.5rem; font-weight:700; font-family:Montserrat,sans-serif; color:#fff; margin-bottom:0.7rem;"><div class="section-icon">👥</div>Recipients & Content</div>', unsafe_allow_html=True)
        recipient_names = st.text_area(
            "Recipient Names",
            height=120,
            placeholder="John Smith\nJane Doe\nMike Johnson",
            help="Enter one name per line for personalization"
        )
        recipient_emails = st.text_area(
            "Recipient Email Addresses",
            height=120,
            placeholder="john@company.com\njane@company.com\nmike@company.com",
            help="Enter one email per line (must match names order)"
        )
        if recipient_names and recipient_emails:
            names_list, emails_list, validation_errors = clean_and_validate_inputs(recipient_names, recipient_emails)
            if validation_errors:
                for error in validation_errors:
                    st.error(f"⚠️ {error}")
            else:
                st.success(f"✅ {len(names_list)} valid recipients ready")

    # Second Row
    st.markdown('<hr style="border: none; border-top: 1.5px solid #a084e8; margin: 2.5rem 0 2.5rem 0;">', unsafe_allow_html=True)
    left_col2, right_col2 = st.columns([1, 1], gap="large")
    
    with left_col2:
        st.markdown('<div style="margin-bottom: 1.2rem;"></div>', unsafe_allow_html=True)
        # Content Customization
        st.markdown('<div class="section-header" style="font-size:1.5rem; font-weight:700; font-family:Montserrat,sans-serif; color:#fff; margin-bottom:0.7rem;"><div class="section-icon">📝</div>Content Customization</div>', unsafe_allow_html=True)
    
        subject = st.text_area(
            "Email Subject",
            height=68,
            placeholder="Weekly Team Update - Important Announcements",
            help="Clear and engaging subject line"
        )
        col_tone, col_length = st.columns([1, 1.4], gap="large")
        with col_tone:
            tone_options = ["Professional & Formal", "Friendly & Conversational", "Enthusiastic & Energetic", "Informative & Direct"]
            email_tone = st.radio(
                "Email Tone & Style",
                options=tone_options,
                key="email_tone_radio",
                help="Choose the tone and style for your email content"
            )
        with col_length:
            content_length_options = ["Short & Concise (300-400 words)", "Medium Length (400-700 words)", "Detailed Content (700-1500 words)", "Comprehensive (1500+ words)"]
            content_length = st.radio(
                "Content Length Preference",
                options=content_length_options,
                key="content_length_radio",
                help="Select how detailed or concise you want your email to be"
            )
        additional_context = st.text_area(
            "Additional Context (Optional)",
            height=100,
            placeholder="Add any specific details, context, or instructions you want included in the emails...",
            help="Provide extra context to make emails more relevant and personalized"
        )
    
    with right_col2:
        st.markdown('<div style="margin-bottom: 1.2rem;"></div>', unsafe_allow_html=True)
        # File Attachments
        st.markdown('<div class="section-header" style="font-size:1.5rem; font-weight:700; font-family:Montserrat,sans-serif; color:#fff; margin-bottom:0.7rem;"><div class="section-icon">📎</div>File Attachments</div>', unsafe_allow_html=True)
        file_attachment = st.file_uploader(
            "Choose files to attach (Optional)",
            type=["pdf", "docx", "jpg", "jpeg", "png", "txt", "xlsx", "pptx"],
            help="Upload documents, images, or other files to include with your emails"
        )
        if file_attachment:
            file_size_mb = file_attachment.size / (1024 * 1024)
            if file_size_mb > 25:
                st.error(f"⚠️ File too large ({file_size_mb:.1f}MB). Most email providers limit attachments to 25MB.")
            else:
                st.success(f"📎 File ready: {file_attachment.name} ({file_size_mb:.1f}MB)")
        
        # Half-width separator line before Delivery Settings
        st.markdown('<hr style="border: none; border-top: 1.5px solid #a084e8; width: 100%; margin: 2rem 0 2rem 0;">', unsafe_allow_html=True)
        
        # Delivery Settings (below File Attachments)
        st.markdown('<div class="section-header" style="margin-top:32px; font-size:1.5rem; font-weight:700; font-family:Montserrat,sans-serif; color:#fff; margin-bottom:0.7rem;"><div class="section-icon">⚙️</div>Delivery Settings</div>', unsafe_allow_html=True)
        col_delay, col_retries = st.columns(2)
        with col_delay:
            rate_limit = st.slider(
                "Delay between emails (seconds)",
                min_value=1,
                max_value=10,
                value=RATE_LIMIT_DELAY,
                help="Prevent spam detection by adding delays"
            )
        with col_retries:
            max_retries = st.slider(
                "Max retry attempts",
                min_value=1,
                max_value=5,
                value=MAX_RETRIES,
                help="Number of retry attempts for failed emails"
            )

    # --- Action Buttons, Preview, Footer remain unchanged ---
    # Add separation line before Generate & Send
    st.markdown('<hr style="border: none; border-top: 1.5px solid #a084e8; margin: 2.5rem 0 2.5rem 0;">', unsafe_allow_html=True)
    # Action Buttons
    st.markdown('<div class="section-header" style="font-size:1.5rem; font-weight:700; font-family:Montserrat,sans-serif; color:#fff; margin-bottom:0.7rem;"><div class="section-icon">🚀</div>Generate & Send</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        if st.button("🎯 Generate Email Preview"):
            if not email_provider or not email_tone or not content_length:
                st.warning("Please select all required options before proceeding.")
            elif not recipient_names or not recipient_emails or not subject:
                st.error("❌ Please fill in all required fields: names, emails, and subject")
            else:
                names_list, emails_list, validation_errors = clean_and_validate_inputs(recipient_names, recipient_emails)
                
                if validation_errors:
                    for error in validation_errors:
                        st.error(f"⚠️ {error}")
                else:
                    if not SENDER_EMAIL:
                        st.error("❌ Please enter your email address in the sidebar")
                    elif not SENDER_NAME:
                        st.error("❌ Please enter your sender name in the sidebar")
                    else:
                        try:
                            clean_username = SENDER_NAME
                            with st.spinner("🤖 Generating email content..."):
                                email_content = generate_email_content(
                                    sender_name=clean_username,
                                    sender_email=SENDER_EMAIL,
                                    subject=subject,
                                    email_tone=email_tone,
                                    content_length=content_length,
                                    additional_context=additional_context
                                )
                            st.session_state.generated_email = email_content
                            st.session_state.editable_email = email_content
                            st.session_state.names_list = names_list
                            st.session_state.emails_list = emails_list
                            st.session_state.sender_name = clean_username
                            st.session_state.edit_mode = False
                            st.success(f"✅ Email content generated successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error generating email: {str(e)}")
    
    with col2:
        send_disabled = (not SENDER_EMAIL or not SENDER_PASSWORD or 
                        'generated_email' not in st.session_state or
                        st.session_state.generated_email is None)
        
        if st.button("📧 Send All Emails", disabled=send_disabled):
            if st.session_state.generated_email is None:
                st.error("❌ Please generate email content first")
            else:
                email_sender = EmailSender(email_provider, SENDER_EMAIL, SENDER_PASSWORD)
                names_list = st.session_state.names_list
                emails_list = st.session_state.emails_list
                email_content = st.session_state.generated_email
                
                progress_bar = st.progress(0)
                status_container = st.container()
                
                email_status = email_sender.send_bulk_emails(
                    names_list=names_list,
                    emails_list=emails_list,
                    subject=subject,
                    email_content=email_content,
                    file_attachment=file_attachment,
                    rate_limit=rate_limit,
                    max_retries=max_retries
                )
                
                # Update progress
                progress_bar.progress(1.0)
                
                # Display results
                with status_container:
                    if "connection_error" in email_status:
                        st.error(f"❌ {email_status['connection_error'][1]}")
                    elif "smtp_error" in email_status:
                        st.error(f"❌ {email_status['smtp_error'][1]}")
                    else:
                        summary = email_status.get("summary", ("info", "No summary available"))
                        st.info(f"📊 {summary[1]}")
                        
                        # Show individual email statuses
                        for email, (status, message) in email_status.items():
                            if email != "summary":
                                if status == "success":
                                    st.success(f"✅ {email}: {message}")
                                else:
                                    st.error(f"❌ {email}: {message}")
                
                st.session_state.email_status = email_status

    # Email Preview Section
    render_email_preview(SENDER_EMAIL, subject, file_attachment)

    # Footer
    render_footer()

# Run the app
if __name__ == "__main__":
    main() 