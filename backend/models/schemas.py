"""
Pydantic models for request/response schemas
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# ==================== User Models ====================

class User(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    company: Optional[str] = None
    role: str = "user"
    created_at: datetime


# ==================== Expense Models ====================

class ExpenseCategory(str, Enum):
    TRAVEL = "Travel"
    MEALS = "Meals & Entertainment"
    OFFICE_SUPPLIES = "Office Supplies"
    EQUIPMENT = "Equipment"
    SOFTWARE = "Software & Subscriptions"
    MARKETING = "Marketing"
    PROFESSIONAL_SERVICES = "Professional Services"
    UTILITIES = "Utilities"
    RENT = "Rent"
    INSURANCE = "Insurance"
    TRAINING = "Training & Development"
    OTHER = "Other"


class LineItem(BaseModel):
    item: str
    quantity: int = 1
    price: float


class ExpenseUploadResponse(BaseModel):
    expense_id: str
    user_id: str
    amount: Optional[float]
    currency: str = "USD"
    date: Optional[str]
    merchant: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    description: Optional[str]
    line_items: List[LineItem] = []
    payment_method: Optional[str]
    tax_amount: Optional[float]
    tip_amount: Optional[float]
    ocr_confidence: float
    classification_confidence: float
    status: str
    processed_at: str
    fraud_analysis: Optional[Dict] = None


# ==================== Invoice Models ====================

class InvoiceItem(BaseModel):
    description: str
    quantity: int = 1
    unit_price: float


class InvoiceRequest(BaseModel):
    description: Optional[str] = None
    structured_data: Optional[Dict] = None
    send_email: bool = False
    webhook_url: Optional[str] = None


class InvoiceResponse(BaseModel):
    invoice_id: str
    invoice_number: str
    client_name: str
    client_email: Optional[str]
    amount: float
    currency: str = "USD"
    due_date: Optional[str]
    items: List[Dict]
    subtotal: float
    tax_amount: float = 0
    total_amount: float
    pdf_url: str
    payment_url: str
    payment_id: str
    status: str
    created_at: str


# ==================== Fraud Models ====================

class FraudSeverity(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FraudAlert(BaseModel):
    transaction_id: str
    analysis_id: str
    risk_score: float
    severity: FraudSeverity
    alert_type: str
    confidence: float
    ml_score: float
    rule_score: float
    contributing_factors: List[str]
    explanation: str
    recommended_actions: List[str]
    requires_review: bool
    auto_block: bool
    analyzed_at: str
    alert_id: Optional[str] = None


# ==================== Cashflow Models ====================

class ForecastData(BaseModel):
    dates: List[str]
    predicted: List[float]
    lower_bound: List[float]
    upper_bound: List[float]


class NetForecastData(BaseModel):
    dates: List[str]
    net_predicted: List[float]
    net_lower: List[float]
    net_upper: List[float]
    cumulative_position: List[float]


class ScenarioData(BaseModel):
    daily_net: List[float]
    cumulative: List[float]
    description: str


class CashflowMetrics(BaseModel):
    runway_months: float
    average_burn_rate: float
    break_even_date: Optional[str]
    forecast_accuracy_mape: float
    predicted_12m_net: float
    confidence_level: str


class CashflowForecast(BaseModel):
    forecast_id: str
    user_id: str
    forecast_date: str
    horizon_days: int
    inflow_forecast: ForecastData
    outflow_forecast: ForecastData
    net_forecast: NetForecastData
    scenarios: Dict[str, ScenarioData]
    metrics: CashflowMetrics
    confidence_interval: float
    model_version: str
    generated_by: str


# ==================== Workflow Models ====================

class WorkflowRequest(BaseModel):
    workflow_type: str
    data: Dict[str, Any]
    priority: str = "normal"


class WorkflowStatus(BaseModel):
    workflow_id: str
    workflow_type: Optional[str] = None
    status: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    failed_at: Optional[str] = None
    error: Optional[str] = None
    result: Optional[Dict] = None


# ==================== Database Models ====================

from sqlalchemy import Column, String, Float, DateTime, JSON, Integer, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()


class DBUser(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    company = Column(String)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)


class DBExpense(Base):
    __tablename__ = "expenses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    expense_id = Column(String, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    filename = Column(String)
    amount = Column(Float)
    currency = Column(String, default="USD")
    date = Column(String)
    merchant = Column(String)
    category = Column(String)
    subcategory = Column(String)
    description = Column(String)
    line_items = Column(JSON)
    payment_method = Column(String)
    tax_amount = Column(Float)
    tip_amount = Column(Float)
    ocr_confidence = Column(Float)
    classification_confidence = Column(Float)
    status = Column(String)
    fraud_analysis = Column(JSON)
    processed_at = Column(DateTime, default=datetime.utcnow)
    agent = Column(String)


class DBInvoice(Base):
    __tablename__ = "invoices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    invoice_id = Column(String, unique=True, nullable=False)
    invoice_number = Column(String, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    client_name = Column(String, nullable=False)
    client_email = Column(String)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    due_date = Column(String)
    items = Column(JSON)
    subtotal = Column(Float)
    tax_amount = Column(Float)
    total_amount = Column(Float, nullable=False)
    pdf_url = Column(String)
    payment_url = Column(String)
    payment_id = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
    paid_at = Column(DateTime)


class DBFraudAlert(Base):
    __tablename__ = "fraud_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alert_id = Column(String, unique=True, nullable=False)
    transaction_id = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    risk_score = Column(Float, nullable=False)
    severity = Column(String, nullable=False)
    alert_type = Column(String)
    explanation = Column(String)
    recommended_actions = Column(JSON)
    status = Column(String, default="open")
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime)
    resolution_action = Column(String)


class DBCashflowForecast(Base):
    __tablename__ = "cashflow_forecasts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forecast_id = Column(String, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    forecast_data = Column(JSON, nullable=False)
    metrics = Column(JSON)
    model_version = Column(String)
    generated_at = Column(DateTime, default=datetime.utcnow)


class DBWorkflowLog(Base):
    __tablename__ = "workflow_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(String, unique=True, nullable=False)
    workflow_type = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(String, nullable=False)
    input_data = Column(JSON)
    result = Column(JSON)
    error = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
