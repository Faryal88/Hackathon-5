# AGENTS.md - TechCorp AI Customer Support System

This document describes the TechCorp AI Customer Support System repository structure and conventions for AI agents.

## Repository Overview

The TechCorp AI Customer Support System is a full-stack customer support application featuring:
- **Backend**: FastAPI-based API server with AI integration
- **Frontend**: Next.js-based React application
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Integration**: OpenAI GPT for automated responses
- **Multi-channel Support**: Web forms, Gmail, and WhatsApp

## Directory Structure

```
├── main.py                 # FastAPI main application with API endpoints
├── ai_agent.py            # AI agent implementation with tools for customer support
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic schemas for data validation
├── database.py            # Database configuration
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── pages/                 # Next.js pages directory
│   ├── index.jsx          # Main support form page
│   ├── dashboard.jsx      # Admin dashboard showing metrics
│   └── api/               # Next.js API routes
├── components/            # Reusable React components
│   └── WebSupportForm.jsx # Support form component
├── next.config.js         # Next.js configuration with API proxy
├── package.json           # Node.js dependencies
├── Dockerfile             # Containerization setup
├── docker-compose.yml     # Multi-service Docker configuration
├── .env                   # Environment variables
├── company_info.txt       # Company information for AI agent
└── README.md              # Project documentation
```

## Key Files and Their Purpose

### Backend Files
- `main.py`: Main FastAPI application containing all API endpoints for customer support
- `ai_agent.py`: AI agent implementation with tools for knowledge base search, ticket creation, customer history, escalation, and response sending
- `models.py`: SQLAlchemy database models (Customer, Conversation, Message, Ticket, KnowledgeBase)
- `schemas.py`: Pydantic schemas for request/response validation
- `database.py`: Database configuration with connection setup
- `init_db.py`: Database initialization and sample data population

### Frontend Files
- `pages/index.jsx`: Main support form page where customers can submit requests
- `pages/dashboard.jsx`: Admin dashboard showing real-time metrics and analytics
- `components/WebSupportForm.jsx`: Reusable support form component with validation
- `next.config.js`: Next.js configuration with API proxy to backend

### Configuration Files
- `Dockerfile`: Defines container image with Python, dependencies, and application
- `docker-compose.yml`: Multi-service orchestration for backend, frontend, and database
- `.env`: Environment variables including database URL and API keys

## API Endpoints

### Public Endpoints
- `POST /api/support/submit`: Submit support request via web form
- `GET /api/dashboard/stats`: Get dashboard statistics
- `GET /api/conversations`: Get list of conversations
- `GET /api/messages/{conversation_id}`: Get messages for specific conversation
- `GET /api/tickets/user?email=xxx`: Get tickets for user by email

### Health Check
- `GET /health`: System health check

## Database Schema

### Models
- **Customer**: Stores customer information (email, name, phone)
- **Conversation**: Tracks support interactions by channel (web_form, gmail, whatsapp)
- **Message**: Individual messages with direction (incoming/outgoing)
- **Ticket**: Support tickets with status and priority
- **KnowledgeBase**: FAQ and common responses for AI agent

### Relationships
- One Customer to Many Conversations
- One Conversation to Many Messages
- One Conversation to One Ticket
- Knowledge Base for AI responses

## AI Agent Features

### Tools Available
- **Knowledge Base Search**: Search for relevant information in company knowledge base
- **Ticket Creation**: Create support tickets automatically
- **Customer History**: Retrieve interaction history
- **Escalation**: Automatically escalate to human agents
- **Response Sending**: Send responses via appropriate channels

### Escalation Rules
The system automatically escalates to human agents for:
- Pricing and billing disputes
- Contract negotiations
- Legal inquiries
- Security breach reports
- Angry or threatening customers
- Requests for custom feature development
- Data recovery requests
- Account closure requests
- Competitor comparison discussions
- CEO/C-level escalation requests

## Multi-Channel Support

### Supported Channels
- **Web Form**: Direct form submissions via frontend
- **Gmail**: Email webhook integration
- **WhatsApp**: Twilio-powered WhatsApp integration

## Deployment

### Docker Setup
The system is container-ready with:
- Dockerfile for backend service
- docker-compose.yml for multi-service deployment
- Environment configuration via .env

### Environment Variables
Required configuration in .env:
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for AI responses
- Various other service configurations

## Development Workflow

### Adding New Features
1. Update models.py for new data structures
2. Add corresponding schemas in schemas.py
3. Create API endpoints in main.py
4. Implement frontend components in pages/
5. Update this AGENTS.md as needed

## Security Considerations
- Input validation on all endpoints
- SQL injection prevention via SQLAlchemy ORM
- Environment-based configuration
- API key management

## Performance Considerations
- Efficient database queries
- Caching-ready architecture
- Asynchronous processing where appropriate
