#!/usr/bin/env python3
"""
Check if the backend server is responding
"""

import requests
import socket

def check_port_8000():
    """Check if port 8000 is accessible"""
    print("Checking if port 8000 is accessible...")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8000))
        sock.close()

        if result == 0:
            print("SUCCESS: Port 8000 is open and accepting connections")
            return True
        else:
            print("FAILED: Port 8000 is not accessible")
            return False
    except Exception as e:
        print(f"ERROR: Error checking port 8000: {e}")
        return False

def test_server_health():
    """Test the server health endpoint"""
    print("\nTesting server health endpoint...")

    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"Response Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("SUCCESS: Server is responding correctly!")
            return True
        else:
            print("FAILED: Server responded but with error status")
            return False

    except requests.exceptions.ConnectionError:
        print("FAILED: Cannot connect to server - connection refused")
        return False
    except requests.exceptions.Timeout:
        print("FAILED: Request timed out - server may be slow or unresponsive")
        return False
    except Exception as e:
        print(f"FAILED: Error testing server: {e}")
        return False

def main():
    print("Server Connectivity Check")
    print("=" * 40)

    port_ok = check_port_8000()

    if port_ok:
        test_server_health()
    else:
        print("\nThe backend server is not running properly.")
        print("\nTo start the backend server, run:")
        print("   python -c \"import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8000)\"")
        print("\nMake sure you have the required dependencies installed:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
