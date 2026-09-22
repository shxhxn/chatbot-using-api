# Gemini CLI Chat

A small Python command-line chat client that sends prompts to Google's Gemini API and stores conversations locally in SQLite.

## Features

- Ask Gemini questions from the terminal
- Save questions and responses to a local SQLite database
- Review previous conversations
- Keep API credentials outside the source code

## Setup

1. Create and activate a Python virtual environment.
2. Install the dependency:

   ```bash
   pip install -r requirements.txt
   ```

3. Set your Gemini API key:

   **macOS / Linux**

   ```bash
   export GEMINI_API_KEY="your_api_key"
   ```

   **Windows PowerShell**

   ```powershell
   $env:GEMINI_API_KEY="your_api_key"
   ```

4. Start the app:

   ```bash
   python 1_test.py
   ```

## Security

Never commit real API keys. `.env` and the local `chat.db` file are ignored by Git.

If a credential was ever committed, removing it from the current file is not enough: revoke it in the provider console and issue a replacement because old commits remain in Git history.

## Tech stack

Python · Gemini API · SQLite
