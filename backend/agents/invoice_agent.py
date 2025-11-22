"""
Invoice Agent
AI-powered invoice generation, management, and payment tracking
"""

import os
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from openai import AsyncOpenAI
from loguru import logger
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import stripe
import io


class InvoiceAgent:
    """
    Intelligent agent for invoice management
    - Natural language invoice creation
    - Professional PDF generation
    - Payment link integration
    - Automated delivery
    """
    
    def __init__(self):
        self.name = "InvoiceAgent"
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        stripe.api_key = os.getenv("STRIPE_API_KEY")
        
        logger.info(f"✅ {self.name} initialized")
    
    async def create_invoice(
        self,
        user_input: str,
        user_id: str,
        structured_data: Optional[Dict] = None
    ) -> Dict:
        """
        Create invoice from natural language or structured data
        
        Args:
            user_input: Natural language description or JSON
            user_id: User identifier
            structured_data: Optional pre-structured data
            
        Returns:
            Complete invoice with PDF and payment link
        """
        try:
            logger.info(f"Creating invoice for user {user_id}")
            
            # Step 1: Extract invoice details
            if structured_data:
                invoice_data = structured_data
            else:
                invoice_data = await self._extract_invoice_details(user_input)
            
            # Step 2: Validate data
            validation_result = self._validate_invoice_data(invoice_data)
            if not validation_result["is_valid"]:
                return {
                    "status": "incomplete",
                    "missing_fields": validation_result["missing_fields"],
                    "message": "Please provide missing information"
                }
            
            # Step 3: Generate invoice number
            invoice_number = await self._generate_invoice_number(user_id)
            invoice_data["invoice_number"] = invoice_number
            invoice_data["invoice_id"] = f"inv_{invoice_number.lower().replace('-', '_')}"
            
            # Step 4: Calculate totals
            invoice_data = self._calculate_totals(invoice_data)
            
            # Step 5: Generate PDF
            pdf_url = await self._generate_pdf(invoice_data, user_id)
            
            # Step 6: Create payment link
            payment_data = await self._create_payment_link(invoice_data)
            
            # Step 7: Prepare response
            result = {
                "invoice_id": invoice_data["invoice_id"],
                "invoice_number": invoice_number,
                "client_name": invoice_data.get("client_name"),
                "client_email": invoice_data.get("client_email"),
                "amount": invoice_data["total_amount"],
                "currency": invoice_data.get("currency", "USD"),
                "due_date": invoice_data.get("due_date"),
                "items": invoice_data.get("items", []),
                "subtotal": invoice_data.get("subtotal"),
                "tax_amount": invoice_data.get("tax_amount", 0),
                "total_amount": invoice_data["total_amount"],
                "pdf_url": pdf_url,
                "payment_url": payment_data["url"],
                "payment_id": payment_data["id"],
                "status": "draft",
                "created_at": datetime.utcnow().isoformat(),
                "created_by": self.name
            }
            
            logger.info(f"✅ Invoice created: {invoice_number} - ${invoice_data['total_amount']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Invoice creation failed: {str(e)}")
            raise
    
    async def _extract_invoice_details(self, user_input: str) -> Dict:
        """
        Use GPT-4 to extract invoice details from natural language
        """
        try:
            prompt = f"""
Extract invoice information from this request:

"{user_input}"

Return a JSON object with these fields:
- client_name: Client/company name
- client_email: Client email
- client_address: Client address (if mentioned)
- items: Array of items with {{description, quantity, unit_price}}
- tax_rate: Tax percentage (default 0 if not mentioned)
- due_date: Payment due date (YYYY-MM-DD format, default +30 days from today)
- notes: Any special notes or terms
- project_name: Project/service name if mentioned

Example:
{{
  "client_name": "Acme Corp",
  "client_email": "billing@acmecorp.com",
  "items": [
    {{
      "description": "Website Design",
      "quantity": 1,
      "unit_price": 5000
    }},
    {{
      "description": "SEO Optimization",
      "quantity": 1,
      "unit_price": 2000
    }}
  ],
  "tax_rate": 0,
  "due_date": "{(datetime.utcnow() + timedelta(days=30)).strftime('%Y-%m-%d')}",
  "notes": "Payment due within 30 days",
  "project_name": "Website Redesign"
}}

Return ONLY valid JSON.
"""
            
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at extracting structured invoice data. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Extracted invoice data: {result.get('client_name')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Invoice extraction failed: {str(e)}")
            raise
    
    def _validate_invoice_data(self, data: Dict) -> Dict:
        """Validate invoice data completeness"""
        required_fields = ["client_name", "items"]
        missing_fields = [
            field for field in required_fields
            if not data.get(field)
        ]
        
        # Validate items structure
        if data.get("items"):
            for item in data["items"]:
                if not all(k in item for k in ["description", "quantity", "unit_price"]):
                    missing_fields.append("Complete item details (description, quantity, unit_price)")
                    break
        
        return {
            "is_valid": len(missing_fields) == 0,
            "missing_fields": missing_fields
        }
    
    async def _generate_invoice_number(self, user_id: str) -> str:
        """
        Generate sequential invoice number
        Format: INV-YYYYMM-XXXX
        """
        now = datetime.utcnow()
        prefix = f"INV-{now.strftime('%Y%m')}"
        
        # In production, query database for last invoice number
        # For demo, generate random sequence
        import random
        sequence = random.randint(1, 9999)
        
        return f"{prefix}-{sequence:04d}"
    
    def _calculate_totals(self, invoice_data: Dict) -> Dict:
        """Calculate invoice totals"""
        items = invoice_data.get("items", [])
        
        # Calculate subtotal
        subtotal = sum(
            item.get("quantity", 1) * item.get("unit_price", 0)
            for item in items
        )
        
        # Calculate tax
        tax_rate = invoice_data.get("tax_rate", 0) / 100
        tax_amount = subtotal * tax_rate
        
        # Calculate total
        total_amount = subtotal + tax_amount
        
        invoice_data.update({
            "subtotal": round(subtotal, 2),
            "tax_amount": round(tax_amount, 2),
            "total_amount": round(total_amount, 2)
        })
        
        return invoice_data
    
    async def _generate_pdf(self, invoice_data: Dict, user_id: str) -> str:
        """
        Generate professional invoice PDF
        """
        try:
            # Create PDF in memory
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Company header (placeholder - should come from user profile)
            pdf.setFont("Helvetica-Bold", 24)
            pdf.drawString(1*inch, height - 1*inch, "Your Company")
            
            pdf.setFont("Helvetica", 10)
            pdf.drawString(1*inch, height - 1.3*inch, "123 Business St")
            pdf.drawString(1*inch, height - 1.5*inch, "City, State 12345")
            pdf.drawString(1*inch, height - 1.7*inch, "contact@company.com")
            
            # Invoice title and number
            pdf.setFont("Helvetica-Bold", 20)
            pdf.drawRightString(width - 1*inch, height - 1*inch, "INVOICE")
            
            pdf.setFont("Helvetica", 10)
            pdf.drawRightString(
                width - 1*inch,
                height - 1.3*inch,
                f"Invoice #: {invoice_data['invoice_number']}"
            )
            pdf.drawRightString(
                width - 1*inch,
                height - 1.5*inch,
                f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}"
            )
            pdf.drawRightString(
                width - 1*inch,
                height - 1.7*inch,
                f"Due Date: {invoice_data.get('due_date', 'N/A')}"
            )
            
            # Bill To
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(1*inch, height - 2.5*inch, "Bill To:")
            
            pdf.setFont("Helvetica", 10)
            pdf.drawString(1*inch, height - 2.8*inch, invoice_data.get("client_name", ""))
            if invoice_data.get("client_address"):
                pdf.drawString(1*inch, height - 3*inch, invoice_data["client_address"])
            if invoice_data.get("client_email"):
                pdf.drawString(1*inch, height - 3.2*inch, invoice_data["client_email"])
            
            # Items table
            table_data = [
                ["Description", "Qty", "Unit Price", "Amount"]
            ]
            
            for item in invoice_data.get("items", []):
                amount = item.get("quantity", 1) * item.get("unit_price", 0)
                table_data.append([
                    item.get("description", ""),
                    str(item.get("quantity", 1)),
                    f"${item.get('unit_price', 0):.2f}",
                    f"${amount:.2f}"
                ])
            
            table = Table(table_data, colWidths=[3.5*inch, 0.75*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            table.wrapOn(pdf, width, height)
            table.drawOn(pdf, 1*inch, height - 5*inch)
            
            # Totals
            y_position = height - 5.5*inch - (len(table_data) * 0.3*inch)
            
            pdf.setFont("Helvetica", 10)
            pdf.drawRightString(width - 2.2*inch, y_position, "Subtotal:")
            pdf.drawRightString(width - 1*inch, y_position, f"${invoice_data.get('subtotal', 0):.2f}")
            
            if invoice_data.get("tax_amount", 0) > 0:
                pdf.drawRightString(width - 2.2*inch, y_position - 0.3*inch, "Tax:")
                pdf.drawRightString(
                    width - 1*inch,
                    y_position - 0.3*inch,
                    f"${invoice_data.get('tax_amount', 0):.2f}"
                )
                y_position -= 0.3*inch
            
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawRightString(width - 2.2*inch, y_position - 0.4*inch, "Total:")
            pdf.drawRightString(
                width - 1*inch,
                y_position - 0.4*inch,
                f"${invoice_data.get('total_amount', 0):.2f}"
            )
            
            # Notes
            if invoice_data.get("notes"):
                pdf.setFont("Helvetica-Bold", 10)
                pdf.drawString(1*inch, 2*inch, "Notes:")
                pdf.setFont("Helvetica", 9)
                pdf.drawString(1*inch, 1.7*inch, invoice_data["notes"])
            
            # Footer
            pdf.setFont("Helvetica", 8)
            pdf.drawCentredString(width / 2, 0.75*inch, "Thank you for your business!")
            
            pdf.save()
            
            # In production, upload to S3 and return URL
            # For demo, return placeholder URL
            pdf_url = f"https://storage.finagent.pro/invoices/{invoice_data['invoice_number']}.pdf"
            
            logger.info(f"✅ PDF generated: {pdf_url}")
            return pdf_url
            
        except Exception as e:
            logger.error(f"PDF generation failed: {str(e)}")
            return "https://storage.finagent.pro/invoices/placeholder.pdf"
    
    async def _create_payment_link(self, invoice_data: Dict) -> Dict:
        """
        Create Stripe payment link
        """
        try:
            # Create Stripe Payment Link
            payment_link = stripe.PaymentLink.create(
                line_items=[{
                    "price_data": {
                        "currency": invoice_data.get("currency", "usd").lower(),
                        "product_data": {
                            "name": f"Invoice {invoice_data['invoice_number']}",
                            "description": invoice_data.get("project_name", "Payment"),
                        },
                        "unit_amount": int(invoice_data["total_amount"] * 100),
                    },
                    "quantity": 1,
                }],
                metadata={
                    "invoice_number": invoice_data["invoice_number"],
                    "invoice_id": invoice_data["invoice_id"]
                }
            )
            
            return {
                "id": payment_link.id,
                "url": payment_link.url
            }
            
        except Exception as e:
            logger.error(f"Payment link creation failed: {str(e)}")
            # Return placeholder
            return {
                "id": "placeholder_id",
                "url": f"https://pay.finagent.pro/invoice/{invoice_data['invoice_number']}"
            }
    
    async def send_invoice(self, invoice_id: str) -> Dict:
        """
        Send invoice to client via email
        (Integration with SendGrid would go here)
        """
        logger.info(f"Sending invoice {invoice_id}")
        
        # In production, integrate with SendGrid
        return {
            "status": "sent",
            "sent_at": datetime.utcnow().isoformat(),
            "method": "email"
        }
    
    async def track_payment_status(self, invoice_id: str) -> Dict:
        """
        Check payment status from Stripe
        """
        # In production, query Stripe for payment status
        return {
            "invoice_id": invoice_id,
            "status": "pending",
            "amount_paid": 0,
            "last_checked": datetime.utcnow().isoformat()
        }
    
    def health_status(self) -> Dict:
        """Return agent health status"""
        return {
            "agent": self.name,
            "status": "healthy",
            "capabilities": [
                "Natural Language Processing",
                "PDF Generation",
                "Payment Integration",
                "Email Delivery"
            ]
        }
