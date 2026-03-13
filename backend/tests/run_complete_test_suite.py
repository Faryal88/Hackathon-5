#!/usr/bin/env python3
"""
Complete test suite runner for TechCorp AI Customer Support
This script starts the server and runs comprehensive webhook tests
"""

import subprocess
import sys
import time
import signal
import os
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

    print("⏳ Waiting for server to be ready...")

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

def run_tests():
    """Run the comprehensive test suite"""
    print("Running comprehensive webhook tests...")

    # Import and run our test script
    try:
        import comprehensive_webhook_test
        comprehensive_webhook_test.run_comprehensive_tests()
        return True
    except Exception as e:
        print(f"Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function to orchestrate the complete test suite"""
    print("TechCorp AI Customer Support - Complete Test Suite")
    print("=" * 60)

    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)

    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("Warning: .env file not found. Please create one with required environment variables:")
        print("   OPENAI_API_KEY=your_openai_key")
        print("   EMAIL_USERNAME=your_email")
        print("   EMAIL_PASSWORD=your_app_password")
        print("   TWILIO_ACCOUNT_SID=your_twilio_sid")
        print("   TWILIO_AUTH_TOKEN=your_twilio_token")
        print()
    else:
        print(".env file found")
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()

    # Start server in a separate thread
    print("Starting server...")
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Wait for server to be ready
    if not wait_for_server_ready():
        print("Cannot proceed with tests - server not ready")
        sys.exit(1)

    # Give server a bit more time to initialize fully
    time.sleep(3)

    # Run tests
    tests_passed = run_tests()

    print()
    print("Test Suite Complete!")
    print("=" * 60)

    if tests_passed:
        print("All tests completed successfully!")
    else:
        print("Some tests failed")

    print()
    print("📋 Summary:")
    print("   - Gmail webhook tested (manual trigger)")
    print("   - WhatsApp webhook tested (Twilio payload simulation)")
    print("   - Web form webhook tested (support request submission)")
    print("   - AI agent responses tested (across all channels)")
    print("   - Knowledge base queries tested")
    print("   - Escalation handling tested")
    print("   - Dashboard statistics tested")
    print("   - Conversation management tested")
    print()
    print("Note: Some tests may show warnings if external services aren't configured")

    # Keep server running for manual testing
    print("\nServer remaining active for manual testing...")
    print("Press Ctrl+C to stop the server")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTest suite terminated by user")

if __name__ == "__main__":
    main()
