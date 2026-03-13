#!/usr/bin/env python3
"""
Simple server startup script for TechCorp AI Customer Support
"""

import subprocess
import sys
import time
import signal
import os

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting TechCorp AI Customer Support Server...")
    print("Listening on http://localhost:8000")

    try:
        # Start the server using uvicorn
        process = subprocess.Popen([
            sys.executable, "-c",
            "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8000)"
        ])

        print("✅ Server started successfully!")
        print("💡 Server is now running. Press Ctrl+C to stop.")
        print()

        # Wait for process to complete (or be interrupted)
        process.wait()

    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        print("✅ Server stopped.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server()
