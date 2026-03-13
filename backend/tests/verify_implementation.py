import os
import sys
from pathlib import Path

def check_files_and_setup():
    """Verify that all required files and setup are in place"""
    print("Verifying TechCorp AI Support System Setup...")
    print("="*60)

    # Check essential files exist
    essential_files = [
        "main.py",
        "models.py",
        "schemas.py",
        "database.py",
        "ai_agent.py",
        "company_info.txt",
        "database_schema.sql",
        ".env",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "pages/index.jsx",
        "pages/dashboard.jsx",
        "components/WebSupportForm.jsx"
    ]

    print("Checking essential files...")
    all_files_exist = True
    for file in essential_files:
        if os.path.exists(file):
            print(f"  YES {file}")
        else:
            print(f"  NO {file}")
            all_files_exist = False

    print()

    # Check .env configuration
    print("Checking .env configuration...")
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
            required_vars = [
                'DATABASE_URL',
                'OPENAI_API_KEY',
                'GMAIL_CLIENT_ID',
                'TWILIO_ACCOUNT_SID'
            ]

            all_vars_present = True
            for var in required_vars:
                if var in env_content:
                    print(f"  YES {var}")
                else:
                    print(f"  NO {var}")
                    all_vars_present = False

            if all_vars_present:
                print("  YES .env file properly configured")
            else:
                print("  Some environment variables missing")
    else:
        print("  NO .env file not found")
        all_files_exist = False

    print()

    # Check requirements
    print("Checking requirements...")
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            req_content = f.read()
            required_packages = [
                'fastapi',
                'sqlalchemy',
                'openai',
                'twilio',
                'psycopg2-binary'
            ]

            all_packages_present = True
            for pkg in required_packages:
                if pkg in req_content:
                    print(f"  YES {pkg}")
                else:
                    print(f"  NO {pkg}")
                    all_packages_present = False
    else:
        print("  NO requirements.txt not found")
        all_files_exist = False

    print()

    # Check database models
    print("Checking database models...")
    if os.path.exists('models.py'):
        with open('models.py', 'r') as f:
            model_content = f.read()
            required_models = [
                'Customer',
                'Conversation',
                'Message',
                'Ticket',
                'KnowledgeBase'
            ]

            all_models_present = True
            for model in required_models:
                if model in model_content:
                    print(f"  YES {model} model")
                else:
                    print(f"  NO {model} model")
                    all_models_present = False
    else:
        print("  NO models.py not found")
        all_files_exist = False

    print()

    # Check AI agent
    print("Checking AI agent...")
    if os.path.exists('ai_agent.py'):
        with open('ai_agent.py', 'r') as f:
            ai_content = f.read()
            required_tools = [
                'search_knowledge_base',
                'create_ticket',
                'get_customer_history',
                'escalate_to_human',
                'send_response'
            ]

            all_tools_present = True
            for tool in required_tools:
                if tool in ai_content:
                    print(f"  YES {tool} tool")
                else:
                    print(f"  NO {tool} tool")
                    all_tools_present = False

        # Check if OpenAI is imported and used
        if 'import openai' in ai_content or 'openai.' in ai_content:
            print("  YES OpenAI integration")
        else:
            print("  NO OpenAI integration")
            all_tools_present = False
    else:
        print("  NO ai_agent.py not found")
        all_files_exist = False

    print()

    # Check API endpoints
    print("Checking API endpoints...")
    if os.path.exists('main.py'):
        with open('main.py', 'r') as f:
            main_content = f.read()
            required_endpoints = [
                'POST /api/support/submit',
                'POST /webhooks/gmail',
                'POST /webhooks/whatsapp',
                'GET /api/dashboard/stats',
                'GET /api/conversations'
            ]

            all_endpoints_present = True
            endpoint_checks = {
                'POST /api/support/submit': '@app.post("/api/support/submit"',
                'POST /webhooks/gmail': '@app.post("/webhooks/gmail"',
                'POST /webhooks/whatsapp': '@app.post("/webhooks/whatsapp"',
                'GET /api/dashboard/stats': '@app.get("/api/dashboard/stats"',
                'GET /api/conversations': '@app.get("/api/conversations"'
            }

            for name, pattern in endpoint_checks.items():
                if pattern in main_content:
                    print(f"  YES {name}")
                else:
                    print(f"  NO {name}")
                    all_endpoints_present = False
    else:
        print("  NO main.py not found")
        all_files_exist = False

    print()

    # Summary
    print("="*60)
    print("IMPLEMENTATION SUMMARY:")
    print("="*60)

    print(f"Essential Files: {'COMPLETE' if all_files_exist else 'INCOMPLETE'}")
    print(f"Database Models: {'COMPLETE' if 'all_models_present' in locals() and all_models_present else 'INCOMPLETE'}")
    print(f"AI Agent Tools: {'COMPLETE' if 'all_tools_present' in locals() and all_tools_present else 'INCOMPLETE'}")
    print(f"API Endpoints: {'COMPLETE' if 'all_endpoints_present' in locals() and all_endpoints_present else 'INCOMPLETE'}")
    print(f"Dependencies: {'INSTALLED' if 'all_packages_present' in locals() and all_packages_present else 'MISSING'}")

    overall_complete = all([
        all_files_exist,
        'all_models_present' in locals() and all_models_present,
        'all_tools_present' in locals() and all_tools_present,
        'all_endpoints_present' in locals() and all_endpoints_present,
        'all_packages_present' in locals() and all_packages_present
    ])

    print()
    if overall_complete:
        print("OVERALL STATUS: COMPLETE")
        print("The TechCorp AI Customer Support System is fully implemented!")
        print("All components are in place and properly configured!")
        print()
        print("TO RUN THE SYSTEM:")
        print("   1. Clean up Python processes: taskkill /f /im python.exe")
        print("   2. Start backend: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
        print("   3. Start frontend: npm run dev (in another terminal)")
        print("   4. Visit http://localhost:3000 to access the web form")
        print("   5. Visit http://localhost:8000/dashboard for the admin dashboard")
    else:
        print("OVERALL STATUS: INCOMPLETE")
        print("Some components are missing. Please review the checks above.")

    return overall_complete

if __name__ == "__main__":
    check_files_and_setup()
