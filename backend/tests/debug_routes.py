#!/usr/bin/env python3
"""
Debug script to check server routes and status
"""

import requests
import sys

def check_routes():
    """Check various routes to see what's available"""

    base_url = "http://localhost:8001"

    routes_to_check = [
        "/",
        "/health",
        "/api/dashboard/stats",
        "/webhooks/whatsapp",  # This should return 405 for GET, not 404 or 405 for wrong reason
    ]

    print("🔍 CHECKING SERVER ROUTES")
    print("=" * 50)

    for route in routes_to_check:
        try:
            url = base_url + route
            if route == "/webhooks/whatsapp":
                # Test with GET (which should fail with 405) to see if route exists
                response = requests.get(url)
            else:
                response = requests.get(url)

            print(f"GET {route}: {response.status_code} - {response.reason}")
            if response.status_code < 400:
                try:
                    print(f"  Response: {response.json()}")
                except:
                    print(f"  Response: {response.text[:100]}...")
            elif response.status_code == 405:
                print(f"  ✅ Route EXISTS but wrong method (expected for {route})")
            else:
                print(f"  ❌ Route might not exist or other error")

        except requests.exceptions.ConnectionError:
            print(f"GET {route}: ❌ CONNECTION ERROR - Server not running?")
        except Exception as e:
            print(f"GET {route}: ❌ EXCEPTION - {str(e)}")

    print("\n" + "=" * 50)

    # Now try POST to whatsapp webhook
    print("Testing POST to WhatsApp webhook...")
    try:
        response = requests.post(
            f"{base_url}/webhooks/whatsapp",
            headers={'Content-Type': 'application/json'},
            json={"test": "data"}
        )
        print(f"POST /webhooks/whatsapp: {response.status_code} - {response.reason}")
        print(f"Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print("POST /webhooks/whatsapp: ❌ CONNECTION ERROR - Server not running?")
    except Exception as e:
        print(f"POST /webhooks/whatsapp: ❌ EXCEPTION - {str(e)}")

def main():
    print("SERVER DEBUG SCRIPT")
    print("=" * 60)
    print("This script will check if your server routes are properly registered")
    print("=" * 60)

    check_routes()

    print("\n📋 INTERPRETATION:")
    print("- 200: Route works with GET")
    print("- 404: Route does not exist")
    print("- 405: Route exists but wrong method (good for POST routes tested with GET)")
    print("- 500: Route exists but has server error")
    print("- Connection Error: Server not running")

if __name__ == "__main__":
    main()
