import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.smtp_server = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
        self.username = os.getenv("EMAIL_USERNAME")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.from_name = os.getenv("EMAIL_FROM_NAME", "TechCorp AI Support")

        # Human agent email addresses
        self.agent_emails = os.getenv("AGENT_EMAILS", "").split(",") if os.getenv("AGENT_EMAILS") else []

    async def send_escalation_notification(self, ticket_id: int, customer_name: str, issue: str, priority: str = "medium"):
        """Send notification to human agents when a ticket is escalated"""
        if not self.agent_emails:
            logger.warning("No agent emails configured for escalation notifications")
            return False

        subject = f"🚨 URGENT: Ticket #{ticket_id} Requires Human Attention"

        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background-color: #dc2626; color: white; padding: 15px; text-align: center; border-radius: 6px 6px 0 0; }}
                .content {{ padding: 20px; }}
                .ticket-info {{ background-color: #f8fafc; padding: 15px; border-radius: 6px; margin: 15px 0; }}
                .priority-high {{ border-left: 4px solid #ef4444; }}
                .priority-medium {{ border-left: 4px solid #f59e0b; }}
                .priority-low {{ border-left: 4px solid #10b981; }}
                .footer {{ text-align: center; padding: 15px; font-size: 12px; color: #6b7280; border-top: 1px solid #e5e7eb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>🚨 URGENT: Escalation Alert</h2>
                    <p>Ticket #{ticket_id} requires immediate attention</p>
                </div>

                <div class="content">
                    <h3>New Escalated Ticket</h3>
                    <p>A ticket has been escalated and requires human intervention:</p>

                    <div class="ticket-info priority-{priority.lower()}">
                        <h4>Ticket Details:</h4>
                        <p><strong>Ticket ID:</strong> #{ticket_id}</p>
                        <p><strong>Customer:</strong> {customer_name}</p>
                        <p><strong>Priority:</strong> <span style="font-weight:bold;">{priority.upper()}</span></p>
                        <p><strong>Issue:</strong> {issue[:200]}{'...' if len(issue) > 200 else ''}</p>
                        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>

                    <p>Please log into the admin dashboard to review and respond to this ticket:</p>
                    <p><a href="http://127.0.0.1:8000/admin" style="color: #dc2626; font-weight: bold;">Access Admin Dashboard</a></p>

                    <p>This is an automated notification. Please respond promptly to maintain our service levels.</p>
                </div>

                <div class="footer">
                    <p>TechCorp AI Customer Support System</p>
                    <p>You received this email because you are designated as a support agent.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return await self._send_bulk_email(subject, body_html, self.agent_emails)

    async def send_agent_assignment_notification(self, ticket_id: int, agent_name: str, customer_name: str, issue: str):
        """Notify specific agent when assigned to a ticket"""
        subject = f"📋 Assigned: Ticket #{ticket_id} for you to handle"

        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background-color: #3b82f6; color: white; padding: 15px; text-align: center; border-radius: 6px 6px 0 0; }}
                .content {{ padding: 20px; }}
                .ticket-info {{ background-color: #f8fafc; padding: 15px; border-radius: 6px; margin: 15px 0; }}
                .footer {{ text-align: center; padding: 15px; font-size: 12px; color: #6b7280; border-top: 1px solid #e5e7eb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>📋 Ticket Assignment</h2>
                    <p>Ticket #{ticket_id} has been assigned to you</p>
                </div>

                <div class="content">
                    <h3>Ticket Assignment</h3>
                    <p>You have been assigned to handle this ticket:</p>

                    <div class="ticket-info">
                        <h4>Ticket Details:</h4>
                        <p><strong>Ticket ID:</strong> #{ticket_id}</p>
                        <p><strong>Customer:</strong> {customer_name}</p>
                        <p><strong>Issue:</strong> {issue[:200]}{'...' if len(issue) > 200 else ''}</p>
                        <p><strong>Assigned to:</strong> {agent_name}</p>
                        <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>

                    <p>Please log into the admin dashboard to review and respond to this ticket:</p>
                    <p><a href="http://127.0.0.1:8000/admin" style="color: #3b82f6; font-weight: bold;">Access Admin Dashboard</a></p>

                    <p>This is an automated assignment notification.</p>
                </div>

                <div class="footer">
                    <p>TechCorp AI Customer Support System</p>
                    <p>You received this email because you are designated as a support agent.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # For assignment, we might want to send to specific agent instead of all
        agent_email = os.getenv(f"AGENT_{agent_name.upper()}_EMAIL")
        if agent_email:
            return await self._send_email(subject, body_html, agent_email)
        else:
            # Fallback to all agents
            return await self._send_bulk_email(subject, body_html, self.agent_emails)

    async def _send_email(self, subject: str, body: str, to_email: str) -> bool:
        """Send a single email"""
        try:
            if not self.username or not self.password:
                logger.error("Email credentials not configured")
                return False

            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.username}>"
            msg['To'] = to_email

            # Create both plain text and HTML versions
            text_part = MIMEText(self._html_to_text(body), 'plain')
            html_part = MIMEText(body, 'html')

            msg.attach(text_part)
            msg.attach(html_part)

            # Send the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {e}")
            return False

    async def _send_bulk_email(self, subject: str, body: str, to_emails: List[str]) -> bool:
        """Send email to multiple recipients"""
        results = []
        for email in to_emails:
            if email.strip():  # Skip empty emails
                result = await self._send_email(subject, body, email.strip())
                results.append(result)

        success_count = sum(results)
        logger.info(f"Sent {success_count}/{len(to_emails)} escalation notifications")
        return success_count > 0

    def _html_to_text(self, html: str) -> str:
        """Convert HTML to plain text (simple conversion)"""
        import re
        # Remove HTML tags and convert to plain text
        clean = re.compile('<.*?>')
        text = re.sub(clean, '', html)
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

# Global notification service instance
notification_service = NotificationService()
