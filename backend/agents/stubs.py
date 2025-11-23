"""
Lightweight stub agents for DEMO_MODE
Avoid heavy ML/ocr/payment dependencies. Returns plausible demo outputs.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger
import asyncio
import random
import base64
import io

# In-memory storage for demo mode
_expense_storage = {}
_invoice_storage = {}


class ExpenseClassifierAgent:
    def __init__(self, huggingface_service=None):
        self.name = "ExpenseClassifierAgentStub"
        self.hf_service = huggingface_service
        self.expenses_by_user = {}  # Track expenses for analytics
        logger.info(f"✅ {self.name} initialized (stub)")

    def health_status(self) -> Dict:
        return {"agent": self.name, "status": "healthy", "stub": True}

    async def process_receipt(self, file_content: bytes, filename: str, user_id: str) -> Dict:
        # Generate varied demo data
        file_hash = len(file_content) % 100
        amount = round(50 + (file_hash * 30), 2)
        
        merchants = ["Starbucks", "Delta Airlines", "Amazon Web Services", "Office Depot", "Uber", "WeWork"]
        categories = ["Meals", "Travel", "Software", "Office Supplies", "Transportation", "Rent"]
        idx = file_hash % len(merchants)
        
        expense_id = f"exp_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{file_hash:02d}"
        
        # Store file content as base64 for viewing
        receipt_data = base64.b64encode(file_content).decode('utf-8')
        _expense_storage[expense_id] = {
            "file_content": receipt_data,
            "filename": filename,
            "content_type": "image/png" if filename.lower().endswith('.png') else "image/jpeg"
        }
        
        result = {
            "expense_id": expense_id,
            "user_id": user_id,
            "merchant": merchants[idx],
            "amount": amount,
            "date": (datetime.utcnow() - timedelta(days=file_hash % 30)).date().isoformat(),
            "category": categories[idx],
            "classification_confidence": 0.90 + (file_hash % 10) / 100,
            "status": "approved" if amount < 1000 else "pending_review",
            "receipt_url": f"/api/v1/expenses/{expense_id}/receipt",
        }
        
        # Store expense for analytics
        if user_id not in self.expenses_by_user:
            self.expenses_by_user[user_id] = []
        self.expenses_by_user[user_id].append(result)
        
        return result
    
    def get_receipt(self, expense_id: str) -> Optional[Dict]:
        """Get stored receipt data"""
        return _expense_storage.get(expense_id)
    
    def get_analytics(self, user_id: str) -> Dict:
        """Get expense analytics for a user"""
        expenses = self.expenses_by_user.get(user_id, [])
        
        if not expenses:
            # Return sample data if no expenses yet
            return {
                "total_expenses": 48392.00,
                "expense_count": 127,
                "average_expense": 381.00,
                "by_category": {
                    "Meals": 8234.50,
                    "Travel": 15890.00,
                    "Software": 12450.00,
                    "Office Supplies": 5678.50,
                    "Transportation": 3245.00,
                    "Rent": 2894.00
                },
                "by_status": {
                    "approved": 115,
                    "pending_review": 8,
                    "rejected": 4
                },
                "recent_trend": [
                    {"month": "Jan", "total": 3850.00},
                    {"month": "Feb", "total": 4120.00},
                    {"month": "Mar", "total": 3980.00},
                    {"month": "Apr", "total": 5240.00},
                    {"month": "May", "total": 4580.00},
                    {"month": "Jun", "total": 5120.00}
                ],
                "top_merchants": [
                    {"merchant": "Amazon Web Services", "total": 8920.00, "count": 12},
                    {"merchant": "Delta Airlines", "total": 7850.00, "count": 6},
                    {"merchant": "Office Depot", "total": 4230.00, "count": 28},
                    {"merchant": "Starbucks", "total": 2156.00, "count": 47},
                    {"merchant": "Uber", "total": 1890.00, "count": 34}
                ]
            }
        
        # Calculate actual analytics from stored expenses
        total = sum(e["amount"] for e in expenses)
        count = len(expenses)
        by_category = {}
        by_status = {}
        
        for expense in expenses:
            cat = expense["category"]
            by_category[cat] = by_category.get(cat, 0) + expense["amount"]
            
            status = expense["status"]
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            "total_expenses": round(total, 2),
            "expense_count": count,
            "average_expense": round(total / count if count > 0 else 0, 2),
            "by_category": by_category,
            "by_status": by_status,
            "recent_trend": [
                {"month": "Current", "total": round(total, 2)}
            ],
            "top_merchants": []
        }


class FraudAnalyzerAgent:
    def __init__(self):
        self.name = "FraudAnalyzerAgentStub"
        logger.info(f"✅ {self.name} initialized (stub)")

    def health_status(self) -> Dict:
        return {"agent": self.name, "status": "healthy", "stub": True}

    async def analyze_transaction(self, transaction_id: str, user_id: str, amount: float, merchant: str, category: str) -> Dict:
        risk = 85 if amount >= 5000 or merchant.startswith("Tech") else 45
        severity = "high" if risk >= 80 else "low"
        return {
            "transaction_id": transaction_id,
            "user_id": user_id,
            "risk_score": risk,
            "severity": severity,
            "explanation": "Amount 20x above average" if risk >= 80 else "Within normal pattern",
        }


class InvoiceAgent:
    def __init__(self):
        self.name = "InvoiceAgentStub"
        self.invoices_by_user = {}  # Track invoices for management
        logger.info(f"✅ {self.name} initialized (stub)")

    def health_status(self) -> Dict:
        return {"agent": self.name, "status": "healthy", "stub": True}

    async def create_invoice(self, user_input: str, user_id: str, structured_data: Optional[Dict] = None) -> Dict:
        number = f"INV-{datetime.utcnow().strftime('%Y%m%d%H%M')}"
        
        # Extract amount from input
        import re
        amount_match = re.search(r'\$?([\d,]+(?:\.\d{2})?)', user_input)
        total = float(amount_match.group(1).replace(',', '')) if amount_match else 500.00
        
        # Extract client name
        client_name = "Client Co"
        for word in ["Acme", "Corp", "Inc", "LLC", "Ltd"]:
            if word.lower() in user_input.lower():
                client_name = f"{word} Corporation"
                break
        
        invoice_id = f"inv_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        # Generate simple PDF-like text (in real app use reportlab)
        pdf_content = f"""INVOICE

Invoice Number: {number}
Date: {datetime.utcnow().date().isoformat()}

BILL TO:
{client_name}

ITEMS:
Description: Professional Services
Quantity: 1
Unit Price: ${total:.2f}

TOTAL: ${total:.2f}

Due Date: {(datetime.utcnow() + timedelta(days=30)).date().isoformat()}

Thank you for your business!
"""
        # Store as base64
        pdf_bytes = pdf_content.encode('utf-8')
        _invoice_storage[invoice_id] = base64.b64encode(pdf_bytes).decode('utf-8')
        
        invoice_data = {
            "invoice_id": invoice_id,
            "invoice_number": number,
            "client_name": client_name,
            "items": [
                {"description": "Professional Services", "quantity": 1, "unit_price": total}
            ],
            "total_amount": total,
            "due_date": (datetime.utcnow() + timedelta(days=30)).date().isoformat(),
            "pdf_url": f"/api/v1/invoices/{invoice_id}/pdf",
            "payment_url": f"https://pay.demo.com/{invoice_id}",
            "status": "sent",
            "payment_status": "pending",
            "created_date": datetime.utcnow().isoformat(),
        }
        
        # Store invoice for tracking
        if user_id not in self.invoices_by_user:
            self.invoices_by_user[user_id] = []
        self.invoices_by_user[user_id].append(invoice_data)
        
        return invoice_data
    
    def get_invoice_pdf(self, invoice_id: str) -> Optional[str]:
        """Get stored invoice PDF as base64"""
        return _invoice_storage.get(invoice_id)
    
    def get_invoices(self, user_id: str, status: Optional[str] = None) -> List[Dict]:
        """Get invoices for a user, optionally filtered by status"""
        invoices = self.invoices_by_user.get(user_id, [])
        
        if not invoices:
            # Return sample data if no invoices yet
            return [
                {
                    "invoice_id": "inv_sample1",
                    "invoice_number": "INV-20240101",
                    "client_name": "Acme Corporation",
                    "total_amount": 5000.00,
                    "due_date": (datetime.utcnow() + timedelta(days=15)).date().isoformat(),
                    "payment_status": "pending",
                    "status": "sent",
                    "created_date": (datetime.utcnow() - timedelta(days=15)).isoformat(),
                },
                {
                    "invoice_id": "inv_sample2",
                    "invoice_number": "INV-20240115",
                    "client_name": "Corp Inc",
                    "total_amount": 3200.00,
                    "due_date": (datetime.utcnow() + timedelta(days=5)).date().isoformat(),
                    "payment_status": "paid",
                    "status": "sent",
                    "created_date": (datetime.utcnow() - timedelta(days=25)).isoformat(),
                },
                {
                    "invoice_id": "inv_sample3",
                    "invoice_number": "INV-20240120",
                    "client_name": "Tech LLC",
                    "total_amount": 7500.00,
                    "due_date": (datetime.utcnow() - timedelta(days=5)).date().isoformat(),
                    "payment_status": "overdue",
                    "status": "sent",
                    "created_date": (datetime.utcnow() - timedelta(days=35)).isoformat(),
                },
            ]
        
        if status:
            invoices = [inv for inv in invoices if inv.get("payment_status") == status]
        
        return invoices
    
    def update_invoice_status(self, invoice_id: str, payment_status: str) -> bool:
        """Update invoice payment status"""
        for user_invoices in self.invoices_by_user.values():
            for invoice in user_invoices:
                if invoice["invoice_id"] == invoice_id:
                    invoice["payment_status"] = payment_status
                    return True
        return False

    async def send_invoice(self, invoice_id: str):
        await asyncio.sleep(0.1)
        logger.info(f"Invoice sent (stub): {invoice_id}")


class CashflowForecastAgent:
    def __init__(self):
        self.name = "CashflowForecastAgentStub"
        self.confidence_interval = 0.95
        logger.info(f"✅ {self.name} initialized (stub)")

    def health_status(self) -> Dict:
        return {"agent": self.name, "status": "healthy", "stub": True}

    async def generate_forecast(self, user_id: str) -> Dict:
        today = datetime.utcnow().date()
        net_series = [{"date": (today + timedelta(days=i)).isoformat(), "value": 1000 + i * 5} for i in range(30)]
        return {
            "forecast_id": f"fc_{datetime.utcnow().strftime('%H%M%S')}",
            "user_id": user_id,
            "forecast_date": datetime.utcnow().isoformat(),
            "horizon_days": 30,
            "net_forecast": net_series,
            "scenarios": {
                "best": [{"date": d["date"], "value": d["value"] * 1.2} for d in net_series],
                "expected": net_series,
                "worst": [{"date": d["date"], "value": d["value"] * 0.8} for d in net_series],
            },
            "metrics": {"runway_months": 12.3, "burn_rate": 25000},
            "confidence_interval": self.confidence_interval,
        }

    async def incremental_update(self, user_id: str, new_data: Dict):
        await asyncio.sleep(0.05)
        logger.info("Cashflow incremental update (stub)")
