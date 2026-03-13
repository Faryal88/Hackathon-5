#!/usr/bin/env python3
"""
Specific test examples for Gmail and Web Form functionality
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def send_web_form_examples():
    """Send specific web form examples"""
    print("=" * 70)
    print("SENDING WEB FORM EXAMPLES")
    print("=" * 70)

    # Example 1: Pricing Inquiry
    print("\n📝 Example 1: Pricing Inquiry")
    pricing_inquiry = {
        "name": "Alex Johnson",
        "email": f"alex.johnson.{int(time.time())}@company.com",
        "subject": "Pricing Information Request",
        "category": "Sales Question",
        "message": "Hello, I'm interested in your AI analytics platform. Could you please provide detailed information about your Professional and Enterprise pricing plans? I need to know about user limits, data processing capacity, and API rate limits.",
        "priority": "medium"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/support/submit", json=pricing_inquiry, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result['success']}")
            print(f"   Ticket ID: {result.get('ticket_id', 'N/A')}")
            print(f"   AI Response: {result['message'][:100]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error connecting to server: {e}")

    # Example 2: Technical Support
    print("\n🔧 Example 2: Technical Support Request")
    tech_support = {
        "name": "Maria Garcia",
        "email": f"maria.garcia.{int(time.time())}@techcorp.com",
        "subject": "API Connection Issues",
        "category": "Technical Support",
        "message": "I'm experiencing difficulties connecting to your API. I keep receiving authentication errors despite using the correct API key. The error message says 'Invalid API key'. Could you please help troubleshoot this issue?",
        "priority": "high"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/support/submit", json=tech_support, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result['success']}")
            print(f"   Ticket ID: {result.get('ticket_id', 'N/A')}")
            print(f"   AI Response: {result['message'][:100]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error connecting to server: {e}")

    # Example 3: Integration Question
    print("\n🔗 Example 3: Integration Question")
    integration_q = {
        "name": "David Kim",
        "email": f"david.kim.{int(time.time())}@business.com",
        "subject": "Salesforce Integration Help",
        "category": "Integration Question",
        "message": "We want to integrate your platform with our Salesforce CRM. Do you have a step-by-step guide for this integration? Also, what permissions are required and how often does the data sync occur?",
        "priority": "medium"
    }

    try:
        response = requests.post(f"{BASE_URL}/api/support/submit", json=integration_q, headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result['success']}")
            print(f"   Ticket ID: {result.get('ticket_id', 'N/A')}")
            print(f"   AI Response: {result['message'][:100]}...")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error connecting to server: {e}")

def trigger_gmail_webhook():
    """Trigger the Gmail webhook"""
    print("\n" + "=" * 70)
    print("TRIGGERING GMAIL WEBHOOK")
    print("=" * 70)

    print("\n📧 Gmail Webhook Trigger:")
    print("   Action: Manual trigger to check for new emails via IMAP")
    print("   Endpoint: POST /webhooks/gmail")

    try:
        response = requests.post(f"{BASE_URL}/webhooks/gmail", headers=HEADERS)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Success: {result['success']}")
            print(f"   Message: {result['message']}")
            print("   This triggers the email polling mechanism to check for new emails")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   Error connecting to server: {e}")

def check_system_status():
    """Check system status"""
    print("\n" + "=" * 70)
    print("SYSTEM STATUS CHECK")
    print("=" * 70)

    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health Check Error: {e}")

    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"Dashboard Stats: {stats}")
        else:
            print(f"Dashboard Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Dashboard Check Error: {e}")

def main():
    """Main function to send examples"""
    print("🚀 TechCorp AI Customer Support - Gmail & Web Form Examples")
    print(f"Target: {BASE_URL}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n💡 This script demonstrates:")
    print("   • Web form submissions with realistic customer inquiries")
    print("   • AI agent processing and response generation")
    print("   • Gmail webhook triggering for email processing")
    print("   • Ticket creation and conversation management")

    # Check if server is running
    print("\n🔍 Checking server connectivity...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"   ✓ Server is accessible - Status: {response.status_code}")
    except:
        print(f"   ✗ Server is not accessible at {BASE_URL}")
        print("   Please start the server with: uvicorn main:app --host 0.0.0.0 --port 8000")
        return

    # Run examples
    send_web_form_examples()
    trigger_gmail_webhook()
    check_system_status()

    print("\n" + "=" * 70)
    print("EXAMPLE EXECUTION COMPLETE!")
    print("=" * 70)
    print("These examples demonstrate the full functionality of the TechCorp AI")
    print("Customer Support system for both web form submissions and email processing.")

if __name__ == "__main__":
    main()
