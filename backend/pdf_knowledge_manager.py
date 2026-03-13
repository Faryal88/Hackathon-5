"""
Utility script to manage PDF knowledge for the AI agent
"""

import asyncio
from sqlalchemy.orm import Session
from enhanced_ai_agent import EnhancedAIAgent
from database import SessionLocal
import sys
import os
from pathlib import Path

def load_pdf_to_agent(pdf_path: str):
    """Load a PDF file into the AI agent's knowledge base"""
    print(f"Loading PDF: {pdf_path}")

    # Create a database session
    db = SessionLocal()

    try:
        # Initialize the enhanced AI agent
        ai_agent = EnhancedAIAgent(db)

        # Load the PDF into the agent's knowledge base
        result = asyncio.run(ai_agent.load_new_pdf(pdf_path))
        print(result)

        print("PDF successfully loaded into the AI agent's knowledge base!")
        print("The agent can now respond to queries based on the information in this PDF.")

    except Exception as e:
        print(f"Error loading PDF: {str(e)}")
    finally:
        db.close()

def main():
    print("TechCorp AI Agent PDF Knowledge Manager")
    print("="*50)

    if len(sys.argv) < 2:
        print("Usage: python pdf_knowledge_manager.py <path_to_pdf_file>")
        print("\nThis tool allows you to load PDF documents into the AI agent's knowledge base.")
        print("The agent will then be able to answer questions based on the content of these PDFs.")
        print("\nExample: python pdf_knowledge_manager.py company_handbook.pdf")
        return

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        return

    if not pdf_path.lower().endswith('.pdf'):
        print("Error: File must be a PDF")
        return

    print(f"Preparing to load PDF knowledge from: {pdf_path}")
    print("This will enhance the AI agent's ability to answer questions based on your company documentation.")

    confirm = input("\nContinue? (y/N): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return

    load_pdf_to_agent(pdf_path)

if __name__ == "__main__":
    main()
