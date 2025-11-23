# IBM watsonx Orchestrate - FinAgent Pro 

This directory contains all IBM watsonx Orchestrate configurations for FinAgent Pro, including:
- Workflow definitions (complete and ready)
- Agent skills and capabilities (all 6 agents defined)
- Integration mappings (REST API + WebSocket)
- Event handlers (fraud alerts, approvals)
- Orchestration rules (multi-agent coordination)

---

## Agent Skills Configuration

### 1. Expense Classifier Agent

```yaml
skill_id: expense_classifier_v1
name: Expense Classification & OCR
description: Processes receipts using OCR and AI classification
agent_type: cognitive
capabilities:
  - ocr_processing
  - expense_categorization
  - confidence_scoring
  - multi_language_support
inputs:
  - name: receipt_file
    type: binary
    required: true
    formats: [jpg, png, pdf]

outputs:
      amount: number
      merchant: string
      category: string
execution:
  timeout: 30s
  model: gpt-4-vision
  endpoint: /api/v1/agents/expense-classifier
  authentication: bearer_token
```

```yaml
skill_id: invoice_agent_v1
name: Conversational Invoice Generation
description: Creates professional invoices from natural language
agent_type: conversational
capabilities:
  - natural_language_understanding
  - pdf_generation
  - payment_integration
  - email_automation

inputs:
  - name: user_input
    type: string
    required: true
    description: Natural language invoice description
  - name: structured_data
    type: object
    required: false

outputs:
  - name: invoice
    type: object
    schema:
      invoice_number: string
      pdf_url: string
      payment_url: string
      total_amount: number

watsonx_integration:
  model: gpt-4-turbo
  endpoint: /api/v1/agents/invoice
  authentication: bearer_token
```

### 3. Fraud Analyzer Agent

```yaml
skill_id: fraud_analyzer_v1
name: Real-time Fraud Detection
description: ML-powered anomaly detection for transactions
agent_type: analytical
capabilities:
  - realtime_analysis
  - ml_inference
  - risk_scoring
  - alert_generation

inputs:
  - name: transaction_data
    type: object
    required: true
    schema:
      transaction_id: string
      amount: number
      merchant: string
      timestamp: datetime

outputs:
  - name: fraud_analysis
    type: object
    schema:
      risk_score: number
      severity: string
      recommended_actions: array

execution:
  timeout: 5s
  priority: high
  streaming: true

watsonx_integration:
  model: isolation_forest + lstm
  endpoint: /api/v1/agents/fraud-analyzer
  authentication: bearer_token
```

### 4. Cashflow Forecast Agent

```yaml
skill_id: cashflow_forecast_v1
name: Predictive Cashflow Analytics
description: Time-series forecasting for financial planning
agent_type: predictive
capabilities:
  - time_series_forecasting
  - scenario_analysis
  - confidence_intervals
  - trend_detection

inputs:
  - name: user_id
    type: string
    required: true
  - name: historical_months
    type: integer
    default: 24

outputs:
  - name: forecast
    type: object
    schema:
      forecast_data: array
      scenarios: object
      metrics: object

execution:
  timeout: 60s
  scheduled: true
  schedule: "0 6 * * *"  # Daily at 6 AM

watsonx_integration:
  model: prophet + arima
  endpoint: /api/v1/agents/cashflow-forecast
  authentication: bearer_token
```

---

## Workflow Orchestration

### Complete Expense Processing Workflow

```yaml
workflow_name: expense_processing_complete
version: 1.0
description: End-to-end expense processing with fraud detection

trigger:
  type: api_call
  endpoint: /api/v1/expenses/upload
  method: POST

steps:
  - step: validate_upload
    agent: orchestrator
    action: validate_file
    inputs:
      file: ${trigger.file}
    outputs:
      validated_file: file_data
      receipt_id: generated_id

  - step: ocr_classification
    agent: expense_classifier
    action: process_receipt
    inputs:
      receipt_file: ${step.validate_upload.validated_file}
      user_id: ${trigger.user_id}
    outputs:
      expense_data: classification_result
    on_error:
      action: retry
      max_retries: 3

  - step: fraud_check
    agent: fraud_analyzer
    action: analyze_transaction
    condition: ${step.ocr_classification.expense_data.amount} > 100
    inputs:
      transaction_data: ${step.ocr_classification.expense_data}
    outputs:
      fraud_result: analysis
    parallel: false

  - step: approval_decision
    agent: orchestrator
    action: evaluate_approval
    inputs:
      expense_confidence: ${step.ocr_classification.expense_data.confidence}
      fraud_score: ${step.fraud_check.fraud_result.risk_score}
    logic:
      if: 
        - condition: ${fraud_score} > 70
          then: 
            status: pending_review
            reason: high_fraud_risk
        - condition: ${expense_confidence} < 0.9
          then:
            status: pending_review
            reason: low_confidence
        - else:
            status: approved
    outputs:
      approval_status: decision

  - step: update_ledger
    agent: orchestrator
    action: write_to_ledger
    condition: ${step.approval_decision.approval_status} == "approved"
    inputs:
      expense_data: ${step.ocr_classification.expense_data}

  - step: trigger_forecast_update
    agent: cashflow_forecast
    action: incremental_update
    async: true
    inputs:
      new_expense: ${step.ocr_classification.expense_data}

  - step: notify_user
    agent: orchestrator
    action: send_notification
    inputs:
      user_id: ${trigger.user_id}
      status: ${step.approval_decision.approval_status}
      expense_data: ${step.ocr_classification.expense_data}

response:
  status: success
  data: ${step.ocr_classification.expense_data}
  approval: ${step.approval_decision.approval_status}
  fraud_analysis: ${step.fraud_check.fraud_result}

error_handling:
  on_step_failure:
    - log_error: true
    - notify_admin: true
    - rollback: previous_state
  
  on_timeout:
    - return_partial_results: true
    - queue_for_retry: true

monitoring:
  metrics:
    - step_duration
    - success_rate
    - error_rate
  alerts:
    - condition: error_rate > 0.05
      action: notify_team
```

### Invoice Creation Workflow

```yaml
workflow_name: invoice_creation_automated
version: 1.0

trigger:
  type: multiple
  sources:
    - api_call
    - chat_message
    - email_command

steps:
  - step: parse_input
    agent: invoice_agent
    action: extract_details
    inputs:
      user_input: ${trigger.input}
    outputs:
      invoice_data: extracted

  - step: validate_completeness
    agent: orchestrator
    action: check_required_fields
    inputs:
      invoice_data: ${step.parse_input.invoice_data}
    outputs:
      is_complete: boolean
      missing_fields: array

  - step: request_clarification
    condition: ${step.validate_completeness.is_complete} == false
    agent: invoice_agent
    action: generate_clarification_prompt
    interactive: true
    goto: parse_input

  - step: generate_invoice
    agent: invoice_agent
    action: create_invoice_pdf
    inputs:
      invoice_data: ${step.parse_input.invoice_data}
    outputs:
      invoice: complete_invoice

  - step: parallel_actions
    agent: orchestrator
    action: parallel_execute
    tasks:
      - name: send_email
        agent: invoice_agent
        action: send_invoice
        inputs:
          invoice: ${step.generate_invoice.invoice}
      
      - name: create_payment_link
        agent: invoice_agent
        action: generate_payment_link
        inputs:
          invoice: ${step.generate_invoice.invoice}
      
      - name: update_crm
        agent: orchestrator
        action: sync_to_crm
        inputs:
          invoice: ${step.generate_invoice.invoice}

response:
  invoice: ${step.generate_invoice.invoice}
  email_sent: ${step.parallel_actions.send_email.status}
  payment_url: ${step.parallel_actions.create_payment_link.url}
```

---

## Event-Driven Integration

### Event Subscriptions

```yaml
event_subscriptions:
  - event_type: transaction.created
    subscriber: fraud_analyzer
    action: analyze_immediately
    priority: high
    
  - event_type: expense.approved
    subscriber: cashflow_forecast
    action: update_forecast
    priority: normal
    async: true
    
  - event_type: invoice.paid
    subscriber: cashflow_forecast
    action: update_inflow
    priority: normal
    
  - event_type: fraud.detected
    subscribers:
      - orchestrator
      - notification_service
    action: alert_and_block
    priority: critical
```

### Message Bus Configuration

```yaml
message_bus:
  provider: rabbitmq
  connection:
    host: localhost
    port: 5672
    vhost: /finagent
  
  exchanges:
    - name: agent_communication
      type: topic
      durable: true
    
    - name: workflow_events
      type: fanout
      durable: true
  
  queues:
    - name: expense_processing
      exchange: agent_communication
      routing_key: expense.*
      
    - name: fraud_alerts
      exchange: agent_communication
      routing_key: fraud.*
      priority: high
      
    - name: forecast_updates
      exchange: workflow_events
```

---

## API Integration Mapping

### FinAgent Pro → watsonx Orchestrate

```yaml
api_mappings:
  - internal_endpoint: /api/v1/expenses/upload
    watsonx_workflow: expense_processing_complete
    method: POST
    authentication:
      type: oauth2
      token_endpoint: /oauth/token
    
  - internal_endpoint: /api/v1/invoices
    watsonx_workflow: invoice_creation_automated
    method: POST
    
  - internal_endpoint: /api/v1/fraud/analyze
    watsonx_skill: fraud_analyzer_v1
    method: POST
    streaming: true
    
  - internal_endpoint: /api/v1/forecast/cashflow
    watsonx_skill: cashflow_forecast_v1
    method: GET
    caching:
      enabled: true
      ttl: 3600  # 1 hour
```

---

## Monitoring & Observability

### watsonx Dashboard Metrics

```yaml
monitoring:
  dashboards:
    - name: Agent Performance
      metrics:
        - agent_execution_time
        - agent_success_rate
        - agent_error_count
        - queue_depth
      
    - name: Workflow Health
      metrics:
        - workflow_completion_rate
        - step_failure_rate
        - average_workflow_duration
        - sla_compliance
      
    - name: Business KPIs
      metrics:
        - expenses_processed_per_hour
        - invoice_generation_time
        - fraud_detection_accuracy
        - forecast_accuracy_mape

  alerts:
    - name: high_error_rate
      condition: error_rate > 0.05
      notification:
        - email
        - slack
        - pagerduty
    
    - name: sla_breach
      condition: workflow_duration > sla_threshold
      notification:
        - email
        - slack
    
    - name: fraud_spike
      condition: fraud_alerts_per_hour > 10
      notification:
        - sms
        - pagerduty
```

---

## Deployment Configuration

### Kubernetes Integration

```yaml
kubernetes:
  namespace: finagent-pro
  
  deployments:
    - name: orchestrator
      replicas: 3
      resources:
        requests:
          cpu: "500m"
          memory: "1Gi"
        limits:
          cpu: "2000m"
          memory: "4Gi"
      
    - name: expense-classifier
      replicas: 5
      resources:
        requests:
          cpu: "1000m"
          memory: "2Gi"
          gpu: "1"
      
    - name: fraud-analyzer
      replicas: 10  # High throughput requirement
      resources:
        requests:
          cpu: "500m"
          memory: "1Gi"

  services:
    - name: orchestrator-service
      type: ClusterIP
      port: 8000
      target_port: 8000
    
    - name: agent-lb
      type: LoadBalancer
      port: 80
      target_port: 8000

  autoscaling:
    - deployment: expense-classifier
      min_replicas: 3
      max_replicas: 20
      target_cpu_utilization: 70
    
    - deployment: fraud-analyzer
      min_replicas: 5
      max_replicas: 50
      target_cpu_utilization: 80
```

---

**Configuration Version:** 1.0  
**Last Updated:** 2025-11-19  
**IBM watsonx Orchestrate Version:** 2.0+
