"""
Expense Classifier Agent
Handles OCR, extraction, and AI-powered categorization of expenses
Enhanced with Hugging Face LLM integration
"""

import os
import asyncio
from typing import Dict, Optional, List
from datetime import datetime
import pytesseract
from PIL import Image
import io
from openai import AsyncOpenAI
from loguru import logger
import json

# Configure Tesseract path if provided via environment
tesseract_env_path = os.getenv("TESSERACT_PATH")
if tesseract_env_path and os.path.isfile(tesseract_env_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_env_path
elif os.name == "nt":
    # Fallback to common Windows install path
    default_tesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    if os.path.isfile(default_tesseract):
        pytesseract.pytesseract.tesseract_cmd = default_tesseract


class ExpenseClassifierAgent:
    """
    Intelligent agent for expense classification
    - OCR processing for receipts
    - GPT-4 powered categorization (fallback)
    - Hugging Face LLM for enhanced analysis
    - Confidence scoring
    - Multi-language support
    """
    
    def __init__(self, huggingface_service=None):
        self.name = "ExpenseClassifierAgent"
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4-vision-preview"
        self.hf_service = huggingface_service
        
        # Expense categories
        self.categories = [
            "Travel", "Meals & Entertainment", "Office Supplies",
            "Equipment", "Software & Subscriptions", "Marketing",
            "Professional Services", "Utilities", "Rent",
            "Insurance", "Training & Development", "Other"
        ]
        
        logger.info(f"✅ {self.name} initialized")
    
    async def process_receipt(
        self,
        file_content: bytes,
        filename: str,
        user_id: str
    ) -> Dict:
        """
        Main processing pipeline for expense receipts
        Now enhanced with Hugging Face LLM
        
        Args:
            file_content: Raw file bytes
            filename: Original filename
            user_id: User identifier
            
        Returns:
            Structured expense data with classification
        """
        try:
            logger.info(f"Processing receipt: {filename}")
            
            # Step 1: OCR Extraction
            ocr_result = await self._perform_ocr(file_content)
            
            # Step 2: Try Hugging Face enhanced analysis first
            if self.hf_service:
                try:
                    hf_result = await self.hf_service.analyze_receipt_with_llm(
                        receipt_text=ocr_result["text"],
                        receipt_image_path=None  # We have bytes, not path
                    )
                    logger.info("✅ Hugging Face LLM analysis complete")
                    
                    # Use HF result as primary classification
                    classification_result = hf_result
                except Exception as hf_error:
                    logger.warning(f"HF analysis failed, falling back to GPT-4: {hf_error}")
                    # Fallback to GPT-4
                    classification_result = await self._classify_with_gpt4(
                        ocr_text=ocr_result["text"],
                        file_content=file_content
                    )
            else:
                # No HF service available, use GPT-4
                classification_result = await self._classify_with_gpt4(
                    ocr_text=ocr_result["text"],
                    file_content=file_content
                )
            
            # Step 3: Confidence Scoring
            confidence_score = self._calculate_confidence(
                ocr_result,
                classification_result
            )
            
            # Step 4: Structure Result
            expense_data = {
                "expense_id": self._generate_expense_id(),
                "user_id": user_id,
                "filename": filename,
                "amount": classification_result.get("amount"),
                "currency": classification_result.get("currency", "USD"),
                "date": classification_result.get("date"),
                "merchant": classification_result.get("merchant"),
                "category": classification_result.get("category"),
                "subcategory": classification_result.get("subcategory"),
                "description": classification_result.get("description"),
                "line_items": classification_result.get("line_items", []),
                "payment_method": classification_result.get("payment_method"),
                "tax_amount": classification_result.get("tax_amount"),
                "tip_amount": classification_result.get("tip_amount"),
                "ocr_confidence": ocr_result.get("confidence", 0.0),
                "classification_confidence": confidence_score,
                "status": "pending_review" if confidence_score < 0.9 else "approved",
                "processed_at": datetime.utcnow().isoformat(),
                "agent": self.name,
                "raw_ocr_text": ocr_result["text"],
                "ai_model": "huggingface" if self.hf_service else "gpt4"
            }
            
            logger.info(f"✅ Receipt processed: {expense_data['category']} - ${expense_data['amount']}")
            return expense_data
            
        except Exception as e:
            logger.error(f"❌ Receipt processing failed: {str(e)}")
            raise
    
    async def _perform_ocr(self, file_content: bytes) -> Dict:
        """
        Extract text from receipt image using OCR
        """
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(file_content))
            
            # Perform OCR with Tesseract
            text = pytesseract.image_to_string(image)
            
            # Get confidence data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                "text": text,
                "confidence": avg_confidence / 100,
                "method": "tesseract"
            }
            
        except Exception as e:
            logger.error(f"OCR failed: {str(e)}")
            # Fallback: return empty result
            return {"text": "", "confidence": 0.0, "method": "failed"}
    
    async def _classify_with_gpt4(
        self,
        ocr_text: str,
        file_content: bytes
    ) -> Dict:
        """
        Use GPT-4 Vision to extract and classify expense information
        """
        try:
            # Prepare prompt
            prompt = f"""
You are an expert financial assistant analyzing a receipt/expense document.

Extract the following information from this receipt:

1. **Amount**: Total amount (number only)
2. **Currency**: Currency code (e.g., USD, EUR)
3. **Date**: Transaction date (YYYY-MM-DD format)
4. **Merchant**: Business/vendor name
5. **Category**: One of {', '.join(self.categories)}
6. **Subcategory**: More specific classification
7. **Description**: Brief description of the expense
8. **Line Items**: List of individual items purchased (if applicable)
9. **Payment Method**: Cash, Credit Card, etc.
10. **Tax Amount**: Tax/VAT amount (if shown)
11. **Tip Amount**: Tip/gratuity (if applicable)

OCR Text:
{ocr_text}

Return ONLY a valid JSON object with these fields. If a field is not found, use null.

Example:
{{
  "amount": 125.50,
  "currency": "USD",
  "date": "2025-11-19",
  "merchant": "Office Depot",
  "category": "Office Supplies",
  "subcategory": "Stationery",
  "description": "Office supplies for Q4",
  "line_items": [
    {{"item": "Paper Reams", "quantity": 5, "price": 25.00}},
    {{"item": "Pens", "quantity": 10, "price": 15.50}}
  ],
  "payment_method": "Credit Card",
  "tax_amount": 10.50,
  "tip_amount": null
}}
"""
            
            # Call GPT-4
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial data extraction expert. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            logger.info(f"GPT-4 classification: {result.get('category')} - ${result.get('amount')}")
            
            return result
            
        except Exception as e:
            logger.error(f"GPT-4 classification failed: {str(e)}")
            # Return minimal structure
            return {
                "amount": None,
                "category": "Other",
                "merchant": "Unknown"
            }
    
    def _calculate_confidence(
        self,
        ocr_result: Dict,
        classification_result: Dict
    ) -> float:
        """
        Calculate overall confidence score for the classification
        """
        confidence_factors = []
        
        # OCR quality
        confidence_factors.append(ocr_result.get("confidence", 0.0))
        
        # Data completeness (0-1 scale)
        required_fields = ["amount", "date", "merchant", "category"]
        present_fields = sum(
            1 for field in required_fields 
            if classification_result.get(field) is not None
        )
        completeness = present_fields / len(required_fields)
        confidence_factors.append(completeness)
        
        # Amount validity
        amount = classification_result.get("amount")
        if amount and isinstance(amount, (int, float)) and amount > 0:
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.0)
        
        # Category confidence (known categories get higher score)
        category = classification_result.get("category", "")
        if category in self.categories:
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(0.5)
        
        # Calculate weighted average
        return sum(confidence_factors) / len(confidence_factors)
    
    def _generate_expense_id(self) -> str:
        """Generate unique expense ID"""
        from uuid import uuid4
        return f"exp_{uuid4().hex[:12]}"
    
    async def batch_process(
        self,
        files: List[tuple],
        user_id: str
    ) -> List[Dict]:
        """
        Process multiple receipts in parallel
        
        Args:
            files: List of (file_content, filename) tuples
            user_id: User identifier
            
        Returns:
            List of processed expense records
        """
        tasks = [
            self.process_receipt(content, filename, user_id)
            for content, filename in files
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        successful = [r for r in results if not isinstance(r, Exception)]
        errors = [r for r in results if isinstance(r, Exception)]
        
        if errors:
            logger.warning(f"⚠️ {len(errors)} receipts failed to process")
        
        return successful
    
    def health_status(self) -> Dict:
        """Return agent health status"""
        return {
            "agent": self.name,
            "status": "healthy",
            "model": self.model,
            "categories": len(self.categories),
            "capabilities": [
                "OCR",
                "AI Classification",
                "Multi-language",
                "Batch Processing"
            ]
        }
    
    async def improve_classification(
        self,
        expense_id: str,
        corrections: Dict
    ) -> Dict:
        """
        Learn from user corrections to improve future classifications
        (Placeholder for ML model retraining logic)
        """
        logger.info(f"Learning from correction for expense {expense_id}")
        
        # Store correction for future model training
        return {
            "status": "learned",
            "expense_id": expense_id,
            "corrections_applied": corrections
        }
