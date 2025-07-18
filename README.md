# AI Email Studio Pro

A professional, modular, and user-friendly email generation and sending platform powered by Google Gemini AI and Streamlit.

---

## 🚀 Features

- **AI-Powered Email Generation**: Uses Google Gemini to generate context-aware, professional, and fully-completed emails—never any placeholders or bracketed instructions.
- **Bulk Personalized Sending**: Send to multiple recipients, each with their own name, with robust error handling and rate limiting.
- **Modern Streamlit UI**: Beautiful, responsive, and user-friendly interface with persistent preview and editing.
- **Attachment Support**: Upload and send files with your emails.
- **Multiple Providers**: Gmail, Outlook, Yahoo, and easily extensible to others.
- **No Placeholders Policy**: All generated emails are ready to send, with no incomplete sentences or bracketed instructions—ever.
- **Editable Preview**: Always-visible plain text edit box below the preview, with Save/Cancel for easy last-minute changes.
- **Separation of Concerns**: Modular codebase (UI, AI, email, utils, config) for easy maintenance and extension.
- **Validation & Safety**: Real-time validation, duplicate checks, and connection testing to prevent errors.
- **Customization**: Easily change prompts, providers, and UI styling.

---

## 🏗️ Architecture & Concepts

- **Streamlit** for the web UI, with custom CSS for a modern look.
- **Google Gemini AI** for generating high-quality, context-aware email content.
- **SMTP** for sending emails, with support for attachments and multiple providers.
- **Session State** for persistent user data and editing experience.
- **Strict Prompting & Post-Processing** to ensure no bracketed placeholders or incomplete content ever appear in generated emails.
- **Modular Design**: Each module (UI, AI, email, utils, config) has a single responsibility and can be reused or extended independently.

---

## 📦 Project Structure

```
Email Generator/
├── main.py            # Main application entry point
├── config.py          # Configuration constants and settings
├── utils.py           # Utility functions and helpers
├── ai_generator.py    # AI email generation module
├── email_sender.py    # Email sending functionality
├── ui_components.py   # UI components and styling
├── requirements.txt   # Python dependencies
├── README.md          # Project documentation
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- Google Generative AI API key
- Email provider credentials (Gmail App Password, etc.)

### Installation
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure your API key**:
   - Edit `config.py`
   - Replace `GOOGLE_API_KEY` with your actual API key
4. **Run the application**:
   ```bash
   streamlit run main.py
   ```

---

## 👩‍💻 Usage

1. **Configure Email Settings**: Enter your email, app password, and sender name.
2. **Add Recipients**: Enter names and email addresses (one per line, in order).
3. **Set Content**: Choose subject, tone, and length preferences. Optionally add extra context.
4. **Generate Content**: Click "Generate Email Preview". The preview will show formatted, ready-to-send content (never placeholders).
5. **Edit if Needed**: Use the always-visible edit box below the preview to make changes. Save or cancel edits as needed.
6. **Send Emails**: Click "Send All Emails" to send to all recipients, with progress and error reporting.

---

## 🛠️ Customization

- **Add Providers**: Edit `config.py` to add or modify email providers.
- **Change Prompts**: Edit `ai_generator.py` to adjust the AI's behavior and instructions.
- **Restyle UI**: Edit `ui_components.py` for custom CSS and UI tweaks.

---

## 🧩 Module Overview

- **config.py**: Centralized configuration (API keys, providers, page settings)
- **utils.py**: Validation, formatting, and helper functions
- **ai_generator.py**: Gemini AI integration, strict prompt creation, and retry logic
- **email_sender.py**: Bulk and single email sending, with attachment support and error handling
- **ui_components.py**: All UI rendering, session state, and persistent editing logic
- **main.py**: Orchestrates the app, integrates all modules, and manages the Streamlit flow

---

## 🐞 Troubleshooting

- **API Key Error**: Ensure your Google API key is valid and has Gemini access
- **SMTP Connection**: Use App Passwords for Gmail/Outlook
- **File Size**: Keep attachments under 25MB
- **Rate Limiting**: Increase delay if needed

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License

---

**Built with ❤️ using Streamlit and Google Gemini AI** 