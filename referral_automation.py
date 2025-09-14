
from __future__ import print_function
import os.path
import base64
import pandas as pd
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Authenticate Gmail API and return service object"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, ask user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    """Create an email message"""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    """Send email via Gmail API"""
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent! Message Id: {message['id']}")
        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == '__main__':
    service = authenticate_gmail()

    # Load your CSV file
    df = pd.read_csv("employees.csv")   # <-- make sure your CSV has a column "email"

    for index, row in df.iterrows():
        recipient = row["email"]   # column name must match your CSV
        name = row["name"]         # optional, if you want personalization
        company = row["company"]   # optional

        email_message = create_message(
            sender="sapanadashoni@gmail.com",
            to=recipient,
            subject="Testing my automation application",
            message_text=f"Hi {name},\n\nMy {company} I just want to let you know that my brother made that move.\n\nThank you!"
        )


        send_message(service, 'me', email_message)
        print(f"✅ Email sent to {recipient}")
