#!/usr/bin/env python3
"""
Quick diagnosis to check why emails aren't getting responses
"""

import requests
import os
from dotenv import load_dotenv

def check_system_status():
    """Check if the system is running and responding"""
    print("Checking system status...")

    try:
        # Check if server is running
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("SUCCESS: Backend server is running")
            return True
        else:
            print("ERROR: Backend server is not responding")
            return False
    except:
        print("ERROR: Backend server is not running")
        print("   Please start it with: python -c \"import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8000)\"")
        return False

def check_env_config():
    """Check email configuration"""
    print("\nChecking email configuration...")

    load_dotenv()

    email_username = os.getenv("EMAIL_USERNAME", "")
    email_password = os.getenv("EMAIL_PASSWORD", "")

    if email_username and email_password:
        print(f"SUCCESS: Email username configured: {email_username}")
        print(f"SUCCESS: Email password is set (length: {len(email_password)})")
        return True
    else:
        print("ERROR: Email configuration missing!")
        print("   Make sure your .env file has:")
        print("   EMAIL_USERNAME=aimoshahs@gmail.com")
        print("   EMAIL_PASSWORD=your_app_password")
        return False

def check_dashboard():
    """Check dashboard stats"""
    print("\nChecking dashboard stats...")

    try:
        response = requests.get("http://localhost:8000/api/dashboard/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print(f"SUCCESS: Dashboard accessible")
            print(f"   Total tickets: {stats.get('total_tickets', 0)}")
            print(f"   Active conversations: {stats.get('active_conversations', 0)}")
            print(f"   Escalations: {stats.get('escalations', 0)}")
            return True
        else:
            print("ERROR: Dashboard not accessible")
            return False
    except:
        print("ERROR: Cannot access dashboard")
        return False

def trigger_webhook_and_check():
    """Trigger webhook and see what happens"""
    print("\nTesting webhook trigger...")

    try:
        response = requests.post("http://localhost:8000/webhooks/gmail", timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"SUCCESS: Webhook triggered successfully")
            print(f"   Response: {result}")

            # Check if any emails were processed
            if "processed" in str(result).lower():
                processed_count = 0
                if "processed" in result.get('message', ''):
                    import re
                    matches = re.findall(r'(\d+)\s+new\s+message', result.get('message', ''))
                    if matches:
                        processed_count = int(matches[0])

                if processed_count > 0:
                    print(f"   SUCCESS: {processed_count} email(s) were processed")
                else:
                    print(f"   INFO: No new emails were found to process")
                    print(f"   INFO: This means no unread emails were in the inbox")

            return True
        else:
            print(f"ERROR: Webhook failed with status: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"ERROR: Webhook trigger failed: {str(e)}")
        return False

def main():
    print("QUICK DIAGNOSIS - Why You're Not Getting Email Responses")
    print("=" * 60)

    # Run all checks
    server_ok = check_system_status()
    env_ok = check_env_config()
    dashboard_ok = check_dashboard()

    if server_ok and env_ok:
        print(f"\n{'='*60}")
        print("TESTING EMAIL PROCESSING...")
        print("=" * 60)

        # Trigger webhook to see if it processes emails
        webhook_ok = trigger_webhook_and_check()

        print(f"\n{'='*60}")
        print("DIAGNOSIS RESULTS:")
        print("=" * 60)

        if server_ok:
            print("SUCCESS: Backend server: Running")
        if env_ok:
            print("SUCCESS: Email configuration: Present")
        if dashboard_ok:
            print("SUCCESS: Dashboard: Accessible")
        if webhook_ok:
            print("SUCCESS: Webhook: Working")

        print(f"\n{'='*60}")
        print("POSSIBLE ISSUES:")
        print("=" * 60)

        if server_ok and env_ok and webhook_ok:
            print("1. No unread emails in aimoshahs@gmail.com inbox")
            print("2. Email was already read/processed before")
            print("3. Escalation keywords in your email (responses go to humans)")
            print("4. SMTP settings preventing outbound replies")

        print(f"\n{'='*60}")
        print("TO FIX: Send a new email and IMMEDIATELY trigger the webhook!")
        print("1. Send email to aimoshahs@gmail.com")
        print("2. Run: curl -X POST http://localhost:8000/webhooks/gmail")
        print("3. Wait 1-2 minutes for response")

    else:
        print("\n❌ Fix the above issues first before testing email processing!")

if __name__ == "__main__":
    main()
