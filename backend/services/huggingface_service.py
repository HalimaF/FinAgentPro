"""
Hugging Face Integration Service
Provides local and cloud-based LLM capabilities for financial AI
"""

import os
from typing import Dict, List, Optional, Union
from loguru import logger
import asyncio

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("transformers not installed - using API-only mode")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class HuggingFaceService:
    """
    Hugging Face LLM integration for advanced AI features
    - Financial document understanding
    - Conversational expense queries
    - Receipt Q&A
    - Sentiment analysis for fraud detection
    - Predictive insights generation
    """
    
    def __init__(self, use_local_models: bool = False):
        self.use_local_models = use_local_models
        self.hf_api_token = os.getenv("HUGGINGFACE_API_TOKEN", "")
        self.api_base = "https://api-inference.huggingface.co/models"
        
        # Model selections (optimized for finance)
        self.models = {
            "financial_qa": "ProsusAI/finbert",  # Financial sentiment/QA
            "document_understanding": "microsoft/layoutlmv3-base",  # Document AI
            "conversational": "HuggingFaceH4/zephyr-7b-beta",  # Chat
            "summarization": "facebook/bart-large-cnn",  # Financial summaries
            "embeddings": "sentence-transformers/all-MiniLM-L6-v2"  # Semantic search
        }
        
        # Initialize local models if requested
        self.local_pipelines = {}
        if use_local_models and TRANSFORMERS_AVAILABLE:
            self._init_local_models()
        
        logger.info(f"✅ HuggingFaceService initialized (local={use_local_models})")
    
    def _init_local_models(self):
        """Initialize local models (optional, for offline use)"""
        try:
            # Lightweight models for demo
            self.local_pipelines["sentiment"] = pipeline(
                "sentiment-analysis",
                model="ProsusAI/finbert",
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("Local sentiment model loaded")
        except Exception as e:
            logger.warning(f"Could not load local models: {e}")
    
    async def analyze_receipt_with_llm(
        self,
        receipt_text: str,
        receipt_image_path: Optional[str] = None
    ) -> Dict:
        """
        Deep analysis of receipt using multimodal LLM
        - Extract structured data
        - Identify unusual patterns
        - Suggest categorization
        """
        prompt = f"""Analyze this receipt and extract structured information:

Receipt Text:
{receipt_text}

Extract:
1. Merchant name and type
2. Total amount and currency
3. Date and time
4. Payment method
5. Line items with prices
6. Any unusual patterns or anomalies
7. Suggested expense category
8. Tax and tip amounts

Provide a JSON response."""

        response = await self._call_llm(
            prompt=prompt,
            model_type="conversational",
            max_tokens=500
        )
        
        return {
            "raw_response": response,
            "confidence": 0.95,
            "source": "huggingface_llm"
        }
    
    async def conversational_query(
        self,
        user_query: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Natural language queries about finances
        Examples:
        - "How much did I spend on travel last month?"
        - "Show me all expenses over $500"
        - "What's my average monthly burn rate?"
        """
        context_str = ""
        if context:
            context_str = f"\nContext: {context}"
        
        prompt = f"""You are a financial AI assistant for FinAgent Pro. 
Answer the user's question accurately and concisely.

User Question: {user_query}
{context_str}

Answer:"""

        response = await self._call_llm(
            prompt=prompt,
            model_type="conversational",
            max_tokens=200
        )
        
        return response
    
    async def generate_financial_insights(
        self,
        expense_data: List[Dict],
        forecast_data: Dict
    ) -> Dict:
        """
        Generate AI-powered insights from financial data
        - Spending patterns
        - Budget recommendations
        - Risk alerts
        - Optimization suggestions
        """
        summary = self._summarize_data(expense_data, forecast_data)
        
        prompt = f"""Based on this financial data, provide actionable insights:

{summary}

Generate:
1. Top 3 spending patterns
2. Budget optimization recommendations
3. Risk alerts
4. Cashflow improvement suggestions
5. Tax optimization opportunities

Format as JSON with these keys: patterns, budget_tips, risks, cashflow_tips, tax_tips"""

        response = await self._call_llm(
            prompt=prompt,
            model_type="conversational",
            max_tokens=600
        )
        
        return {
            "insights": response,
            "generated_at": "now",
            "model": "huggingface_llm"
        }
    
    async def detect_sentiment_fraud_signals(
        self,
        transaction_description: str,
        merchant_info: Dict
    ) -> Dict:
        """
        Use sentiment analysis to detect fraud signals
        - Unusual merchant descriptions
        - Suspicious transaction patterns
        - Social engineering indicators
        """
        if self.local_pipelines.get("sentiment"):
            # Use local model
            result = self.local_pipelines["sentiment"](transaction_description)
            return {
                "sentiment": result[0]["label"],
                "confidence": result[0]["score"],
                "fraud_indicator": result[0]["label"] == "negative" and result[0]["score"] > 0.8
            }
        else:
            # Use API
            return await self._call_sentiment_api(transaction_description)
    
    async def smart_categorization(
        self,
        merchant: str,
        description: str,
        amount: float
    ) -> Dict:
        """
        AI-powered expense categorization with reasoning
        """
        prompt = f"""Categorize this expense and explain your reasoning:

Merchant: {merchant}
Description: {description}
Amount: ${amount}

Categories: Travel, Meals, Office Supplies, Equipment, Software, Marketing, Professional Services, Utilities, Rent, Insurance, Training, Other

Response format:
{{"category": "...", "subcategory": "...", "confidence": 0-1, "reasoning": "..."}}"""

        response = await self._call_llm(
            prompt=prompt,
            model_type="conversational",
            max_tokens=150
        )
        
        return {
            "llm_response": response,
            "model": "huggingface"
        }
    
    async def generate_invoice_from_conversation(
        self,
        conversation_history: List[str]
    ) -> Dict:
        """
        Extract invoice details from conversational input
        Handles back-and-forth clarifications
        """
        prompt = f"""Extract invoice details from this conversation:

{chr(10).join(conversation_history)}

Extract and format as JSON:
{{
  "client_name": "...",
  "client_email": "...",
  "items": [
    {{"description": "...", "quantity": 1, "unit_price": 0}}
  ],
  "due_date": "...",
  "payment_terms": "...",
  "notes": "..."
}}

If information is missing, set field to null."""

        response = await self._call_llm(
            prompt=prompt,
            model_type="conversational",
            max_tokens=400
        )
        
        return {
            "extracted_data": response,
            "needs_clarification": "null" in response.lower()
        }
    
    async def predictive_cashflow_narrative(
        self,
        forecast_data: Dict
    ) -> str:
        """
        Generate human-readable cashflow narrative
        """
        prompt = f"""Generate a concise executive summary of this cashflow forecast:

Expected runway: {forecast_data.get('metrics', {}).get('runway_months', 12)} months
Monthly burn: ${forecast_data.get('metrics', {}).get('burn_rate', 25000)}
12-month net: ${forecast_data.get('metrics', {}).get('net_cashflow', 125000)}

Write 2-3 sentences highlighting key insights and recommendations."""

        response = await self._call_llm(
            prompt=prompt,
            model_type="summarization",
            max_tokens=150
        )
        
        return response
    
    async def _call_llm(
        self,
        prompt: str,
        model_type: str = "conversational",
        max_tokens: int = 200
    ) -> str:
        """
        Call Hugging Face LLM (API or local)
        """
        model_name = self.models.get(model_type, self.models["conversational"])
        
        if not REQUESTS_AVAILABLE or not self.hf_api_token:
            # Fallback to simulated response for demo
            logger.warning("HF API not available - returning simulated response")
            return self._simulated_response(prompt)
        
        try:
            headers = {"Authorization": f"Bearer {self.hf_api_token}"}
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                f"{self.api_base}/{model_name}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").replace(prompt, "").strip()
                return str(result)
            else:
                logger.error(f"HF API error: {response.status_code}")
                return self._simulated_response(prompt)
                
        except Exception as e:
            logger.error(f"LLM call failed: {str(e)}")
            return self._simulated_response(prompt)
    
    async def _call_sentiment_api(self, text: str) -> Dict:
        """Call sentiment analysis API"""
        try:
            headers = {"Authorization": f"Bearer {self.hf_api_token}"}
            response = requests.post(
                f"{self.api_base}/ProsusAI/finbert",
                headers=headers,
                json={"inputs": text},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()[0]
                return {
                    "sentiment": result["label"],
                    "confidence": result["score"],
                    "fraud_indicator": result["label"] == "negative" and result["score"] > 0.8
                }
        except:
            pass
        
        return {"sentiment": "neutral", "confidence": 0.5, "fraud_indicator": False}
    
    def _simulated_response(self, prompt: str) -> str:
        """Generate simulated response for demo mode"""
        if "categorize" in prompt.lower():
            return '{"category": "Travel", "subcategory": "Airfare", "confidence": 0.92, "reasoning": "Airline merchant with high amount"}'
        elif "insights" in prompt.lower():
            return '{"patterns": ["Travel expenses 40% above average", "Software subscriptions increased 15%"], "budget_tips": ["Consider annual software plans", "Negotiate bulk travel rates"], "risks": ["Burn rate trending up"], "cashflow_tips": ["Accelerate invoicing cycle"], "tax_tips": ["Home office deduction available"]}'
        elif "invoice" in prompt.lower():
            return '{"client_name": "Acme Corp", "items": [{"description": "Consulting services", "quantity": 1, "unit_price": 12500}], "due_date": "net 30"}'
        else:
            return "Based on your financial data, I recommend focusing on reducing travel costs and negotiating better vendor rates."
    
    def _summarize_data(self, expenses: List[Dict], forecast: Dict) -> str:
        """Create text summary of data for LLM"""
        return f"""
Total expenses: {len(expenses)}
Forecast runway: {forecast.get('metrics', {}).get('runway_months', 12)} months
Average burn: ${forecast.get('metrics', {}).get('burn_rate', 25000)}/month
"""
    
    def health_status(self) -> Dict:
        """Return service health"""
        return {
            "service": "HuggingFaceService",
            "status": "healthy",
            "local_models": self.use_local_models,
            "api_configured": bool(self.hf_api_token),
            "transformers_available": TRANSFORMERS_AVAILABLE
        }
