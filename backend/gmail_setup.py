"""
Gmail API Setup Utility for TechCorp AI Customer Support
This script helps set up Gmail API authentication and webhook subscription
"""

import os
import pickle
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.settings.basic',
    'https://www.googleapis.com/auth/gmail.readonly'
]

def setup_gmail_auth():
    """
    Set up Gmail API authentication
    """
    creds = None

    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use the credentials from environment variables
            client_config = {
                "installed": {
                    "client_id": os.getenv("GMAIL_CLIENT_ID"),
                    "project_id": "techcorp-ai-support",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": os.getenv("GMAIL_CLIENT_SECRET"),
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
                }
            }

            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def create_push_subscription(creds, topic_name=None):
    """
    Create a push subscription for Gmail notifications
    This requires setting up Cloud Pub/Sub, which is beyond the scope of this example
    """
    try:
        service = build('gmail', 'v1', credentials=creds)

        # Get the authenticated user's Gmail address
        profile = service.users().getProfile(userId='me').execute()
        email_address = profile['emailAddress']

        print(f"Setting up Gmail push notifications for: {email_address}")

        # Watch for new mail - this creates a push subscription
        # NOTE: This requires a configured Pub/Sub topic which would forward to your webhook
        watch_request = {
            'topicName': topic_name or f'projects/your-project-id/topics/gmail-notifications'
        }

        # This is where you would configure the actual push notification
        # For a complete implementation, you'd need to set up Google Cloud Pub/Sub
        print("Gmail push notification setup requires Google Cloud Pub/Sub configuration.")
        print("For testing purposes, you can manually sync emails periodically.")

        return email_address

    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def test_gmail_connection():
    """
    Test the Gmail connection and send a test email
    """
    try:
        creds = setup_gmail_auth()
        service = build('gmail', 'v1', credentials=creds)

        # Get user profile to verify connection
        profile = service.users().getProfile(userId='me').execute()
        print(f"Successfully connected to Gmail account: {profile['emailAddress']}")

        return service, profile['emailAddress']

    except Exception as e:
        print(f"Error connecting to Gmail: {str(e)}")
        return None, None

def send_test_email(service, to_email, subject="Test from TechCorp AI Support", body="This is a test email from the TechCorp AI Customer Support system."):
    """
    Send a test email to verify sending functionality
    """
    try:
        import base64
        from email.mime.text import MIMEText

        # Create message
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject

        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

        # Send message
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        print(f"Test email sent successfully! Message ID: {sent_message['id']}")
        return True

    except Exception as e:
        print(f"Error sending test email: {str(e)}")
        return False

def sync_recent_emails(service, max_results=5):
    """
    Sync recent emails (for testing without push notifications)
    """
    try:
        # Get recent messages
        results = service.users().messages().list(
            userId='me',
            maxResults=max_results,
            q='is:unread'  # Only unread messages
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            print("No new messages found.")
            return []

        print(f"Found {len(messages)} new messages:")

        emails = []
        for message in messages:
            msg = service.users().messages().get(
                userId='me',
                id=message['id'],
                format='full'
            ).execute()

            # Extract headers and body
            headers = {header['name']: header['value'] for header in msg['payload']['headers']}

            body = ""
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
            else:
                if 'body' in msg['payload'] and 'data' in msg['payload']['body']:
                    body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')

            email_data = {
                'id': message['id'],
                'from': headers.get('From', ''),
                'subject': headers.get('Subject', ''),
                'body': body,
                'date': headers.get('Date', '')
            }

            emails.append(email_data)
            print(f"  - From: {email_data['from']}, Subject: {email_data['subject']}")

        return emails

    except Exception as e:
        print(f"Error syncing emails: {str(e)}")
        return []

if __name__ == "__main__":
    print("TechCorp AI Customer Support - Gmail Setup Utility")
    print("=" * 50)

    # Check if required environment variables are set
    required_env_vars = ['GMAIL_CLIENT_ID', 'GMAIL_CLIENT_SECRET', 'GMAIL_REFRESH_TOKEN']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]

    if missing_vars:
        print(f"ERROR: Missing required environment variables: {missing_vars}")
        print("Please set these in your .env file before proceeding.")
        exit(1)

    print("All required environment variables are present.")

    # Test Gmail connection
    service, email_address = test_gmail_connection()

    if service:
        print(f"\nConnected to Gmail: {email_address}")

        # Optionally send a test email
        response = input("\nDo you want to send a test email? (y/n): ")
        if response.lower() == 'y':
            test_recipient = input("Enter recipient email address: ")
            send_test_email(service, test_recipient)

        # Optionally sync recent emails
        response = input("\nDo you want to sync recent emails? (y/n): ")
        if response.lower() == 'y':
            sync_recent_emails(service)

        print("\nGmail setup completed successfully!")
    else:
        print("\nFailed to connect to Gmail. Please check your credentials.")
