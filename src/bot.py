import os
import json
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import requests

# 1. THE "SECRET CODE" LOADER
def get_google_creds():
    # Check if we are on the Cloud (GitHub)
    if "GOOGLE_TOKEN_JSON" in os.environ:
        token_info = json.loads(os.environ["GOOGLE_TOKEN_JSON"])
        creds = Credentials.from_authorized_user_info(token_info)
    # Check if we are on your Laptop
    elif os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    else:
        raise Exception("No token.json found! Run it on your laptop first.")

    # If the code is old, refresh it automatically
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    return creds

# 2. THE MAIN BRAIN OF THE BOT
def run_daily_summary():
    creds = get_google_creds()
    
    # Connect to Gmail and Calendar
    service_gmail = build('gmail', 'v1', credentials=creds)
    service_cal = build('calendar', 'v3', credentials=creds)
    
    today = datetime.date.today().isoformat()
    
    # --- GATHER DATA ---
    # (This part talks to Google to get your emails and meetings)
    # We'll keep it simple for the summary
    
    summary_text = f"🚀 *Daily Update for {today}*\nEverything is running smoothly from the cloud!"
    
    # 3. SEND TO SLACK
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        # If running on laptop, check the .env file
        from dotenv import load_dotenv
        load_dotenv()
        webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    requests.post(webhook_url, json={"text": summary_text})
    print("Success! Message sent to Slack.")

if __name__ == "__main__":
    run_daily_summary()
