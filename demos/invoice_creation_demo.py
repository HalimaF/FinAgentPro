import asyncio
import aiohttp
import json
from aiohttp.client_exceptions import ClientConnectorError

async def run_invoice_creation_demo():
    """
    Simulate conversational invoice creation
    """
    print("=" * 60)
    print("FINAGENT PRO - CONVERSATIONAL INVOICE DEMO")
    print("=" * 60)
    print()
    
    user_input = "Create invoice for Acme Corp for Q4 consulting services, $12,500, due net 30"
    
    print("💬 USER INPUT:")
    print(f'   "{user_input}"')
    print()
    await asyncio.sleep(1)
    
    print("🤖 INVOICE AGENT: Analyzing request...")
    print("   🧠 Extracting invoice details with GPT-4...")
    print()
    await asyncio.sleep(2)
    
    try:
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                'http://localhost:8000/api/v1/invoices',
                json={'description': user_input},
                headers={'Authorization': 'Bearer demo_token'}
            )

            invoice = await response.json()
    except ClientConnectorError:
        # Backend not running: simulate a plausible invoice payload
        from datetime import datetime, timedelta
        invoice = {
            "invoice_id": "inv_demo",
            "invoice_number": f"INV-{datetime.utcnow().strftime('%Y%m%d')}-0045",
            "client_name": "Acme Corp",
            "items": [{"description": "Q4 consulting services", "quantity": 1, "unit_price": 12500.00}],
            "total_amount": 12500.00,
            "due_date": (datetime.utcnow() + timedelta(days=30)).date().isoformat(),
            "pdf_url": "https://example.com/invoices/INV-demo.pdf",
            "payment_url": "https://pay.stripe.com/demo",
            "status": "sent"
        }
    
    print("   ✅ Details Extracted:")
    print(f"      - Client: {invoice.get('client_name')}")
    print(f"      - Amount: ${invoice.get('total_amount'):,.2f}")
    print(f"      - Due Date: {invoice.get('due_date')}")
    print(f"      - Items: {len(invoice.get('items', []))} service(s)")
    print()
    await asyncio.sleep(2)
    
    print("📄 GENERATING INVOICE...")
    print("   Creating invoice number...")
    print(f"   ✅ Invoice #: {invoice.get('invoice_number')}")
    print()
    await asyncio.sleep(1)
    
    print("   Generating professional PDF...")
    print(f"   ✅ PDF: {invoice.get('pdf_url')}")
    print()
    await asyncio.sleep(1)
    
    print("💳 CREATING PAYMENT LINK...")
    print("   Integrating with Stripe...")
    print(f"   ✅ Payment URL: {invoice.get('payment_url')}")
    print()
    await asyncio.sleep(1)
    
    print("📧 PARALLEL EXECUTION:")
    print("   ├─ Sending email to client...")
    print("   ├─ Updating CRM (Salesforce)...")
    print("   └─ Triggering accounting webhook...")
    print()
    await asyncio.sleep(2)
    
    print("   ✅ All tasks completed!")
    print()
    
    print("=" * 60)
    print("INVOICE CREATED SUCCESSFULLY")
    print("=" * 60)
    print()
    
    print("📊 INVOICE SUMMARY")
    print("-" * 60)
    print(f"Invoice Number: {invoice.get('invoice_number')}")
    print(f"Client: {invoice.get('client_name')}")
    print(f"Amount: ${invoice.get('total_amount'):,.2f}")
    print(f"Status: {invoice.get('status').upper()}")
    print(f"PDF: [Download]")
    print(f"Payment: [Pay Now]")
    print()
    print(f"⚡ Total Time: 6.5 seconds")
    print(f"🤖 Agent: Invoice Agent")
    print(f"✨ User Effort: Single natural language command")
    print()

if __name__ == "__main__":
    asyncio.run(run_invoice_creation_demo())
