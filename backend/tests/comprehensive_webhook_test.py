#!/usr/bin/env python3
"""
Comprehensive test script for TechCorp AI Customer Support webhooks and AI agent responses.
Tests Gmail, WhatsApp, Web Form, and AI agent functionality.
"""

import requests
import json
import time
import asyncio
from datetime import datetime
import os
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def test_health_check():
    """Test the health check endpoint"""
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("SUCCESS: Health check passed")
        else:
            print("FAILED: Health check failed")

    except Exception as e:
        print(f"ERROR: Error during health check: {e}")

    print()

def test_web_form_webhook():
    """Test the web form webhook endpoint"""
    print("=" * 60)
    print("TEST 2: Web Form Webhook (/api/support/submit)")
    print("=" * 60)

    # Sample support request data
    sample_data = {
        "name": "Test User Web Form",
        "email": f"test.webform.{int(time.time())}@example.com",
        "subject": "Web Form Test Inquiry",
        "category": "General Support",
        "message": "This is a test message from the web form webhook. Testing the AI agent response functionality.",
        "priority": "medium"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/support/submit",
            headers=HEADERS,
            json=sample_data
        )

        print(f"Status Code: {response.status_code}")
        print(f"Request Data: {json.dumps(sample_data, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200 and response.json().get("success"):
            print("SUCCESS: Web form webhook test passed")
            return response.json()
        else:
            print("FAILED: Web form webhook test failed")

    except Exception as e:
        print(f"ERROR: Error during web form webhook test: {e}")

    print()

def test_gmail_webhook():
    """Test the Gmail webhook endpoint (manual trigger)"""
    print("=" * 60)
    print("TEST 3: Gmail Webhook (/webhooks/gmail)")
    print("=" * 60)

    try:
        # This endpoint triggers manual email checking
        response = requests.post(f"{BASE_URL}/webhooks/gmail", headers=HEADERS)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("SUCCESS: Gmail webhook test passed (triggered)")
        else:
            print("FAILED: Gmail webhook test failed")

    except Exception as e:
        print(f"ERROR: Error during Gmail webhook test: {e}")

    print()

def test_whatsapp_webhook():
    """Test the WhatsApp webhook endpoint"""
    print("=" * 60)
    print("TEST 4: WhatsApp Webhook (/webhooks/whatsapp)")
    print("=" * 60)

    # Sample Twilio webhook payload for WhatsApp
    whatsapp_payload = {
        "From": "whatsapp:+1234567890",
        "To": "whatsapp:+0987654321",
        "Body": "This is a test message from WhatsApp. Testing the AI agent response functionality.",
        "MessageSid": f"MM{int(time.time())}",
        "AccountSid": "ACxxxxxxxxxxxxx",
        "MessagingServiceSid": "MGxxxxxxxxxxxxx"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/webhooks/whatsapp",
            headers=HEADERS,
            json=whatsapp_payload
        )

        print(f"Status Code: {response.status_code}")
        print(f"Request Data: {json.dumps(whatsapp_payload, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200 and response.json().get("success"):
            print("SUCCESS: WhatsApp webhook test passed")
            return response.json()
        else:
            print("FAILED: WhatsApp webhook test failed")

    except Exception as e:
        print(f"ERROR: Error during WhatsApp webhook test: {e}")

    print()

def test_dashboard_stats():
    """Test the dashboard statistics endpoint"""
    print("=" * 60)
    print("TEST 5: Dashboard Statistics (/api/dashboard/stats)")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/api/dashboard/stats")

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            stats = response.json()
            print(f"Total Tickets: {stats.get('total_tickets', 0)}")
            print(f"Active Conversations: {stats.get('active_conversations', 0)}")
            print(f"Escalations: {stats.get('escalations', 0)}")
            print(f"Avg Response Time: {stats.get('avg_response_time', 0)}s")
            print("SUCCESS: Dashboard stats test passed")
        else:
            print("FAILED: Dashboard stats test failed")

    except Exception as e:
        print(f"ERROR: Error during dashboard stats test: {e}")

    print()

def test_conversations_list():
    """Test the conversations list endpoint"""
    print("=" * 60)
    print("TEST 6: Conversations List (/api/conversations)")
    print("=" * 60)

    try:
        response = requests.get(f"{BASE_URL}/api/conversations?limit=10")

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json()[:3], indent=2)}")  # Show first 3

        if response.status_code == 200:
            conversations = response.json()
            print(f"Number of conversations retrieved: {len(conversations)}")
            print("SUCCESS: Conversations list test passed")
        else:
            print("FAILED: Conversations list test failed")

    except Exception as e:
        print(f"ERROR: Error during conversations list test: {e}")

    print()

def test_ai_agent_directly():
    """Test the AI agent functionality directly"""
    print("=" * 60)
    print("TEST 7: AI Agent Direct Test")
    print("=" * 60)

    # Submit a web form to trigger AI processing
    sample_data = {
        "name": "AI Agent Test User",
        "email": f"ai.test.{int(time.time())}@example.com",
        "subject": "AI Agent Test",
        "category": "Technical Support",
        "message": "What are your pricing plans?",
        "priority": "medium"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/support/submit",
            headers=HEADERS,
            json=sample_data
        )

        print(f"Status Code: {response.status_code}")
        print(f"Request Data: {json.dumps(sample_data, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200 and response.json().get("success"):
            print("SUCCESS: AI agent direct test passed")

            # Check if response contains pricing information
            response_text = response.json().get("message", "")
            if "pricing" in response_text.lower() or "$" in response_text:
                print("SUCCESS: AI agent correctly responded with pricing information")
            else:
                print("WARNING: AI agent response doesn't seem to contain pricing info")

            return response.json()
        else:
            print("FAILED: AI agent direct test failed")

    except Exception as e:
        print(f"ERROR: Error during AI agent direct test: {e}")

    print()

def test_knowledge_base_query():
    """Test knowledge base querying through web form"""
    print("=" * 60)
    print("TEST 8: Knowledge Base Query Test")
    print("=" * 60)

    # Test various knowledge base queries
    test_queries = [
        {"message": "How do I integrate with Salesforce?", "expected": "integration"},
        {"message": "What security measures do you have?", "expected": "security"},
        {"message": "Can I upgrade my plan?", "expected": "upgrade"},
        {"message": "How long is data retention?", "expected": "retention"}
    ]

    for i, query_data in enumerate(test_queries, 1):
        print(f"\nSub-test {i}: {query_data['message']}")

        sample_data = {
            "name": f"KB Test User {i}",
            "email": f"kb.test.{int(time.time())}.{i}@example.com",
            "subject": f"KB Test {i}",
            "category": "Knowledge Base Query",
            "message": query_data["message"],
            "priority": "medium"
        }

        try:
            response = requests.post(
                f"{BASE_URL}/api/support/submit",
                headers=HEADERS,
                json=sample_data
            )

            print(f"  Status Code: {response.status_code}")

            if response.status_code == 200:
                response_text = response.json().get("message", "")
                print(f"  Response Preview: {response_text[:100]}...")

                if query_data["expected"].lower() in response_text.lower():
                    print(f"  SUCCESS: Correctly answered {query_data['expected']} question")
                else:
                    print(f"  WARNING: Did not find {query_data['expected']} in response")
            else:
                print(f"  FAILED: Failed to get response for {query_data['message']}")

        except Exception as e:
            print(f"  ERROR: Error during KB test {i}: {e}")

    print()

def test_escalation_handling():
    """Test escalation handling"""
    print("=" * 60)
    print("TEST 9: Escalation Handling Test")
    print("=" * 60)

    # Test message that should trigger escalation
    escalation_message = "I need to speak with someone about canceling my contract due to a legal dispute with your billing department."

    sample_data = {
        "name": "Escalation Test User",
        "email": f"escalation.test.{int(time.time())}@example.com",
        "subject": "Escalation Test",
        "category": "Legal/Contract Issue",
        "message": escalation_message,
        "priority": "high"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/support/submit",
            headers=HEADERS,
            json=sample_data
        )

        print(f"Status Code: {response.status_code}")
        print(f"Request Data: {json.dumps(sample_data, indent=2)}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            response_text = response.json().get("message", "")
            print(f"Response Preview: {response_text[:200]}...")

            if "escalat" in response_text.lower() or "human" in response_text.lower():
                print("SUCCESS: Correctly escalated to human agent")
            else:
                print("WARNING: May not have properly escalated (check if knowledge base matched first)")

            return response.json()
        else:
            print("FAILED: Escalation test failed")

    except Exception as e:
        print(f"ERROR: Error during escalation test: {e}")

    print()

def test_user_tickets():
    """Test user tickets endpoint"""
    print("=" * 60)
    print("TEST 10: User Tickets (/api/tickets/user)")
    print("=" * 60)

    # Use one of the emails we created during tests
    test_email = f"test.tickets.{int(time.time())}@example.com"

    # First, create a ticket by submitting a support request
    sample_data = {
        "name": "Tickets Test User",
        "email": test_email,
        "subject": "Tickets Test",
        "category": "General Inquiry",
        "message": "Testing user tickets endpoint.",
        "priority": "low"
    }

    try:
        # Create a ticket first
        create_response = requests.post(
            f"{BASE_URL}/api/support/submit",
            headers=HEADERS,
            json=sample_data
        )

        print(f"Created ticket with status: {create_response.status_code}")

        # Now test the user tickets endpoint
        params = {"email": test_email}
        response = requests.get(f"{BASE_URL}/api/tickets/user", params=params)

        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("SUCCESS: User tickets endpoint test passed")
        else:
            print("FAILED: User tickets endpoint test failed")

    except Exception as e:
        print(f"ERROR: Error during user tickets test: {e}")

    print()

def run_comprehensive_tests():
    """Run all tests in sequence"""
    print("Starting Comprehensive Webhook and AI Agent Tests")
    print(f"Target URL: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Wait a moment to ensure server is ready
    time.sleep(2)

    # Run all tests
    test_health_check()
    test_web_form_webhook()
    test_gmail_webhook()
    test_whatsapp_webhook()
    test_dashboard_stats()
    test_conversations_list()
    test_ai_agent_directly()
    test_knowledge_base_query()
    test_escalation_handling()
    test_user_tickets()

    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
    print("Please note:")
    print("- Some tests may fail if the server is not running on localhost:8000")
    print("- Gmail webhook requires proper email configuration")
    print("- WhatsApp webhook requires Twilio configuration")
    print("- AI agent requires OpenAI API key")

if __name__ == "__main__":
    run_comprehensive_tests()
