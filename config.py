# Configuration Constants
GOOGLE_API_KEY = "AIzaSyCkd_caswEUQ4oJ4sZfCqKvCq0Ac6K2x_g"  # Enter your API key here
RATE_LIMIT_DELAY = 2
MAX_RETRIES = 3
RETRY_DELAY = 5

# Email provider configurations
EMAIL_PROVIDERS = {
    "Gmail": {"server": "smtp.gmail.com", "port": 587, "use_tls": True},
    "Outlook": {"server": "smtp-mail.outlook.com", "port": 587, "use_tls": True},
    "Yahoo": {"server": "smtp.mail.yahoo.com", "port": 587, "use_tls": True}
}

# Page configuration
PAGE_CONFIG = {
    "page_title": "AI Email Generator",
    "page_icon": "📧",
    "layout": "wide",
    "initial_sidebar_state": "collapsed"
} 
