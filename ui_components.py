import streamlit as st
import re
import streamlit_quill as st_quill

def init_session_state():
    if 'email_status' not in st.session_state:
        st.session_state.email_status = {}
    if 'generated_email' not in st.session_state:
        st.session_state.generated_email = None
    if 'names_list' not in st.session_state:
        st.session_state.names_list = []
    if 'emails_list' not in st.session_state:
        st.session_state.emails_list = []
    if 'sender_name' not in st.session_state:
        st.session_state.sender_name = ""
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False

def load_css():
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
            * {
                font-family: 'Inter', sans-serif;
            }
            .main {
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                padding: 0;
            }
            .stApp {
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            }
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 2rem !important;
                max-width: 100% !important;
            }
            .hero-section {
                text-align: center;
                padding: 16px 20px 24px 20px;
                position: relative;
                overflow: hidden;
            }
            .main-title {
                font-size: 4rem;
                font-weight: 800;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                letter-spacing: -2px;
                position: relative;
            }
            .subtitle {
                color: rgba(255, 255, 255, 0.7);
                font-size: 1.3rem;
                font-weight: 300;
                margin: 20px 0 0 0;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
                line-height: 1.6;
            }
            .glass-card {
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(25px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 35px;
                margin: 25px 0;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }
            .glass-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
                border-color: rgba(255, 255, 255, 0.2);
            }
            .section-header {
                color: white;
                font-size: 1.5rem;
                font-weight: 600;
                margin: 0 0 25px 0;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .section-icon {
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
            }
            /* Enhanced form styling */
            .stTextInput > label,
            .stTextArea > label,
            .stSelectbox > label,
            .stFileUploader > label,
            .stRadio > label,
            .stSlider > label,
            div[data-testid="stTextInput"] label,
            div[data-testid="stTextArea"] label,
            div[data-testid="stFileUploader"] label,
            div[data-testid="stRadio"] label,
            div[data-testid="stSlider"] label,
            .stTextInput label,
            .stTextArea label,
            .stFileUploader label,
            .stRadio label,
            .stSlider label {
                color: rgba(255, 255, 255, 0.9) !important;
                font-weight: 500 !important;
                font-size: 18px !important;
                margin-bottom: 8px !important;
            }
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {
                background: rgba(255, 255, 255, 0.1) !important;
                backdrop-filter: blur(20px) !important;
                border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 16px !important;
                color: white !important;
                padding: 16px 20px !important;
                font-size: 15px !important;
                transition: all 0.3s ease !important;
            }
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus {
                background: rgba(255, 255, 255, 0.2) !important;
                border-color: #667eea !important;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
                outline: none !important;
            }
            .stTextInput > div > div > input::placeholder,
            .stTextArea > div > div > textarea::placeholder {
                color: rgba(255, 255, 255, 0.5) !important;
            }
            /* Additional label styling with higher specificity */
            [data-testid="stTextInput"] > div > label,
            [data-testid="stTextArea"] > div > label,
            [data-testid="stFileUploader"] > div > label,
            [data-testid="stRadio"] > div > label,
            [data-testid="stSlider"] > div > label,
            [data-testid="stTextInput"] label,
            [data-testid="stTextArea"] label,
            [data-testid="stFileUploader"] label,
            [data-testid="stRadio"] label,
            [data-testid="stSlider"] label {
                font-size: 18px !important;
                font-weight: 500 !important;
                color: rgba(255, 255, 255, 0.9) !important;
            }
            /* Fixed selectbox styling */
            .stSelectbox > div > div {
                background: rgba(255, 255, 255, 0.1) !important;
                backdrop-filter: blur(20px) !important;
                border: 1.5px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 16px !important;
                color: white !important;
            }
            .stSelectbox > div > div > div {
                color: white !important;
                background: rgba(255, 255, 255, 0.1) !important;
                padding: 16px 20px !important;
            }
            .stSelectbox > div > div > div[data-baseweb="select"] > div {
                color: white !important;
                background: transparent !important;
            }
            /* Button styling */
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
                border-radius: 20px !important;
                border: none !important;
                padding: 18px 32px !important;
                font-weight: 600 !important;
                font-size: 16px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
                box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3) !important;
                width: 100% !important;
                height: 60px !important;
            }
            .stButton > button:hover {
                background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
                transform: translateY(-4px) !important;
                box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4) !important;
            }
            /* Email preview styling */
            .email-preview {
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid #ddd;
                border-radius: 16px;
                padding: 30px;
                margin: 20px 0;
                color: #333;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                position: relative;
            }
            .email-header {
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 20px;
                margin-bottom: 25px;
            }
            .email-meta {
                background: #f8f9fa;
                padding: 15px 20px;
                border-radius: 8px;
                margin-bottom: 20px;
                font-size: 14px;
                line-height: 1.6;
                border-left: 4px solid #667eea;
            }
            .email-content {
                line-height: 1.7;
                font-size: 16px;
                color: #444;
            }
            .email-content p {
                margin-bottom: 16px;
            }
            .edit-button {
                position: absolute;
                top: 20px;
                right: 20px;
                background: #667eea !important;
                color: white !important;
                border: none !important;
                padding: 8px 16px !important;
                border-radius: 8px !important;
                font-size: 14px !important;
                cursor: pointer !important;
                height: auto !important;
                width: auto !important;
            }
            .edit-button:hover {
                background: #5a6fd8 !important;
            }
            /* File uploader styling */
            .stFileUploader {
                background: rgba(255, 255, 255, 0.06) !important;
                backdrop-filter: blur(20px) !important;
                border: 2px dashed rgba(255, 255, 255, 0.2) !important;
                border-radius: 16px !important;
                padding: 30px !important;
                text-align: center !important;
            }
            .stFileUploader:hover {
                background: rgba(255, 255, 255, 0.1) !important;
                border-color: #667eea !important;
            }
            /* Status styling */
            .status-success {
                color: #10b981;
                background: rgba(16, 185, 129, 0.1);
                padding: 8px 16px;
                border-radius: 8px;
                display: inline-block;
                margin: 4px;
            }
            .status-error {
                color: #ef4444;
                background: rgba(239, 68, 68, 0.1);
                padding: 8px 16px;
                border-radius: 8px;
                display: inline-block;
                margin: 4px;
            }
            /* Footer */
            .footer {
                text-align: center;
                padding: 50px 20px;
                color: rgba(255, 255, 255, 0.5);
                margin-top: 60px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
            /* Mobile responsive */
            @media (max-width: 768px) {
                .main-title {
                    font-size: 2.8rem;
                }
                .glass-card {
                    padding: 25px;
                    margin: 15px 0;
                }
                .hero-section {
                    padding: 40px 20px 30px;
                }
            }
            /* Hide Streamlit elements */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display: none;}
            /* Hide Streamlit header link icon */
            [data-testid="stAppViewContainer"] a[title="Copy app link"],
            [data-testid="stAppViewContainer"] svg[data-testid*="icon-link"],
            [data-testid="stAppViewContainer"] button[title="Copy app link"],
            [data-testid="stHeader"] a, [data-testid="stHeader"] svg, [data-testid="stHeader"] button {
                display: none !important;
            }
            /* Hide any SVG or button after the main title in the hero section */
            .hero-section .main-title + svg,
            .hero-section .main-title + button,
            .hero-section .main-title + a {
                display: none !important;
            }
            /* Force all Streamlit widget labels (subheadings) to be larger */
            label[data-testid="stWidgetLabel"] {
                font-size: 20px !important;
                font-weight: 600 !important;
                color: rgba(255, 255, 255, 0.95) !important;
                margin-bottom: 10px !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_hero_section():
    st.markdown("""
        <div class="hero-section">
            <h1 class="main-title">✨ AI Email Studio</h1>
        </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
        <div class="footer">
            <p>🚀 AI Email Studio Pro - Powered by Gemini & Streamlit</p>
        </div>
    """, unsafe_allow_html=True)

def render_email_preview(sender_email: str, subject: str, file_attachment=None):
    import re
    if st.session_state.generated_email:
        from utils import format_email_content, extract_name_from_email, strip_html_tags
        preview_name = st.session_state.names_list[0] if st.session_state.names_list else "[RECIPIENT_NAME]"
        preview_content = st.session_state.generated_email.replace("[RECIPIENT_NAME]", preview_name)
        # Remove any bracketed placeholders like [something]
        preview_content = re.sub(r'\[[^\]]+\]', '', preview_content)
        # Remove all HTML tags using the new utility
        preview_content = strip_html_tags(preview_content)
        formatted_content = format_email_content(preview_content)
        sender_display_name = st.session_state.sender_name or extract_name_from_email(sender_email)

        st.markdown('<div class="section-header"><div class="section-icon">👁️</div>Email Preview</div>', unsafe_allow_html=True)
        # Meta info above the card
        st.markdown(f'<div style="margin-bottom: 10px;">'
            f'<strong>From:</strong> {sender_display_name} &lt;{sender_email}&gt;<br>'
            f'<strong>To:</strong> {preview_name} (and {len(st.session_state.emails_list) - 1 if len(st.session_state.emails_list) > 1 else 0} others)<br>'
            f'<strong>Subject:</strong> {subject}<br>'
            f'{f"<strong>Attachment:</strong> {file_attachment.name}" if file_attachment else ""}'
            '</div>', unsafe_allow_html=True)
        # Always show the formatted preview card at the top
        st.markdown(f'<div style="background: #fff; border-radius: 16px; padding: 30px; margin: 0 0 20px 0; color: #333; box-shadow: 0 10px 30px rgba(0,0,0,0.07); border: 1px solid #eee; position: relative; line-height:1.7; font-size:16px; white-space:pre-line;">{formatted_content}</div>', unsafe_allow_html=True)
        # Always show the edit box below the preview
        if 'editable_email' not in st.session_state:
            st.session_state.editable_email = preview_content
        st.session_state.editable_email = st.text_area("Edit Email Content", st.session_state.editable_email, height=250, key="editable_email_textarea")
        col_save, col_cancel = st.columns([1,1])
        if col_save.button("💾 Save", key="save_email_btn"):
            st.session_state.generated_email = st.session_state.editable_email
            st.session_state.editable_email = st.session_state.generated_email
        if col_cancel.button("❌ Cancel", key="cancel_email_btn"):
            st.session_state.editable_email = st.session_state.generated_email