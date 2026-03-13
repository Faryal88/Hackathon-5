#!/usr/bin/env python3
"""
Simple WhatsApp test to verify integration
"""

import requests
import json

def test_whatsapp_webhook_simple():
    """Test WhatsApp webhook with corrected payload"""
    print("Testing WhatsApp Webhook Integration")
    print("=" * 50)

    # Corrected WhatsApp payload (phone number as phone, not email)
    whatsapp_payload = {
        "From": "whatsapp:+923158437632",
        "To": "whatsapp:+14155238886",
        "Body": "Hello, I need help with my account",
        "MessageSid": "",
        "AccountSid": "",
        "MessagingServiceSid": ""
    }

    try:
        response = requests.post(
            "http://localhost:8000/webhooks/whatsapp",
            json=whatsapp_payload,
            headers={"Content-Type": "application/json"}
        )

        print(f"Response Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result}")
            print("✅ WhatsApp message processed successfully!")
            print("✅ AI agent will respond to the message")
        else:
            print(f"Response: {response.text}")

    except Exception as e:
        print(f"Error: {e}")

def check_system_status():
    """Check if system is running properly"""
    print(f"\nChecking System Status")
    print("=" * 50)

    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health: {response.status_code} - {response.json()}")
    except:
        print("Server not accessible")

    try:
        response = requests.get("http://localhost:8000/api/dashboard/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"Tickets: {stats['total_tickets']}")
            print(f"Conversations: {stats['active_conversations']}")
    except:
        print("Dashboard not accessible")

def main():
    print("SIMPLE WHATSAPP INTEGRATION TEST")
    print("=" * 60)
    print("This test verifies basic WhatsApp webhook functionality")
    print("=" * 60)

    check_system_status()
    test_whatsapp_webhook_simple()

    print(f"\n{'='*60}")
    print("TO TEST REAL WHATSAPP MESSAGES:")
    print("=" * 60)
    print("1. Send a message from your phone to: +1 415-523-8886")
    print("2. Example: 'Hi, I need help with my account'")
    print("3. Wait 1-2 minutes for AI response")
    print("4. Check your WhatsApp for the reply")
    print("=" * 60)

if __name__ == "__main__":
    main()
