#!/usr/bin/env python3
"""
Debug script to check email connection and verify the system can access the inbox
"""

import os
import imaplib
import smtplib
from dotenv import load_dotenv

def check_env_variables():
    """Check if required environment variables are set"""
    print("Checking environment variables...")

    load_dotenv()

    required_vars = [
        'EMAIL_USERNAME',
        'EMAIL_PASSWORD',
        'EMAIL_IMAP_SERVER',
        'EMAIL_IMAP_PORT',
        'EMAIL_SMTP_SERVER',
        'EMAIL_SMTP_PORT'
    ]

    all_present = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  SUCCESS: {var}: {value[:10]}..." if len(value) > 10 else f"  SUCCESS: {var}: {value}")
        else:
            print(f"  ERROR: {var}: NOT SET")
            all_present = False

    return all_present

def test_imap_connection():
    """Test IMAP connection to verify email credentials work"""
    print("\nTesting IMAP connection...")

    load_dotenv()

    username = os.getenv("EMAIL_USERNAME", "aimoshahs@gmail.com")
    password = os.getenv("EMAIL_PASSWORD", "jzjw ikvw nctw xkkc")
    imap_server = os.getenv("EMAIL_IMAP_SERVER", "imap.gmail.com")
    imap_port = int(os.getenv("EMAIL_IMAP_PORT", "993"))

    try:
        print(f"  Connecting to {imap_server}:{imap_port}")
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        print("  Authenticating...")
        mail.login(username, password)

        print("  Selecting inbox...")
        mail.select('inbox')

        # Search for ALL emails (not just unseen)
        print("  Searching for emails...")
        status, messages = mail.search(None, 'ALL')

        if status == 'OK':
            email_ids = messages[0].split()
            print(f"  SUCCESS: Connected successfully!")
            print(f"  ✅ Found {len(email_ids)} total emails in inbox")

            # Get unseen emails specifically
            status_unseen, unseen_msgs = mail.search(None, 'UNSEEN')
            if status_unseen == 'OK':
                unseen_ids = unseen_msgs[0].split()
                print(f"  SUCCESS: Found {len(unseen_ids)} UNREAD emails")

                if unseen_ids:
                    print("  Latest unread emails:")
                    for i, eid in enumerate(unseen_ids[-3:]):  # Last 3 unread emails
                        typ, msg_data = mail.fetch(eid, '(RFC822.HEADER)')
                        if typ == 'OK':
                            import email
                            msg = email.message_from_bytes(msg_data[0][1])
                            subject = msg.get('Subject', 'No Subject')
                            sender = msg.get('From', 'Unknown Sender')
                            print(f"    {i+1}. From: {sender}, Subject: {subject}")

            mail.close()
            mail.logout()
            return True

    except Exception as e:
        print(f"  ERROR: IMAP connection failed: {str(e)}")
        print("  This could be due to:")
        print("  - Wrong email/password")
        print("  - 2FA not enabled with App Password")
        print("  - IMAP not enabled in Gmail settings")
        print("  - Network/firewall blocking the connection")
        return False

def test_smtp_connection():
    """Test SMTP connection for sending responses"""
    print("\nTesting SMTP connection...")

    load_dotenv()

    username = os.getenv("EMAIL_USERNAME", "aimoshahs@gmail.com")
    password = os.getenv("EMAIL_PASSWORD", "jzjw ikvw nctw xkkc")
    smtp_server = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        server.quit()
        print("  SUCCESS: SMTP connection successful!")
        return True

    except Exception as e:
        print(f"  ERROR: SMTP connection failed: {str(e)}")
        return False

def check_recent_emails():
    """Check for recent emails that might be processed"""
    print("\nChecking for recent emails that should be processed...")

    load_dotenv()

    username = os.getenv("EMAIL_USERNAME", "aimoshahs@gmail.com")
    password = os.getenv("EMAIL_PASSWORD", "jzjw ikvw nctw xkkc")
    imap_server = os.getenv("EMAIL_IMAP_SERVER", "imap.gmail.com")
    imap_port = int(os.getenv("EMAIL_IMAP_PORT", "993"))

    try:
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(username, password)
        mail.select('inbox')

        # Search for emails from your address
        status, messages = mail.search(None, f'FROM "salah0shah2@gmail.com"')

        if status == 'OK':
            email_ids = messages[0].split()
            if email_ids:
                print(f"  SUCCESS: Found {len(email_ids)} emails from salah0shah2@gmail.com")
                for i, eid in enumerate(email_ids[-5:]):  # Last 5 emails
                    typ, msg_data = mail.fetch(eid, '(RFC822.HEADER)')
                    if typ == 'OK':
                        import email
                        msg = email.message_from_bytes(msg_data[0][1])
                        subject = msg.get('Subject', 'No Subject')
                        date = msg.get('Date', 'Unknown Date')
                        print(f"    {i+1}. Subject: {subject}")
                        print(f"        Date: {date}")

                        # Check if this email is seen/unseen
                        typ, flags = mail.fetch(eid, '(FLAGS)')
                        if typ == 'OK':
                            flags_str = str(flags[0])
                            is_seen = '\\Seen' in flags_str
                            print(f"        Status: {'Unread' if not is_seen else 'Read'}")
            else:
                print("  ERROR: No emails found from salah0shah2@gmail.com")
                print("  Make sure you sent emails to the correct address: aimoshahs@gmail.com")

        mail.close()
        mail.logout()

    except Exception as e:
        print(f"  ERROR: Error checking recent emails: {str(e)}")

def main():
    print("Email Connection Debug Tool")
    print("=" * 50)
    print("This script will check if your email system is properly configured")
    print("and can access the inbox for processing emails.\n")

    # Check environment variables
    env_ok = check_env_variables()

    if not env_ok:
        print("\nERROR: Environment variables are not properly set!")
        print("Please make sure your .env file contains:")
        print("EMAIL_USERNAME=your_email@gmail.com")
        print("EMAIL_PASSWORD=your_app_password")
        print("EMAIL_IMAP_SERVER=imap.gmail.com")
        print("EMAIL_SMTP_SERVER=smtp.gmail.com")
        return

    # Test IMAP connection
    imap_ok = test_imap_connection()

    # Test SMTP connection
    smtp_ok = test_smtp_connection()

    # Check for recent emails
    check_recent_emails()

    print("\n" + "=" * 50)
    print("DIAGNOSIS RESULTS:")

    if imap_ok and smtp_ok:
        print("SUCCESS: Email system is properly configured and connected!")
        print("SUCCESS: The webhook should be able to process emails when triggered")
        print("\nTo process your emails:")
        print("1. Make sure you sent emails to aimoshahs@gmail.com")
        print("2. Trigger the webhook: curl -X POST http://localhost:8000/webhooks/gmail")
        print("3. Check the dashboard: http://localhost:8000/api/dashboard/stats")
    else:
        print("ERROR: Email system has connection issues that need to be fixed first")
        print("   before the webhook can process emails.")

if __name__ == "__main__":
    main()
