import asyncio
import aiohttp
import json
from datetime import datetime
import io
from aiohttp.client_exceptions import ClientConnectorError

async def run_expense_processing_demo():
    """
    Simulate complete expense processing workflow
    """
    print("=" * 60)
    print("FINAGENT PRO - EXPENSE PROCESSING DEMO")
    print("=" * 60)
    print()
    
    # Step 1: User uploads receipt
    print("📸 STEP 1: User uploads flight receipt")
    print("   File: delta_flight_SFO_NYC.pdf")
    print("   Amount: $1,250.00")
    print()
    await asyncio.sleep(1)
    
    try:
        async with aiohttp.ClientSession() as session:
            # Build in-memory dummy file to avoid filesystem dependency
            dummy_file = io.BytesIO(b"dummy receipt bytes for demo")
            data = aiohttp.FormData()
            data.add_field('file', dummy_file.getvalue(), filename='flight_receipt.pdf', content_type='application/pdf')

            print("🤖 EXPENSE CLASSIFIER AGENT: Processing...")
            response = await session.post(
                'http://localhost:8000/api/v1/expenses/upload',
                data=data,
                headers={'Authorization': 'Bearer demo_token'}
            )

            expense_data = await response.json()
    except ClientConnectorError:
        # Backend not running: simulate a plausible response
        expense_data = {
            "expense_id": "exp_a3f8b9c4d2e1",
            "merchant": "Delta Airlines",
            "amount": 1250.0,
            "date": datetime.utcnow().date().isoformat(),
            "category": "Travel",
            "classification_confidence": 0.953,
            "fraud_analysis": {"risk_score": 45, "severity": "low", "explanation": "Transaction pattern matches your normal behavior."},
            "status": "approved"
        }
            
    print("   ✅ OCR Extraction Complete")
    print(f"      - Merchant: {expense_data.get('merchant')}")
    print(f"      - Amount: ${expense_data.get('amount')}")
    print(f"      - Date: {expense_data.get('date')}")
    print(f"      - Category: {expense_data.get('category')}")
    print(f"      - Confidence: {expense_data.get('classification_confidence') * 100:.1f}%")
    print()
    await asyncio.sleep(2)
    
    # Step 2: Fraud Analysis
    print("🔍 STEP 2: Fraud Analyzer Agent")
    print("   Analyzing transaction for anomalies...")
    print()
    await asyncio.sleep(1)
    
    fraud_analysis = expense_data.get('fraud_analysis', {})
    risk_score = fraud_analysis.get('risk_score', 0)
    
    print(f"   📊 Risk Score: {risk_score}/100")
    print(f"   🎯 Severity: {fraud_analysis.get('severity')}")
    print(f"   💡 Explanation: {fraud_analysis.get('explanation')}")
    print()
    
    if risk_score > 70:
        print("   ⚠️  HIGH RISK DETECTED!")
        print("   🚨 Creating fraud alert...")
        print("   📧 Notifying security team...")
        print("   ⏸️  Transaction held for review")
    else:
        print("   ✅ Transaction cleared - No anomalies detected")
        
    print()
    await asyncio.sleep(2)
    
    # Step 3: Approval Decision
    print("🎯 STEP 3: Orchestrator Decision")
    status = expense_data.get('status')
    
    if status == 'approved':
        print("   ✅ APPROVED - Updating ledger")
        print("   💰 Adding to expense records")
        print("   📊 Triggering cashflow forecast update")
    else:
        print("   ⏸️  PENDING REVIEW")
        print(f"   📝 Reason: {expense_data.get('review_reason')}")
        print("   👤 Assigned to: Finance Manager")
    
    print()
    await asyncio.sleep(2)
    
    # Step 4: Cashflow Impact
    print("📈 STEP 4: Cashflow Forecast Agent")
    print("   Updating 12-month forecast...")
    print("   Recalculating cash position...")
    print()
    await asyncio.sleep(1)
    
    print("   ✅ Forecast Updated")
    print("   💵 Net Impact: -$1,250.00")
    print("   📉 Runway: 11.2 months (was 11.3)")
    print("   📊 Confidence: 89%")
    print()
    
    # Step 5: Notification
    print("📱 STEP 5: User Notification")
    print("   Sending push notification...")
    print("   ✅ Receipt processed successfully!")
    print()
    
    print("=" * 60)
    print("DEMO COMPLETE - Total Time: 8.2 seconds")
    print("=" * 60)
    print()
    
    # Summary
    print("📊 WORKFLOW SUMMARY")
    print("-" * 60)
    print(f"Expense ID: {expense_data.get('expense_id')}")
    print(f"Status: {status.upper()}")
    print(f"Processing Time: 8.2s")
    print(f"Agents Involved: 4 (Classifier, Fraud, Orchestrator, Forecast)")
    print(f"Automation Rate: 100%")
    print()

if __name__ == "__main__":
    asyncio.run(run_expense_processing_demo())
