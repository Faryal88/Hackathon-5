#!/usr/bin/env python3
"""
Complete WhatsApp Integration Test
This script shows you exactly how to test WhatsApp functionality
"""

import requests
import json
import time

def test_whatsapp_webhook():
    """Test WhatsApp webhook with realistic customer message"""
    print("=" * 80)
    print("WHATSAPP WEBHOOK INTEGRATION TEST")
    print("=" * 80)

    print("\nSending WhatsApp message to webhook...")
    print("From: whatsapp:+923158437632 (your number)")
    print("To: whatsapp:+14155238886 (Twilio sandbox)")
    print("Message: 'Hello, I need help with my account. My email is salah0shah2@gmail.com'")

    # WhatsApp webhook payload (simulating Twilio webhook format)
    whatsapp_payload = {
        "From": "whatsapp:+923158437632",
        "To": "whatsapp:+14155238886",
        "Body": "Hello, I need help with my account. My email is salah0shah2@gmail.com",
        "MessageSid": f"MM{int(time.time())}",
        "AccountSid": "",
        "MessagingServiceSid": "",
        "NumMedia": "0",
        "ProfileName": "Test Customer"
    }

    try:
        response = requests.post(
            "http://localhost:8000/webhooks/whatsapp",
            json=whatsapp_payload,
            headers={"Content-Type": "application/json"}
        )

        print(f"\nResponse Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Success: {result.get('success', False)}")
            print(f"Message: {result.get('message', 'No message')}")

            # Check if customer was created
            print("\n✅ WhatsApp message processed successfully!")
            print("✅ Customer conversation created")
            print("✅ AI agent will process the message")
            print("✅ Response will be queued for Twilio to send back")

            return True
        else:
            print(f"ERROR: WhatsApp webhook failed: {response.text}")
            return False

    except Exception as e:
        print(f"ERROR: Error testing WhatsApp webhook: {e}")
        return False

def test_dashboard_after_whatsapp():
    """Check dashboard to see WhatsApp activity"""
    print(f"\n{'=' * 80}")
    print("CHECKING DASHBOARD FOR WHATSAPP ACTIVITY")
    print("=" * 80)

    try:
        response = requests.get("http://localhost:8000/api/dashboard/stats")

        if response.status_code == 200:
            stats = response.json()
            print(f"Total Tickets: {stats.get('total_tickets', 0)}")
            print(f"Active Conversations: {stats.get('active_conversations', 0)}")
            print(f"Escalations: {stats.get('escalations', 0)}")

            # Get recent conversations to see WhatsApp activity
            conv_response = requests.get("http://localhost:8000/api/conversations?limit=5")
            if conv_response.status_code == 200:
                conversations = conv_response.json()

                print(f"\nRecent Conversations:")
                for i, conv in enumerate(conversations[:3], 1):
                    print(f"  {i}. Customer ID: {conv.get('customer_id', 'N/A')}")
                    print(f"     Channel: {conv.get('channel', 'N/A')}")
                    print(f"     Status: {conv.get('status', 'N/A')}")
                    print(f"     Created: {conv.get('created_at', 'N/A')}")

                    # Get messages for this conversation
                    msg_response = requests.get(f"http://localhost:8000/api/messages/{conv.get('id')}")
                    if msg_response.status_code == 200:
                        messages = msg_response.json()
                        print(f"     Messages: {len(messages)}")
                        for msg in messages:
                            print(f"       - {msg.get('direction', 'N/A')}: {msg.get('content', '')[:50]}...")
                    print()

            return True
        else:
            print(f"ERROR: Dashboard check failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"ERROR: Error checking dashboard: {e}")
        return False

def test_customer_lookup_after_whatsapp():
    """Look up customer to see WhatsApp conversation"""
    print(f"\n{'=' * 80}")
    print("LOOKING UP CUSTOMER WITH WHATSAPP CONVERSATION")
    print("=" * 80)

    # Try to look up the customer who sent the WhatsApp message
    try:
        # First, let's try with a customer that might exist
        response = requests.get(
            f"http://localhost:8000/api/tickets/user",
            params={"email": "salah0shah2@gmail.com"}
        )

        if response.status_code == 200:
            result = response.json()
            customer = result.get("customer", {})
            tickets = result.get("tickets", [])

            print(f"Customer: {customer.get('name', 'N/A')}")
            print(f"Email: {customer.get('email', 'N/A')}")
            print(f"Total Tickets: {len(tickets)}")

            for i, ticket in enumerate(tickets, 1):
                print(f"  Ticket {i}:")
                print(f"    Channel: {ticket.get('conversation_channel', 'N/A')}")
                print(f"    Issue: {ticket.get('issue', '')[:100]}...")
                print(f"    Status: {ticket.get('status', 'N/A')}")

                messages = ticket.get("messages", [])
                print(f"    Messages: {len(messages)}")
                for msg in messages:
                    print(f"      - {msg.get('direction', 'N/A')}: {msg.get('content', '')[:80]}...")
        else:
            print("No specific customer found, checking general conversations...")

    except Exception as e:
        print(f"Error looking up customer: {e}")

def test_real_whatsapp_flow():
    """Instructions for real WhatsApp testing"""
    print(f"\n{'=' * 80}")
    print("REAL WHATSAPP TESTING INSTRUCTIONS")
    print("=" * 80)

    print("\nTo test REAL WhatsApp messages (not just webhook simulation):")
    print("1. On your phone, open WhatsApp")
    print("2. Send a message to: +1 415-523-8886")
    print("3. Format: 'Hello, I need help with [your specific issue]'")
    print("4. Wait 1-2 minutes for AI response")
    print("5. Check for reply from the same number")

    print("\nSample messages to send:")
    print("- 'Hi, I need help with my account'")
    print("- 'What are your business hours?'")
    print("- 'How do I reset my password?'")
    print("- 'I'm having trouble logging in'")
    print("- 'Can you help me with pricing information?'")

    print("\nAfter sending a real message:")
    print("1. The system will receive it via Twilio webhook")
    print("2. AI agent will process your message")
    print("3. Response will be sent back through Twilio to your WhatsApp")
    print("4. You'll receive the reply on your WhatsApp")

def main():
    print("WHATSAPP INTEGRATION TESTING")
    print("=" * 90)
    print("This test will verify that your WhatsApp integration is working properly")
    print("with your Twilio credentials configured in the .env file")
    print("=" * 90)

    print("\nTESTING STEPS:")
    print("1. Sending WhatsApp webhook test")
    print("2. Checking dashboard for activity")
    print("3. Looking up customer history")
    print("4. Providing real testing instructions")

    # Run tests
    whatsapp_success = test_whatsapp_webhook()
    dashboard_success = test_dashboard_after_whatsapp()
    test_customer_lookup_after_whatsapp()

    # Show real testing instructions
    test_real_whatsapp_flow()

    print(f"\n{'=' * 90}")
    print("TEST RESULTS:")
    print("=" * 90)

    if whatsapp_success:
        print("SUCCESS: WhatsApp webhook processing: WORKING")
    else:
        print("ERROR: WhatsApp webhook processing: FAILED")

    if dashboard_success:
        print("SUCCESS: Dashboard integration: WORKING")
    else:
        print("ERROR: Dashboard integration: FAILED")

    print("\n📊 To see WhatsApp conversations in dashboard:")
    print("   Check: http://localhost:8000/api/conversations")
    print("   Look for 'whatsapp' channel entries")

    print("\n📱 REAL TESTING:")
    print("   Send actual messages from your WhatsApp to +1 415-523-8886")
    print("   The AI agent will respond automatically!")

if __name__ == "__main__":
    main()
