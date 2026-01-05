from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText
import os
#Для тестов
#from dotenv import load_dotenv
#load_dotenv()

def get_gmail_service():
    creds = Credentials(
        None,
        refresh_token=os.environ.get("GOOGLE_REFRESH_TOKEN"),
        client_id=os.environ.get("GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build('gmail', 'v1', credentials=creds)

def create_message(to_email: str, subject: str, body_text: str):
    message = MIMEText(body_text)
    message['to'] = to_email
    message['from'] = os.getenv("FROM_EMAIL")
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(to_email: str, subject: str, body_text: str):
    service = get_gmail_service()
    message = create_message(to_email, subject, body_text)
    sent_message = service.users().messages().send(userId='me', body=message).execute()
    return sent_message