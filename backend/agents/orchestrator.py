"""
Workflow Orchestrator Agent
Master coordinator for all agent interactions and workflows
"""

import os
from typing import Dict, Optional, List, Any
from datetime import datetime
from loguru import logger
import asyncio
import json


class WorkflowOrchestrator:
    """
    Master orchestration agent coordinating all specialist agents
    - Workflow routing and execution
    - Inter-agent communication
    - State management
    - Error handling and retry logic
    """
    
    def __init__(
        self,
        expense_classifier,
        invoice_agent,
        fraud_analyzer,
        cashflow_forecast
    ):
        self.name = "WorkflowOrchestrator"
        
        # Agent references
        self.expense_classifier = expense_classifier
        self.invoice_agent = invoice_agent
        self.fraud_analyzer = fraud_analyzer
        self.cashflow_forecast = cashflow_forecast
        
        # Workflow definitions
        self.workflows = {
            "expense_processing": self._expense_processing_workflow,
            "invoice_creation": self._invoice_creation_workflow,
            "fraud_detection": self._fraud_detection_workflow,
            "cashflow_forecast": self._cashflow_forecast_workflow
        }
        
        # Active workflows tracking
        self.active_workflows = {}
        
        # Background tasks
        self.background_tasks = []
        
        logger.info(f"✅ {self.name} initialized with {len(self.workflows)} workflows")
    
    async def execute_workflow(
        self,
        workflow_type: str,
        data: Dict,
        priority: str = "normal"
    ) -> Dict:
        """
        Execute a complete workflow
        
        Args:
            workflow_type: Type of workflow to execute
            data: Input data for workflow
            priority: Execution priority (low, normal, high, critical)
            
        Returns:
            Workflow execution result
        """
        try:
            workflow_id = self._generate_workflow_id()
            
            logger.info(f"🚀 Starting workflow: {workflow_type} [{workflow_id}]")
            
            # Record workflow start
            self.active_workflows[workflow_id] = {
                "workflow_type": workflow_type,
                "status": "running",
                "started_at": datetime.utcnow().isoformat(),
                "priority": priority
            }
            
            # Get workflow function
            workflow_func = self.workflows.get(workflow_type)
            if not workflow_func:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
            
            # Execute workflow
            result = await workflow_func(data, workflow_id)
            
            # Update workflow status
            self.active_workflows[workflow_id].update({
                "status": "completed",
                "completed_at": datetime.utcnow().isoformat(),
                "result": result
            })
            
            logger.info(f"✅ Workflow completed: {workflow_type} [{workflow_id}]")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Workflow failed: {workflow_type} - {str(e)}")
            
            # Update workflow status
            if workflow_id in self.active_workflows:
                self.active_workflows[workflow_id].update({
                    "status": "failed",
                    "error": str(e),
                    "failed_at": datetime.utcnow().isoformat()
                })
            
            raise
    
    async def _expense_processing_workflow(
        self,
        data: Dict,
        workflow_id: str
    ) -> Dict:
        """
        Complete expense processing pipeline
        1. OCR & Classification
        2. Fraud Detection
        3. Ledger Update
        4. Cashflow Forecast Update
        """
        logger.info(f"[{workflow_id}] Step 1: OCR & Classification")
        
        # Step 1: Process receipt with Expense Classifier
        file = data.get("file")
        user_id = data.get("user_id")
        
        # Read file content
        file_content = await file.read()
        
        expense_result = await self.expense_classifier.process_receipt(
            file_content=file_content,
            filename=data.get("filename"),
            user_id=user_id
        )
        
        logger.info(f"[{workflow_id}] Step 2: Fraud Detection")
        
        # Step 2: Fraud analysis if amount is significant
        fraud_result = None
        if expense_result.get("amount", 0) > 100:
            fraud_result = await self.fraud_analyzer.analyze_transaction(
                transaction_id=expense_result["expense_id"],
                user_id=user_id,
                amount=expense_result.get("amount"),
                merchant=expense_result.get("merchant"),
                category=expense_result.get("category")
            )
            
            expense_result["fraud_analysis"] = fraud_result
        
        # Step 3: Determine if manual review needed
        needs_review = (
            expense_result.get("classification_confidence", 1.0) < 0.9 or
            (fraud_result and fraud_result.get("risk_score", 0) >= 70)
        )
        
        if needs_review:
            expense_result["status"] = "pending_review"
            expense_result["review_reason"] = (
                "Low classification confidence" if expense_result.get("classification_confidence", 1.0) < 0.9
                else "High fraud risk detected"
            )
        else:
            expense_result["status"] = "approved"
            
            logger.info(f"[{workflow_id}] Step 3: Update Ledger")
            # In production: Update accounting ledger
            
            logger.info(f"[{workflow_id}] Step 4: Update Cashflow Forecast")
            # Trigger async forecast update
            asyncio.create_task(
                self.cashflow_forecast.incremental_update(
                    user_id=user_id,
                    new_data=expense_result
                )
            )
        
        return expense_result
    
    async def _invoice_creation_workflow(
        self,
        data: Dict,
        workflow_id: str
    ) -> Dict:
        """
        Invoice creation and delivery pipeline
        1. Extract invoice details
        2. Generate PDF
        3. Create payment link
        4. Send email
        5. Update CRM
        """
        logger.info(f"[{workflow_id}] Invoice creation workflow")
        
        input_data = data.get("input", {})
        user_id = data.get("user_id")
        
        # Create invoice
        invoice_result = await self.invoice_agent.create_invoice(
            user_input=input_data.get("description", ""),
            user_id=user_id,
            structured_data=input_data.get("structured_data")
        )
        
        # If invoice requires more information
        if invoice_result.get("status") == "incomplete":
            return invoice_result
        
        # Parallel execution of post-creation tasks
        logger.info(f"[{workflow_id}] Executing parallel tasks")
        
        tasks = []
        
        # Send email (if requested)
        if input_data.get("send_email", False):
            tasks.append(
                self.invoice_agent.send_invoice(invoice_result["invoice_id"])
            )
        
        # Update CRM (simulated)
        tasks.append(
            self._update_crm(invoice_result)
        )
        
        # Trigger webhook (simulated)
        if input_data.get("webhook_url"):
            tasks.append(
                self._trigger_webhook(input_data["webhook_url"], invoice_result)
            )
        
        # Execute all tasks in parallel
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        return invoice_result
    
    async def _fraud_detection_workflow(
        self,
        data: Dict,
        workflow_id: str
    ) -> Dict:
        """
        Real-time fraud detection workflow
        1. Analyze transaction
        2. Create alert if necessary
        3. Take automated actions
        4. Notify user
        """
        logger.info(f"[{workflow_id}] Fraud detection workflow")
        
        # Analyze transaction
        fraud_result = await self.fraud_analyzer.analyze_transaction(**data)
        
        # If high risk, take automated actions
        if fraud_result.get("risk_score", 0) >= 90:
            logger.warning(f"[{workflow_id}] Critical fraud detected - Taking action")
            
            # Block transaction (simulated)
            await self._block_transaction(fraud_result["transaction_id"])
            
            # Send immediate notifications
            await self._send_fraud_alert(
                user_id=data.get("user_id"),
                alert_details=fraud_result
            )
        
        return fraud_result
    
    async def _cashflow_forecast_workflow(
        self,
        data: Dict,
        workflow_id: str
    ) -> Dict:
        """
        Cashflow forecasting workflow
        1. Fetch historical data
        2. Generate forecast
        3. Create scenarios
        4. Update dashboard
        5. Send report (if scheduled)
        """
        logger.info(f"[{workflow_id}] Cashflow forecast workflow")
        
        user_id = data.get("user_id")
        
        # Generate forecast
        forecast_result = await self.cashflow_forecast.generate_forecast(user_id)
        
        # Update dashboard (simulated)
        await self._update_dashboard(user_id, forecast_result)
        
        # Send report if requested
        if data.get("send_report", False):
            await self._send_forecast_report(user_id, forecast_result)
        
        return forecast_result
    
    async def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get status of a workflow"""
        workflow = self.active_workflows.get(workflow_id)
        
        if not workflow:
            return {
                "workflow_id": workflow_id,
                "status": "not_found"
            }
        
        return {
            "workflow_id": workflow_id,
            **workflow
        }
    
    async def start_background_tasks(self):
        """Start recurring background tasks"""
        logger.info("Starting background tasks")
        
        # Daily cashflow forecast update
        self.background_tasks.append(
            asyncio.create_task(self._daily_forecast_task())
        )
        
        # Fraud monitoring task
        self.background_tasks.append(
            asyncio.create_task(self._fraud_monitoring_task())
        )
    
    async def stop_background_tasks(self):
        """Stop all background tasks"""
        logger.info("Stopping background tasks")
        
        for task in self.background_tasks:
            task.cancel()
        
        await asyncio.gather(*self.background_tasks, return_exceptions=True)
    
    async def _daily_forecast_task(self):
        """Daily cashflow forecast update (runs at 6 AM)"""
        while True:
            try:
                # In production, get list of active users
                # For demo, wait 24 hours between updates
                await asyncio.sleep(86400)  # 24 hours
                
                logger.info("Running daily cashflow forecast update")
                # Execute forecast update for all users
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Daily forecast task error: {str(e)}")
    
    async def _fraud_monitoring_task(self):
        """Continuous fraud monitoring"""
        while True:
            try:
                # In production, monitor transaction stream
                await asyncio.sleep(60)  # Check every minute
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Fraud monitoring task error: {str(e)}")
    
    # Helper methods
    
    async def _update_crm(self, invoice_data: Dict):
        """Update CRM system (simulated)"""
        await asyncio.sleep(0.5)
        logger.info(f"CRM updated with invoice {invoice_data['invoice_number']}")
    
    async def _trigger_webhook(self, url: str, data: Dict):
        """Trigger external webhook (simulated)"""
        await asyncio.sleep(0.3)
        logger.info(f"Webhook triggered: {url}")
    
    async def _block_transaction(self, transaction_id: str):
        """Block suspicious transaction (simulated)"""
        await asyncio.sleep(0.2)
        logger.warning(f"Transaction blocked: {transaction_id}")
    
    async def _send_fraud_alert(self, user_id: str, alert_details: Dict):
        """Send fraud alert via multiple channels (simulated)"""
        await asyncio.sleep(0.3)
        logger.warning(f"Fraud alert sent to user {user_id}")
    
    async def _update_dashboard(self, user_id: str, forecast_data: Dict):
        """Update dashboard with latest forecast (simulated)"""
        await asyncio.sleep(0.2)
        logger.info(f"Dashboard updated for user {user_id}")
    
    async def _send_forecast_report(self, user_id: str, forecast_data: Dict):
        """Send forecast report via email (simulated)"""
        await asyncio.sleep(0.4)
        logger.info(f"Forecast report sent to user {user_id}")
    
    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID"""
        from uuid import uuid4
        return f"wf_{uuid4().hex[:12]}"
    
    def health_status(self) -> Dict:
        """Return orchestrator health status"""
        return {
            "agent": self.name,
            "status": "healthy",
            "workflows": list(self.workflows.keys()),
            "active_workflows": len(self.active_workflows),
            "background_tasks": len(self.background_tasks),
            "capabilities": [
                "Workflow Routing",
                "Inter-agent Communication",
                "State Management",
                "Error Handling",
                "Background Processing"
            ]
        }
