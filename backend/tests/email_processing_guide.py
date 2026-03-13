#!/usr/bin/env python3
"""
Email Processing Guide for TechCorp AI Customer Support

This explains how the email system works and why you might be seeing escalation messages.
"""

def explain_email_system():
    """Explain how the email processing system works"""

    print("=" * 80)
    print("EMAIL PROCESSING SYSTEM EXPLANATION")
    print("=" * 80)

    print("\n1. EMAIL POLLING MECHANISM:")
    print("   • The system uses IMAP to periodically check your email inbox")
    print("   • Default polling interval: Every 5 minutes")
    print("   • Manual trigger available: POST /webhooks/gmail")
    print("   • When you send an email to aimoshahs@gmail.com, it won't be processed instantly")
    print("   • You need to wait for the next polling cycle OR manually trigger the webhook")

    print("\n2. MANUAL TRIGGER:")
    print("   To immediately check for new emails, call:")
    print("   POST http://localhost:8000/webhooks/gmail")
    print("   This will scan your inbox and process any UNREAD emails")

    print("\n3. ESCALATION BEHAVIOR:")
    print("   The AI agent has built-in escalation rules that trigger for certain keywords:")
    print("   - 'security', 'legal', 'ceo', 'contract', 'refund', 'cancel'")
    print("   - 'competitor', 'complaint', 'angry', 'frustrated', 'threat'")
    print("   - 'breach', 'hacker', 'privacy'")
    print("   When these words are detected, the system automatically escalates to human agent")
    print("   This is why you're seeing 'escalated' responses instead of AI answers")

    print("\n4. KNOWLEDGE BASE RESPONSES:")
    print("   For non-sensitive topics, the AI should respond with knowledge base information")
    print("   Topics like 'pricing', 'integration', 'account', 'password' should get AI responses")
    print("   The system searches company_info.txt for relevant information")

    print("\n5. TO TEST EMAIL PROCESSING:")
    print("   a) Send an email to aimoshahs@gmail.com with NON-ESCALATION content")
    print("      Good example: 'What are your pricing plans?'")
    print("      Avoid: 'security', 'legal', 'cancel', 'refund', 'ceo', etc.")
    print("   b) Wait for auto-polling (up to 5 minutes) OR")
    print("   c) Manually trigger: curl -X POST http://localhost:8000/webhooks/gmail")
    print("   d) Check dashboard: GET http://localhost:8000/api/dashboard/stats")

    print("\n6. WEB FORM VS EMAIL:")
    print("   Web form submissions (POST /api/support/submit) get immediate AI responses")
    print("   Email processing depends on polling schedule or manual triggers")
    print("   This is by design for email processing efficiency")

    print("\n7. CONFIGURATION CHECK:")
    print("   Make sure your .env file has correct email settings:")
    print("   EMAIL_USERNAME=aimoshahs@gmail.com")
    print("   EMAIL_PASSWORD=your_app_password")
    print("   EMAIL_IMAP_SERVER=imap.gmail.com")
    print("   EMAIL_SMTP_SERVER=smtp.gmail.com")

    print("\n8. TROUBLESHOOTING:")
    print("   • If emails aren't processed, check email credentials in .env")
    print("   • Enable 2-factor authentication and use App Password for Gmail")
    print("   • Ensure the email account can be accessed via IMAP")
    print("   • Check server logs for IMAP connection errors")

def suggest_test_messages():
    """Suggest good test messages that won't trigger escalation"""

    print("\n" + "=" * 80)
    print("SUGGESTED TEST EMAIL CONTENT (Won't Trigger Escalation)")
    print("=" * 80)

    good_messages = [
        "What are your pricing plans?",
        "How do I integrate with Salesforce?",
        "I need help with my account login",
        "Can you explain the API rate limits?",
        "What features are included in the Professional plan?",
        "How do I reset my password?",
        "I'm having trouble with the dashboard",
        "What's the difference between Basic and Professional plans?",
        "How do I export my data?",
        "I need help with the reporting features"
    ]

    for i, msg in enumerate(good_messages, 1):
        print(f"   {i:2d}. {msg}")

    print("\nAVOID THESE WORDS (Will Trigger Escalation):")
    bad_words = [
        "security", "legal", "ceo", "contract", "refund", "cancel", "competitor",
        "complaint", "angry", "frustrated", "threat", "breach", "hacker", "privacy"
    ]
    print(f"   {', '.join(bad_words)}")

def api_endpoints_summary():
    """Summarize the key API endpoints"""

    print("\n" + "=" * 80)
    print("KEY API ENDPOINTS")
    print("=" * 80)

    endpoints = [
        ("GET  /health", "System health check"),
        ("POST /api/support/submit", "Web form submission - gets immediate AI response"),
        ("POST /webhooks/gmail", "Manual email check - triggers IMAP polling"),
        ("GET  /api/dashboard/stats", "Dashboard statistics"),
        ("GET  /api/conversations", "List conversations"),
        ("GET  /api/tickets/user?email=x", "User tickets by email")
    ]

    for method_url, desc in endpoints:
        print(f"   {method_url:<30} - {desc}")

if __name__ == "__main__":
    explain_email_system()
    suggest_test_messages()
    api_endpoints_summary()

    print("\n" + "=" * 80)
    print("TO RESOLVE YOUR ISSUE:")
    print("=" * 80)
    print("1. Send a test email with safe content (avoid escalation keywords)")
    print("2. Manually trigger email processing: curl -X POST http://localhost:8000/webhooks/gmail")
    print("3. Or wait up to 5 minutes for auto-polling")
    print("4. Check the dashboard for new tickets: http://localhost:8000/api/dashboard/stats")
    print("5. Make sure your email credentials are correct in the .env file")
