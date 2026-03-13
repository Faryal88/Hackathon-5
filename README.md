# 🤖 Abdullah AI Customer Support

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-13+-black.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=flat&logo=postgresql&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-412991.svg)

**Abdullah AI Customer Support** is an enterprise-grade, multi-channel customer service platform designed to automate and enhance support operations. Powered by OpenAI's GPT models and a robust RAG (Retrieval-Augmented Generation) engine, it delivers accurate, context-aware responses across Web, Email, and WhatsApp interfaces.

---

## 🚀 Key Features

*   **🧠 Intelligent AI Agent**: Utilizes OpenAI GPT-4 with RAG to answer queries based on company documentation (`company_info.txt`, PDFs).
*   **🌐 Multi-Channel Support**:
    *   **Web Portal**: Real-time chat interface for customers.
    *   **📧 Email Integration**: Automated responses to support emails via Gmail.
    *   **💬 WhatsApp Integration**: Instant support via WhatsApp (Twilio).
*   **📊 Live Dashboard**: Real-time analytics on ticket volume, active conversations, and escalation rates.
*   **🔄 Automated Workflows**: Smart ticket creation, prioritization, and human-handoff escalation.
*   **🛡️ Enterprise Ready**: Built with FastAPI, PostgreSQL, and Docker for scalability and reliability.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python, FastAPI | High-performance async API framework. |
| **Frontend** | TypeScript, Next.js | Modern React framework for the web interface. |
| **Database** | PostgreSQL | Robust relational database for reliable data storage. |
| **AI/ML** | OpenAI GPT, LangChain | LLM orchestration and RAG implementation. |
| **Services** | Kafka, Twilio, Gmail API | Event streaming and communication integrations. |
| **DevOps** | Docker, Docker Compose | Containerization for easy deployment. |

---

## 🏗️ Architecture System Overview

```mermaid
graph TD
    Client[Clients (Web/Mobile)] -->|HTTP/REST| API[FastAPI Backend]
    WhatsApp[WhatsApp/Twilio] -->|Webhook| API
    Gmail[Gmail] -->|Polling/Webhook| API
    
    subgraph "Backend Services"
        API --> Auth[Auth Service]
        API --> Agent[AI Agent Orchestrator]
        Agent --> RAG[RAG Engine]
        RAG --> VectorDB[(Vector Store)]
        Agent --> LLM[OpenAI GPT-4]
    end
    
    subgraph "Data Layer"
        API --> DB[(PostgreSQL)]
        API --> Redis[(Redis Cache)]
    end
```

---

## 🏁 Getting Started

### Prerequisites

*   Python 3.11+
*   Node.js 16+
*   Docker & Docker Compose
*   PostgreSQL
*   OpenAI API Key

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Configure Environment
cp .env.example .env  # Ensure you populate .env with your credentials

# Initialize Database
python init_db.py

# Run Server
python start_server.py
```

### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run Development Server
npm run dev
```

The frontend will be available at `http://localhost:3000` and the backend documentation at `http://localhost:8000/docs`.

---

## 🔧 Environment Configuration

Ensure your `.env` file is configured correctly in the root directory:

```properties
# Core
DATABASE_URL=postgresql://user:pass@localhost:5432/techcorp_support
SECRET_KEY=your_secure_secret
OPENAI_API_KEY=sk-...

# Integrations
GMAIL_CLIENT_ID=...
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
```

---

## 🐳 Docker Deployment

For a production-ready deployment using Docker Compose:

```bash
docker-compose up -d --build
```

This commands starts the Database, Backend (API), and Frontend services in orchestrated containers.

---

## 📚 API Documentation

The API is fully documented using OpenAPI (Swagger). Once the backend is running, visit:

*   **Swagger UI**: `http://localhost:8000/docs`
*   **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

*   `POST /api/support/submit` - Submit a new support ticket.
*   `GET /api/dashboard/stats` - Retrieve real-time system analytics.
*   `POST /webhooks/whatsapp` - Webhook for incoming WhatsApp messages.

---

## 🤝 Contributing

Contributions are welcome! Please verify your changes by running the test suite before submitting a Pull Request.

```bash
# Run backend tests
cd backend
pytest
```

## 📄 License

This project is licensed under the MIT License.
