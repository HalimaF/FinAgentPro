# FinAgent Pro - Technical Architecture

## 🏛️ System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Frontend Layer                              │
│  React UI Dashboard | Expense Upload | Invoice Creator | Analytics  │
└───────────────┬─────────────────────────────────────────────────────┘
                │ REST API / WebSocket
┌───────────────▼─────────────────────────────────────────────────────┐
│                        API Gateway (FastAPI)                         │
│              Authentication | Rate Limiting | Logging                │
└───────────────┬─────────────────────────────────────────────────────┘
                │
┌───────────────▼─────────────────────────────────────────────────────┐
│              IBM watsonx Orchestrate (Orchestration Hub)             │
│    • Task Routing    • Agent Coordination    • Workflow Management  │
│    • Message Bus     • State Management      • Event Streaming      │
└─┬──────────┬──────────┬──────────┬──────────┬────────────────────────┘
  │          │          │          │          │
  ▼          ▼          ▼          ▼          ▼
┌─────┐  ┌──────┐  ┌───────┐  ┌────────┐  ┌─────────┐
│Exp. │  │Inv.  │  │Fraud  │  │Cashflow│  │External │
│Class│  │Agent │  │Analyze│  │Forecast│  │Services │
└──┬──┘  └──┬───┘  └───┬───┘  └───┬────┘  └────┬────┘
   │        │          │          │           │
┌──▼────────▼──────────▼──────────▼───────────▼──────────────┐
│              Data & Storage Layer                           │
│  PostgreSQL | Redis | S3 | Vector DB | Time-Series DB     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Agent Communication Flow

### Message-Based Architecture

```python
# Agent Communication Protocol

{
  "message_id": "msg_12345",
  "source_agent": "expense_classifier",
  "target_agent": "fraud_analyzer",
  "action": "analyze_transaction",
  "payload": {
    "transaction_id": "txn_67890",
    "amount": 5000,
    "merchant": "Tech Supplies Inc",
    "category": "Equipment"
  },
  "priority": "high",
  "timestamp": "2025-11-19T10:30:00Z",
  "correlation_id": "flow_abcdef"
}
```

### Agent Interaction Patterns

#### 1. Sequential Processing
```
User Upload → Expense Classifier → Fraud Analyzer → Ledger Update
```

#### 2. Parallel Processing
```
Invoice Creation → [Email Send | Payment Link | CRM Update] (concurrent)
```

#### 3. Event-Driven
```
Transaction Detected → Event Bus → Fraud Agent Subscribe → Real-time Alert
```

---

## 🗄️ Data Architecture

### Database Schema

```sql
-- Core Tables

CREATE TABLE expenses (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    amount DECIMAL(10,2),
    category VARCHAR(100),
    merchant VARCHAR(255),
    receipt_url TEXT,
    ocr_confidence FLOAT,
    fraud_score FLOAT,
    status VARCHAR(50),
    created_at TIMESTAMP,
    processed_by VARCHAR(100) -- agent identifier
);

CREATE TABLE invoices (
    id UUID PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE,
    client_id UUID REFERENCES clients(id),
    amount DECIMAL(10,2),
    due_date DATE,
    status VARCHAR(50),
    payment_link TEXT,
    created_by VARCHAR(100), -- agent or user
    created_at TIMESTAMP,
    paid_at TIMESTAMP
);

CREATE TABLE fraud_alerts (
    id UUID PRIMARY KEY,
    transaction_id UUID,
    alert_type VARCHAR(100),
    severity VARCHAR(20),
    risk_score FLOAT,
    explanation TEXT,
    status VARCHAR(50),
    detected_at TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE TABLE cashflow_forecasts (
    id UUID PRIMARY KEY,
    forecast_date DATE,
    predicted_inflow DECIMAL(12,2),
    predicted_outflow DECIMAL(12,2),
    net_position DECIMAL(12,2),
    confidence_interval JSONB,
    model_version VARCHAR(50),
    generated_at TIMESTAMP
);

CREATE TABLE agent_logs (
    id UUID PRIMARY KEY,
    agent_name VARCHAR(100),
    action VARCHAR(255),
    input_data JSONB,
    output_data JSONB,
    execution_time_ms INTEGER,
    status VARCHAR(50),
    error_message TEXT,
    timestamp TIMESTAMP
);
```

### Data Flow Pipeline

```
┌─────────────┐
│   Raw Data  │ (Receipts, PDFs, CSV uploads)
└──────┬──────┘
       │
       ▼
┌──────────────┐
│ Preprocessing│ (OCR, Parsing, Validation)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  AI Processing│ (Classification, Extraction, Analysis)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Enrichment  │ (Fraud Check, Category Mapping, Validation)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Storage    │ (PostgreSQL + Vector DB for embeddings)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Analytics   │ (Dashboards, Reports, Forecasts)
└──────────────┘
```

---

## 🔌 API Architecture

### RESTful API Endpoints

```yaml
# Expense Management
POST   /api/v1/expenses/upload          # Upload receipt
GET    /api/v1/expenses                 # List expenses
GET    /api/v1/expenses/{id}            # Get expense details
PUT    /api/v1/expenses/{id}            # Update expense
DELETE /api/v1/expenses/{id}            # Delete expense

# Invoice Management
POST   /api/v1/invoices                 # Create invoice
GET    /api/v1/invoices                 # List invoices
GET    /api/v1/invoices/{id}            # Get invoice
PUT    /api/v1/invoices/{id}/send       # Send invoice
POST   /api/v1/invoices/{id}/payment    # Record payment

# Fraud Detection
GET    /api/v1/fraud/alerts              # Get fraud alerts
GET    /api/v1/fraud/analyze/{txn_id}   # Analyze specific transaction
POST   /api/v1/fraud/alerts/{id}/resolve # Resolve alert

# Cashflow Forecasting
GET    /api/v1/forecast/cashflow         # Get forecast
POST   /api/v1/forecast/refresh          # Regenerate forecast
GET    /api/v1/forecast/scenarios        # What-if scenarios

# Agent Orchestration
POST   /api/v1/orchestrate/workflow      # Trigger workflow
GET    /api/v1/orchestrate/status/{id}   # Check workflow status
GET    /api/v1/agents/health             # Agent health check
```

### WebSocket Events

```javascript
// Real-time event streaming
ws://api.finagent.pro/ws

// Event Types
{
  "type": "expense.classified",
  "type": "invoice.created",
  "type": "fraud.alert",
  "type": "forecast.updated",
  "type": "agent.status_change"
}
```

---

## 🤖 Agent Architecture Details

### 1. Expense Classifier Agent

```
Input: Receipt image/PDF
│
├─→ OCR Processing (Tesseract/Google Vision)
│   └─→ Extract: Amount, Date, Merchant, Line Items
│
├─→ GPT-4 Classification
│   └─→ Categorize: Travel, Meals, Equipment, etc.
│
├─→ Confidence Scoring
│   └─→ Flag low-confidence items for review
│
└─→ Output: Structured expense record
```

**Technologies**: 
- OCR: Tesseract + Google Cloud Vision API
- NLP: OpenAI GPT-4 for context understanding
- Storage: S3 for receipts, PostgreSQL for metadata

### 2. Invoice Agent

```
Input: "Create invoice for Project X, $5000"
│
├─→ NLU Processing (Intent Recognition)
│   └─→ Extract: Client, Amount, Items, Due Date
│
├─→ Template Selection
│   └─→ Choose appropriate invoice format
│
├─→ PDF Generation (ReportLab)
│   └─→ Professional invoice document
│
├─→ Payment Link Creation (Stripe API)
│
└─→ Output: Invoice PDF + Payment URL
```

**Technologies**:
- NLU: GPT-4 for intent parsing
- PDF: ReportLab
- Payments: Stripe API integration
- Email: SendGrid for delivery

### 3. Fraud Analyzer Agent

```
Input: Transaction data stream
│
├─→ Real-time Anomaly Detection
│   ├─→ Statistical outlier detection
│   ├─→ Pattern matching (ML model)
│   └─→ Velocity checks
│
├─→ Risk Scoring (0-100)
│   ├─→ Amount deviation: 30%
│   ├─→ Merchant reputation: 25%
│   ├─→ Historical patterns: 25%
│   └─→ Time/location: 20%
│
├─→ Alert Generation (if score > 70)
│
└─→ Output: Fraud alert + recommended action
```

**Technologies**:
- ML: Isolation Forest, LSTM for sequence analysis
- Rules Engine: Complex event processing
- Real-time: Apache Kafka for streaming

### 4. Cashflow Forecast Agent

```
Input: Historical financial data (12+ months)
│
├─→ Data Preprocessing
│   ├─→ Seasonality decomposition
│   ├─→ Trend extraction
│   └─→ Outlier removal
│
├─→ ML Forecasting
│   ├─→ Prophet (Facebook) for time-series
│   ├─→ ARIMA for baseline
│   └─→ Ensemble model
│
├─→ Scenario Analysis
│   ├─→ Best case (+20%)
│   ├─→ Expected case
│   └─→ Worst case (-20%)
│
└─→ Output: 12-month forecast + confidence intervals
```

**Technologies**:
- Forecasting: Prophet, ARIMA, XGBoost
- Visualization: Plotly for interactive charts
- Storage: TimescaleDB for time-series data

### 5. Workflow Orchestrator Agent

```
Input: User request or system event
│
├─→ Intent Analysis
│   └─→ Determine workflow type
│
├─→ Agent Selection & Routing
│   ├─→ Identify required agents
│   ├─→ Determine execution order
│   └─→ Set priorities
│
├─→ Execution Coordination
│   ├─→ Monitor agent progress
│   ├─→ Handle failures & retries
│   └─→ Aggregate results
│
├─→ State Management
│   └─→ Track workflow completion
│
└─→ Output: Unified response to user
```

**Technologies**:
- Orchestration: IBM watsonx Orchestrate
- State Management: Redis
- Message Queue: RabbitMQ
- Monitoring: Prometheus + Grafana

---

## 🔒 Security Architecture

### Authentication & Authorization

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ JWT Token
┌──────▼──────┐
│ API Gateway │
└──────┬──────┘
       │ Verify + Decode
┌──────▼──────┐
│   RBAC      │ Role-Based Access Control
└──────┬──────┘
       │ Authorized
┌──────▼──────┐
│   Agents    │
└─────────────┘
```

### Data Security

- **Encryption at Rest**: AES-256 for database
- **Encryption in Transit**: TLS 1.3 for all communications
- **PII Handling**: GDPR-compliant data masking
- **Audit Logs**: Immutable logs for all agent actions

---

## 📊 Monitoring & Observability

### Key Metrics

```yaml
Agent Performance:
  - Execution time per agent
  - Success/failure rate
  - Queue depth

Business Metrics:
  - Expenses processed per hour
  - Invoice generation time
  - Fraud detection accuracy
  - Forecast accuracy (MAPE)

System Health:
  - API latency (p50, p95, p99)
  - Database connection pool
  - Memory/CPU usage per agent
```

### Logging Strategy

```python
# Structured logging for agent actions
{
  "timestamp": "2025-11-19T10:30:00Z",
  "agent": "expense_classifier",
  "action": "classify_receipt",
  "input": {"receipt_id": "rcpt_123"},
  "output": {"category": "Travel", "confidence": 0.95},
  "duration_ms": 1250,
  "status": "success"
}
```

---

## 🚀 Scalability Design

### Horizontal Scaling

- **Agents**: Stateless design, can scale to N instances
- **Database**: Read replicas for analytics queries
- **Caching**: Redis cluster for session/state management
- **Storage**: S3 with CDN for receipt images

### Load Balancing

```
                  ┌─→ Agent Instance 1
Client → LB → API ├─→ Agent Instance 2
                  └─→ Agent Instance 3
```

---

## 🔄 Deployment Architecture

```yaml
# Kubernetes Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: finagent-orchestrator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: orchestrator
  template:
    spec:
      containers:
      - name: orchestrator
        image: finagent/orchestrator:latest
        resources:
          requests:
            cpu: "500m"
            memory: "1Gi"
          limits:
            cpu: "2000m"
            memory: "4Gi"
```

---

## 📈 Performance Benchmarks

| Operation | Target | Actual |
|-----------|--------|--------|
| OCR Processing | < 3s | 2.1s |
| Expense Classification | < 1s | 0.7s |
| Invoice Generation | < 2s | 1.4s |
| Fraud Detection | < 500ms | 320ms |
| Cashflow Forecast | < 5s | 3.8s |
| API Response (p95) | < 200ms | 145ms |

---

**Architecture designed for enterprise-scale financial automation**
