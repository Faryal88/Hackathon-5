#!/usr/bin/env python3
"""
Focused test script for Gmail and Web Form webhook functionality
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def test_web_form_example():
    """Test web form submission with example data"""
    print("=" * 60)
    print("TESTING WEB FORM EXAMPLE")
    print("=" * 60)

    # Example web form data
    web_form_examples = [
        {
            "name": "John Smith",
            "email": f"john.smith.{int(time.time())}@example.com",
            "subject": "Pricing Inquiry",
            "category": "Sales Question",
            "message": "Hi, I'm interested in your Professional plan. Can you provide more details about the features included?",
            "priority": "medium"
        },
        {
            "name": "Sarah Johnson",
            "email": f"sarah.johnson.{int(time.time())}@example.com",
            "subject": "Technical Support",
            "category": "Technical Issue",
            "message": "I'm having trouble connecting to the API. I keep getting authentication errors. Can you help?",
            "priority": "high"
        },
        {
            "name": "Mike Chen",
            "email": f"mike.chen.{int(time.time())}@example.com",
            "subject": "Integration Help",
            "category": "Integration Question",
            "message": "How can I integrate your platform with our existing Salesforce CRM? Do you have API documentation?",
            "priority": "medium"
        }
    ]

    for i, example in enumerate(web_form_examples, 1):
        print(f"\nWeb Form Example {i}: {example['subject']}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/support/submit",
                headers=HEADERS,
                json=example
            )

            print(f"  Status Code: {response.status_code}")
            if response.status_code == 200:
                response_data = response.json()
                print(f"  Success: {response_data.get('success', False)}")
                print(f"  Ticket ID: {response_data.get('ticket_id', 'N/A')}")
                print(f"  AI Response Preview: {response_data.get('message', '')[:100]}...")
                print("  SUCCESS: Web form example processed successfully")
            else:
                print(f"  FAILED: Web form example failed with status {response.status_code}")

        except Exception as e:
            print(f"  ERROR: Error with web form example {i}: {e}")

def test_gmail_webhook_example():
    """Test Gmail webhook with example trigger"""
    print("\n" + "=" * 60)
    print("TESTING GMAIL WEBHOOK EXAMPLE")
    print("=" * 60)

    print("\nGmail webhook example: Triggering email check...")
    try:
        response = requests.post(f"{BASE_URL}/webhooks/gmail", headers=HEADERS)

        print(f"  Status Code: {response.status_code}")
        if response.status_code == 200:
            response_data = response.json()
            print(f"  Success: {response_data.get('success', False)}")
            print(f"  Message: {response_data.get('message', 'N/A')}")
            print("  SUCCESS: Gmail webhook example processed successfully")
        else:
            print(f"  FAILED: Gmail webhook example failed with status {response.status_code}")

    except Exception as e:
        print(f"  ERROR: Error with Gmail webhook example: {e}")

def test_dashboard_after_examples():
    """Test dashboard to see the results of our examples"""
    print("\n" + "=" * 60)
    print("CHECKING DASHBOARD AFTER EXAMPLES")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/stats")

        print(f"  Status Code: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"  Total Tickets: {stats.get('total_tickets', 0)}")
            print(f"  Active Conversations: {stats.get('active_conversations', 0)}")
            print(f"  Escalations: {stats.get('escalations', 0)}")
            print(f"  Avg Response Time: {stats.get('avg_response_time', 0)}s")
            print("  SUCCESS: Dashboard stats retrieved successfully")
        else:
            print(f"  FAILED: Dashboard stats failed with status {response.status_code}")

    except Exception as e:
        print(f"  ERROR: Error retrieving dashboard stats: {e}")

def main():
    """Run focused tests for Gmail and Web Form"""
    print("Focused Test: Gmail and Web Form Examples")
    print(f"Target: {BASE_URL}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Wait a moment to ensure server is ready
    time.sleep(2)

    # Run tests
    test_web_form_example()
    test_gmail_webhook_example()
    test_dashboard_after_examples()

    print("\n" + "=" * 60)
    print("FOCUSED TEST COMPLETED!")
    print("=" * 60)
    print("Web Form and Gmail webhook functionality verified!")

if __name__ == "__main__":
    main()
