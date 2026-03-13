#!/usr/bin/env python3
"""
Simple test runner for TechCorp AI Customer Support
This script starts the server and runs basic webhook tests
"""

import subprocess
import sys
import time
import threading
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")

    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import openai
        import requests
        print("All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Please install requirements using: pip install -r requirements.txt")
        return False

def start_server():
    """Start the FastAPI server in a separate thread"""
    print("Starting TechCorp AI Customer Support Server...")

    # Import and start server using uvicorn
    import uvicorn
    from main import app

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    try:
        server.run()
    except KeyboardInterrupt:
        print("Server shutdown requested")
    except Exception as e:
        print(f"Server error: {e}")

def wait_for_server_ready(max_wait=30):
    """Wait for server to be ready to accept requests"""
    import requests
    import time

    print("Waiting for server to be ready...")

    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass

        time.sleep(1)

    print("Server did not become ready in time")
    return False

def run_basic_tests():
    """Run basic webhook tests"""
    print("Running basic webhook tests...")

    # Test health check
    print("\nTest 1: Health Check")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # Test web form submission
    print("\nTest 2: Web Form Submission")
    try:
        sample_data = {
            "name": "Test User",
            "email": f"test.{int(time.time())}@example.com",
            "subject": "Test Subject",
            "category": "General Support",
            "message": "This is a test message for the AI agent.",
            "priority": "medium"
        }
        response = requests.post("http://localhost:8000/api/support/submit", json=sample_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Web form test failed: {e}")

    # Test dashboard stats
    print("\nTest 3: Dashboard Stats")
    try:
        response = requests.get("http://localhost:8000/api/dashboard/stats")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Dashboard stats test failed: {e}")

    # Test Gmail webhook (manual trigger)
    print("\nTest 4: Gmail Webhook Trigger")
    try:
        response = requests.post("http://localhost:8000/webhooks/gmail")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Gmail webhook test failed: {e}")

    # Test WhatsApp webhook
    print("\nTest 5: WhatsApp Webhook")
    try:
        whatsapp_payload = {
            "From": "whatsapp:+1234567890",
            "Body": "Test message for WhatsApp webhook",
            "MessageSid": f"MM{int(time.time())}"
        }
        response = requests.post("http://localhost:8000/webhooks/whatsapp", json=whatsapp_payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"WhatsApp webhook test failed: {e}")

    return True

def main():
    """Main function to run the test suite"""
    print("TechCorp AI Customer Support - Basic Test Suite")
    print("=" * 60)

    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)

    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("Warning: .env file not found. Some features may not work properly.")
    else:
        print(".env file found")
        from dotenv import load_dotenv
        load_dotenv()

    # Start server in a separate thread
    print("Starting server...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Wait for server to be ready
    time.sleep(3)  # Give some time for server to start
    if not wait_for_server_ready():
        print("Cannot proceed with tests - server not ready")
        sys.exit(1)

    # Run tests
    run_basic_tests()

    print("\nBasic test suite completed!")
    print("Press Ctrl+C to stop the server")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTest suite terminated by user")

if __name__ == "__main__":
    main()
