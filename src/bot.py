import os
import json
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from openai import OpenAI
import requests

# 1. THE "SECRET CODE" LOADER
def get_google_creds():
    # GitHub Action creates 'token.json' file, so we check for that first
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    elif "GOOGLE_TOKEN_JSON" in os.environ:
        token_info = json.loads(os.environ["GOOGLE_TOKEN_JSON"])
        creds = Credentials.from_authorized_user_info(token_info)
    else:
        raise Exception("No token.json found!")

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

# 2. THE MAIN BRAIN OF THE BOT
def run_daily_summary():
    creds = get_google_creds()
    
    # Connect to Gmail
    service_gmail = build('gmail', 'v1', credentials=creds)
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # --- GATHER DATA ---
    # Fetch 5 unread emails
    results = service_gmail.users().messages().list(userId='me', q="is:unread", maxResults=5).execute()
    messages = results.get('messages', [])
    
    email_summaries = []
    if not messages:
        summary_text = "✅ No new unread emails today!"
    else:
        for msg in messages:
            m = service_gmail.users().messages().get(userId='me', id=msg['id']).execute()
            email_summaries.append(m['snippet'])
        
        # --- AI ANALYSIS ---
        # Combine snippets and send to OpenAI
        all_emails = "\n".join(email_summaries)
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Summarize these emails into short bullet points."},
                {"role": "user", "content": f"Summarize these emails:\n{all_emails}"}
            ]
        )
        summary_text = f"🚀 *Gmail AI Summary*:\n{response.choices[0].message.content}"
    
    # 3. SEND TO SLACK
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    requests.post(webhook_url, json={"text": summary_text})
    print("Success! Summary sent to Slack.")

if __name__ == "__main__":
    run_daily_summary()
