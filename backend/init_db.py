import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database import Base, DATABASE_URL
from models import *
from dotenv import load_dotenv
import os

load_dotenv()

def init_database():
    """Initialize the database with tables and sample data"""
    print("Initializing TechCorp AI Support Database...")

    # Create database engine
    engine = create_engine(DATABASE_URL)

    # Drop and recreate all tables to apply schema changes
    print("Dropping and recreating database tables to apply schema changes...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if knowledge base already has data
        kb_count = db.query(KnowledgeBase).count()
        if kb_count == 0:
            print("Populating knowledge base with initial data...")

            # Read company info and populate knowledge base
            if os.path.exists("company_info.txt"):
                with open("company_info.txt", "r") as f:
                    content = f.read()

                # This is a simplified parsing - in a real app, you'd want more sophisticated parsing
                # For now, let's add some sample entries
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
                    kb_entry = KnowledgeBase(
                        question=entry["question"],
                        answer=entry["answer"],
                        category=entry["category"],
                        keywords=""
                    )
                    db.add(kb_entry)

                db.commit()
                print(f"Added {len(sample_entries)} sample knowledge base entries")
            else:
                print("Warning: company_info.txt not found, skipping knowledge base population")

        print("Database initialization completed successfully!")
        print(f"Tables created: customers, conversations, messages, tickets, knowledge_base")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
