-- TechCorp AI Customer Support Database Schema

-- Customers table
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    channel VARCHAR(50) NOT NULL, -- 'web_form', 'gmail', 'whatsapp'
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'processing', 'resolved', 'escalated'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    content TEXT NOT NULL,
    channel VARCHAR(50) NOT NULL, -- 'web_form', 'gmail', 'whatsapp'
    direction VARCHAR(10) NOT NULL, -- 'incoming', 'outgoing'
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tickets table
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    conversation_id INTEGER REFERENCES conversations(id),
    issue TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'open', -- 'open', 'in_progress', 'resolved', 'escalated'
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'urgent'
    assigned_agent VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge Base table
CREATE TABLE knowledge_base (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(100),
    keywords TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_conversations_customer_id ON conversations(customer_id);
CREATE INDEX idx_conversations_status ON conversations(status);
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_tickets_customer_id ON tickets(customer_id);
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_knowledge_base_category ON knowledge_base(category);

-- Insert initial knowledge base data
INSERT INTO knowledge_base (question, answer, category) VALUES
('How do I reset my password?', 'You can reset your password by clicking the "Forgot Password" link on the login page. Enter your email address and follow the instructions sent to your inbox.', 'account'),
('What are your pricing plans?', 'We offer three plans: Basic ($29/month), Professional ($99/month), and Enterprise ($299/month). Each plan offers different features and data limits. Visit our website for detailed comparison.', 'pricing'),
('How do I integrate with my existing systems?', 'Our platform offers REST APIs, webhooks, and pre-built connectors for popular platforms like Salesforce, Google Analytics, and Microsoft Dynamics. Check our documentation portal for integration guides.', 'technical'),
('What security measures do you have?', 'We maintain SOC 2 Type II compliance, end-to-end encryption, and regular security audits. All data is encrypted and we comply with GDPR and CCPA regulations.', 'security'),
('Can I upgrade my plan?', 'Yes, you can change your plan anytime. Downgrades take effect at the next billing cycle, while upgrades are immediate with prorated charges.', 'account'),
('Do you offer training?', 'Yes, Professional and Enterprise plans include onboarding sessions. We also offer advanced training workshops and certification programs.', 'training'),
('What is your uptime guarantee?', 'We offer a 99.9% uptime SLA for all paid plans, with monthly reporting on system availability.', 'technical');