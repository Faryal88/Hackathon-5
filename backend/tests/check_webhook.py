#!/usr/bin/env python3
"""
Check if the webhook endpoint is accessible and working
"""

import requests
import time

def check_endpoints():
    """Check all endpoints to see which ones are working"""
    print("Checking all endpoints...")

    endpoints = [
        ("Health", "http://localhost:8000/health"),
        ("Root", "http://localhost:8000/"),
        ("Dashboard", "http://localhost:8000/api/dashboard/stats"),
        ("Conversations", "http://localhost:8000/api/conversations"),
        ("Gmail Webhook", "http://localhost:8000/webhooks/gmail"),
    ]

    for name, url in endpoints:
        try:
            if name == "Gmail Webhook":
                # Use POST for webhook
                response = requests.post(url, timeout=10)
            else:
                response = requests.get(url, timeout=10)

            print(f"SUCCESS: {name}: Status {response.status_code}")

            # For webhook, also check the response
            if name == "Gmail Webhook":
                try:
                    result = response.json()
                    print(f"   Response: {result}")
                except:
                    print(f"   Response: {response.text[:200]}...")

        except requests.exceptions.Timeout:
            print(f"ERROR: {name}: TIMEOUT (took more than 10 seconds)")
        except requests.exceptions.ConnectionError:
            print(f"ERROR: {name}: CONNECTION ERROR (server may not be listening)")
        except Exception as e:
            print(f"ERROR: {name}: ERROR - {str(e)}")

def test_simple_webhook():
    """Test the webhook with a simple approach"""
    print(f"\nTesting webhook with minimal timeout...")

    try:
        # Try with a very short timeout to see if it connects at all
        import socket

        # Test if we can establish a connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # 5 second timeout
        result = sock.connect_ex(('localhost', 8000))
        sock.close()

        if result == 0:
            print("SUCCESS: Port 8000 is open and accepting connections")
        else:
            print("ERROR: Port 8000 is not accessible")
            return

        # Now try the webhook
        print("Trying POST request to /webhooks/gmail...")

        # Use a session with specific timeout
        session = requests.Session()
        session.timeout = 10

        response = session.post(
            "http://localhost:8000/webhooks/gmail",
            timeout=10
        )

        print(f"SUCCESS: Webhook responded with status: {response.status_code}")
        print(f"Response: {response.text[:500]}")

    except requests.exceptions.Timeout:
        print("ERROR: Webhook request timed out - may be stuck in email processing")
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to webhook - server may not be listening on that endpoint")
    except Exception as e:
        print(f"ERROR: Webhook test failed: {str(e)}")
        print("   This could mean the email processing is hanging or there's an error in the code")

def check_server_logs():
    """Provide instructions for checking server logs"""
    print(f"\n📋 SERVER LOG INVESTIGATION:")
    print("If endpoints are not responding, check:")
    print("1. Is the server still running? Check with: ps aux | grep python")
    print("2. Are there any error messages in the server console?")
    print("3. Check if there are multiple server instances running")

def main():
    print("WEBHOOK CONNECTIVITY CHECK")
    print("=" * 50)

    print("This script will test if the webhook endpoint is accessible")
    print("and identify why it might not be responding.\n")

    check_endpoints()
    test_simple_webhook()
    check_server_logs()

    print(f"\n{'='*50}")
    print("TROUBLESHOOTING STEPS:")
    print("=" * 50)
    print("1. Restart the server if it's not responding")
    print("2. Check your .env file for correct email settings")
    print("3. Verify Gmail IMAP is enabled and using App Password")
    print("4. Make sure no firewall is blocking the connection")
    print("5. Try sending a test email and immediately trigger webhook")

if __name__ == "__main__":
    main()
