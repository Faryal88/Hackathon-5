import asyncio
import json
import requests
from datetime import datetime

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            return True
        else:
            print("Health check failed")
            return False
    except Exception as e:
        print(f"Health check error: {e}")
        return False

def test_submit_support_request():
    """Test submitting a support request"""
    try:
        test_data = {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "subject": "Test Support Request",
            "category": "Technical Issue",
            "message": "This is a test message for the support system.",
            "priority": "medium"
        }

        response = requests.post(
            "http://localhost:8000/api/support/submit",
            headers={"Content-Type": "application/json"},
            json=test_data
        )

        if response.status_code == 200:
            result = response.json()
            print(f"Support request submitted successfully")
            print(f"  Ticket ID: {result.get('ticket_id')}")
            return True
        else:
            print(f"Failed to submit support request: {response.text}")
            return False
    except Exception as e:
        print(f"Support request test error: {e}")
        return False

def test_get_dashboard_stats():
    """Test getting dashboard statistics"""
    try:
        response = requests.get("http://localhost:8000/api/dashboard/stats")

        if response.status_code == 200:
            stats = response.json()
            print("Dashboard stats retrieved successfully")
            print(f"  Total Tickets: {stats['total_tickets']}")
            print(f"  Active Conversations: {stats['active_conversations']}")
            print(f"  Escalations: {stats['escalations']}")
            print(f"  Avg Response Time: {stats['avg_response_time']}s")
            return True
        else:
            print(f"Failed to get dashboard stats: {response.text}")
            return False
    except Exception as e:
        print(f"Dashboard stats test error: {e}")
        return False

def test_get_conversations():
    """Test getting conversations"""
    try:
        response = requests.get("http://localhost:8000/api/conversations")

        if response.status_code == 200:
            conversations = response.json()
            print(f"Retrieved {len(conversations)} conversations")
            return True
        else:
            print(f"Failed to get conversations: {response.text}")
            return False
    except Exception as e:
        print(f"Conversations test error: {e}")
        return False

def run_tests():
    """Run all backend tests"""
    print("Running TechCorp AI Support Backend Tests...\n")

    tests = [
        test_health_check,
        test_submit_support_request,
        test_get_dashboard_stats,
        test_get_conversations
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("\nAll tests passed!")
    else:
        print(f"\n{total - passed} test(s) failed")

if __name__ == "__main__":
    run_tests()
