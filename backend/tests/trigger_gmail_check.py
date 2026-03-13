#!/usr/bin/env python3
"""
Script to trigger Gmail webhook and check for new emails
"""

import requests
import time

def trigger_gmail_check():
    """Trigger the Gmail webhook to check for new emails"""
    print("Triggering Gmail webhook to check for new emails...")

    try:
        # Call the Gmail webhook endpoint
        response = requests.post(
            "http://localhost:8000/webhooks/gmail",
            headers={"Content-Type": "application/json"}
        )

        print(f"Response Status: {response.status_code}")
        print(f"Response Data: {response.json()}")

        if response.status_code == 200:
            print("SUCCESS: Gmail webhook triggered successfully!")
            print("The system is now checking for new emails via IMAP...")
        else:
            print(f"FAILED: Failed to trigger Gmail webhook. Status: {response.status_code}")

    except Exception as e:
        print(f"❌ Error triggering Gmail webhook: {e}")
        print("Make sure the server is running on http://localhost:8000")

def check_dashboard_stats():
    """Check dashboard statistics to see if emails were processed"""
    print("\n📊 Checking dashboard statistics...")

    try:
        response = requests.get("http://localhost:8000/api/dashboard/stats")
        print(f"Dashboard Status: {response.status_code}")

        if response.status_code == 200:
            stats = response.json()
            print(f"Total Tickets: {stats.get('total_tickets', 0)}")
            print(f"Active Conversations: {stats.get('active_conversations', 0)}")
            print(f"Escalations: {stats.get('escalations', 0)}")
            print("SUCCESS: Dashboard stats retrieved successfully!")
        else:
            print(f"FAILED: Failed to get dashboard stats. Status: {response.status_code}")

    except Exception as e:
        print(f"FAILED: Error getting dashboard stats: {e}")

def main():
    print("Gmail Webhook Trigger Tool")
    print("=" * 50)
    print("This script will trigger the Gmail webhook to check for new emails")
    print("and then check the dashboard for updates.")
    print()

    # Trigger Gmail check
    trigger_gmail_check()

    # Wait a moment for processing
    print("\nWaiting 5 seconds for email processing...")
    time.sleep(5)

    # Check dashboard stats
    check_dashboard_stats()

    print("\n💡 Note: The email polling runs automatically every 5 minutes,")
    print("but you can manually trigger it using this webhook endpoint.")
    print("Make sure your email credentials are properly configured in .env")

if __name__ == "__main__":
    main()
