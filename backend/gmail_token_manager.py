"""
Gmail Token Manager for TechCorp AI Customer Support
Handles token refresh and management for Gmail API
"""

import os
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class GmailTokenManager:
    def __init__(self, token_file='gmail_token.pickle'):
        self.token_file = token_file

    def load_credentials(self):
        """Load existing credentials from file"""
        creds = None
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        return creds

    def save_credentials(self, creds):
        """Save credentials to file"""
        with open(self.token_file, 'wb') as token:
            pickle.dump(creds, token)

    def refresh_if_needed(self):
        """Refresh the access token if it's expired"""
        creds = self.load_credentials()

        if not creds:
            print("No credentials found. Please run gmail_setup.py first.")
            return None

        if not creds.valid:
            if creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    self.save_credentials(creds)
                    print("Access token refreshed successfully")
                    return creds
                except Exception as e:
                    print(f"Error refreshing token: {str(e)}")
                    print("You may need to re-authenticate by running gmail_setup.py")
                    return None
            else:
                print("Credentials invalid and cannot be refreshed. Please re-authenticate.")
                return None
        else:
            return creds

    def get_access_token(self):
        """Get a valid access token"""
        creds = self.refresh_if_needed()
        if creds:
            return creds.token
        return None

    def is_token_valid(self):
        """Check if the token is valid and not expired"""
        creds = self.load_credentials()
        if not creds:
            return False
        return creds.valid

# Global token manager instance
token_manager = GmailTokenManager()

def get_valid_credentials():
    """Get valid credentials for API calls"""
    return token_manager.refresh_if_needed()

def refresh_gmail_token():
    """Manually refresh the Gmail token"""
    return token_manager.refresh_if_needed()

def check_token_status():
    """Check the status of the stored token"""
    creds = token_manager.load_credentials()
    if not creds:
        print("No stored credentials found.")
        return

    print(f"Token valid: {creds.valid}")
    print(f"Token expiry: {creds.expiry if hasattr(creds, 'expiry') else 'Unknown'}")

    if creds.expired:
        print("Token is expired.")
    else:
        time_to_expiry = creds.expiry - datetime.now() if hasattr(creds, 'expiry') else None
        if time_to_expiry:
            print(f"Time to expiry: {time_to_expiry}")
