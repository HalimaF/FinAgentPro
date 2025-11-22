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


class ExpenseClassifierAgent:
    def __init__(self, huggingface_service=None):
        self.name = "ExpenseClassifierAgentStub"
        self.hf_service = huggingface_service
        logger.info(f"✅ {self.name} initialized (stub)")

    def health_status(self) -> Dict:
        return {"agent": self.name, "status": "healthy", "stub": True}

    async def process_receipt(self, file_content: bytes, filename: str, user_id: str) -> Dict:
        random.seed(42)
        amount = round(random.uniform(50, 1250), 2)
        result = {
            "expense_id": f"exp_{random.randrange(10**8):08d}",
            "user_id": user_id,
            "merchant": "Delta Airlines" if amount > 300 else "Starbucks",
            "amount": amount,
            "date": datetime.utcnow().date().isoformat(),
            "category": "Travel" if amount > 300 else "Meals",
            "classification_confidence": 0.953 if amount > 300 else 0.972,
            "status": "approved",
        }
        return result


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
        logger.info(f"✅ {self.name} initialized (stub)")

    def health_status(self) -> Dict:
        return {"agent": self.name, "status": "healthy", "stub": True}

    async def create_invoice(self, user_input: str, user_id: str, structured_data: Optional[Dict] = None) -> Dict:
        number = f"INV-{datetime.utcnow().strftime('%Y%m%d')}-0045"
        total = 12500.00 if "12,500" in user_input or "12500" in user_input else 500.00
        return {
            "invoice_id": f"inv_{datetime.utcnow().strftime('%H%M%S')}",
            "invoice_number": number,
            "client_name": "Acme Corp" if "Acme" in user_input else "Client Co",
            "items": [
                {"description": "Q4 consulting services", "quantity": 1, "unit_price": total}
            ],
            "total_amount": total,
            "due_date": (datetime.utcnow() + timedelta(days=30)).date().isoformat(),
            "pdf_url": "https://example.com/invoices/INV-demo.pdf",
            "payment_url": "https://pay.stripe.com/demo",
            "status": "sent",
        }

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
