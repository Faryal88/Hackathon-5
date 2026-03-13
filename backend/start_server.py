import subprocess
import sys
import os
from threading import Thread
import time

def check_requirements():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import openai
        import psycopg2
        print("✓ All required packages are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please install requirements using: pip install -r requirements.txt")
        return False

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting TechCorp AI Support Backend...")

    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def start_frontend():
    """Start the Next.js frontend server"""
    print("🌐 Starting TechCorp AI Support Frontend...")

    try:
        subprocess.run(["npm", "run", "dev"], cwd=os.getcwd())
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    print("🔧 TechCorp AI Customer Support System Startup")
    print("="*50)

    # Check requirements
    if not check_requirements():
        return

    # Check if .env file exists
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found. Please create one with required environment variables.")
        print("Refer to README.md for required environment variables.")
    else:
        print("✅ Environment variables loaded from .env file")

    print("\n📋 Available Services:")
    print("   1. Backend (FastAPI) - Port 8000")
    print("   2. Frontend (Next.js) - Port 3000 (if started separately)")
    print("   3. Both (Backend only - frontend served via proxy)")

    print("\n💡 Tip: Run 'python start_server.py' to start the backend server")
    print("   The backend serves both API and static files")
    print("   Access the application at http://localhost:8000")

    # Start backend server
    start_backend()

if __name__ == "__main__":
    main()
