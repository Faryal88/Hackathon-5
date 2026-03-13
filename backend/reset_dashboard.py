import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DATABASE_URL, Base, engine
from models import Customer, Conversation, Message, Ticket, KnowledgeBase

def reset_dashboard_data():
    """Reset dashboard data by clearing existing tickets and conversations"""
    print("Resetting TechCorp AI Support Dashboard Data...")

    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Clear existing data (in reverse order to respect foreign key constraints)
        print("Clearing existing tickets...")
        db.execute(text("DELETE FROM tickets"))

        print("Clearing existing messages...")
        db.execute(text("DELETE FROM messages"))

        print("Clearing existing conversations...")
        db.execute(text("DELETE FROM conversations"))

        print("Clearing existing customers...")
        db.execute(text("DELETE FROM customers"))

        # Optionally, repopulate knowledge base with fresh data
        print("Clearing existing knowledge base...")
        db.execute(text("DELETE FROM knowledge_base"))

        # Add fresh sample knowledge base entries
        sample_entries = [
            {
                "question": "How do I reset my password?",
                "answer": "You can reset your password by clicking the 'Forgot Password' link on the login page. Enter your email address and follow the instructions sent to your inbox.",
                "category": "account"
            },
            {
                "question": "What are your pricing plans?",
                "answer": "We offer three plans: Basic ($29/month), Professional ($99/month), and Enterprise ($299/month). Each plan offers different features and data limits. Visit our website for detailed comparison.",
                "category": "pricing"
            },
            {
                "question": "How do I integrate with my existing systems?",
                "answer": "Our platform offers REST APIs, webhooks, and pre-built connectors for popular platforms like Salesforce, Google Analytics, and Microsoft Dynamics. Check our documentation portal for integration guides.",
                "category": "technical"
            },
            {
                "question": "What security measures do you have?",
                "answer": "We maintain SOC 2 Type II compliance, end-to-end encryption, and regular security audits. All data is encrypted and we comply with GDPR and CCPA regulations.",
                "category": "security"
            },
            {
                "question": "Can I upgrade my plan?",
                "answer": "Yes, you can change your plan anytime. Downgrades take effect at the next billing cycle, while upgrades are immediate with prorated charges.",
                "category": "account"
            }
        ]

        for entry in sample_entries:
            db.execute(text("""
                INSERT INTO knowledge_base (question, answer, category, keywords, created_at, updated_at)
                VALUES (:question, :answer, :category, :keywords, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """), {
                "question": entry["question"],
                "answer": entry["answer"],
                "category": entry["category"],
                "keywords": ""
            })

        db.commit()
        print("Dashboard data reset completed successfully!")
        print("All tickets, conversations, messages, and customers have been cleared.")
        print("Sample knowledge base has been repopulated.")

    except Exception as e:
        print(f"Error resetting dashboard data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_dashboard_data()
