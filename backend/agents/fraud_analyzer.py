"""
Fraud Analyzer Agent
Real-time fraud detection using ML and rule-based systems
"""

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger
import numpy as np
from sklearn.ensemble import IsolationForest
import asyncio


class FraudAnalyzerAgent:
    """
    Intelligent fraud detection agent
    - Real-time anomaly detection
    - ML-based risk scoring
    - Rule engine for known fraud patterns
    - Multi-factor analysis
    """
    
    def __init__(self):
        self.name = "FraudAnalyzerAgent"
        
        # Initialize ML model
        self.isolation_forest = IsolationForest(
            contamination=0.05,
            random_state=42,
            n_estimators=100
        )
        
        # Fraud detection thresholds
        self.thresholds = {
            "critical": 90,
            "high": 80,
            "medium": 70,
            "low": 60
        }
        
        # Rule weights
        self.rule_weights = {
            "large_amount": 0.30,
            "rapid_transactions": 0.25,
            "new_merchant": 0.20,
            "location_anomaly": 0.15,
            "off_hours": 0.10
        }
        
        logger.info(f"✅ {self.name} initialized")
    
    async def analyze_transaction(
        self,
        transaction_id: str,
        user_id: str,
        amount: float = None,
        merchant: str = None,
        category: str = None,
        timestamp: datetime = None,
        location: Dict = None
    ) -> Dict:
        """
        Comprehensive fraud analysis of a transaction
        
        Args:
            transaction_id: Transaction identifier
            user_id: User identifier
            amount: Transaction amount
            merchant: Merchant name
            category: Expense category
            timestamp: Transaction timestamp
            location: Location data
            
        Returns:
            Fraud analysis result with risk score and recommended actions
        """
        try:
            logger.info(f"Analyzing transaction {transaction_id}")
            
            # Step 1: Load user profile and historical data
            user_profile = await self._load_user_profile(user_id)
            
            # Step 2: Extract features
            features = self._extract_features(
                amount=amount,
                merchant=merchant,
                category=category,
                timestamp=timestamp or datetime.utcnow(),
                location=location,
                user_profile=user_profile
            )
            
            # Step 3: Run ML model
            ml_score = self._ml_anomaly_detection(features, user_profile)
            
            # Step 4: Apply rule engine
            rule_score = self._apply_fraud_rules(features, user_profile)
            
            # Step 5: Calculate composite risk score
            composite_score = self._calculate_composite_score(ml_score, rule_score)
            
            # Step 6: Determine severity and actions
            severity, actions = self._determine_response(composite_score)
            
            # Step 7: Generate explanation
            explanation = self._generate_explanation(features, rule_score, severity)
            
            # Step 8: Prepare result
            result = {
                "transaction_id": transaction_id,
                "analysis_id": self._generate_analysis_id(),
                "risk_score": round(composite_score, 2),
                "severity": severity,
                "alert_type": self._classify_alert_type(features),
                "confidence": 0.85,  # Model confidence
                "ml_score": round(ml_score, 2),
                "rule_score": round(rule_score, 2),
                "contributing_factors": [
                    factor for factor, score in features.items()
                    if score > 0.5
                ],
                "explanation": explanation,
                "recommended_actions": actions,
                "requires_review": composite_score >= self.thresholds["medium"],
                "auto_block": composite_score >= self.thresholds["critical"],
                "analyzed_at": datetime.utcnow().isoformat(),
                "analyzed_by": self.name
            }
            
            # Create alert if necessary
            if composite_score >= self.thresholds["medium"]:
                alert_id = await self._create_fraud_alert(result)
                result["alert_id"] = alert_id
                logger.warning(f"🚨 Fraud alert created: {alert_id} - Score: {composite_score}")
            else:
                logger.info(f"✅ Transaction passed fraud check - Score: {composite_score}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Fraud analysis failed: {str(e)}")
            raise
    
    async def _load_user_profile(self, user_id: str) -> Dict:
        """
        Load user's historical transaction profile
        (In production, query from database)
        """
        # Simulate loading user profile
        await asyncio.sleep(0.1)  # Simulate DB query
        
        return {
            "user_id": user_id,
            "avg_transaction": 250.0,
            "std_transaction": 150.0,
            "frequent_merchants": [
                "Amazon", "Office Depot", "Starbucks", "Shell Gas"
            ],
            "typical_categories": [
                "Office Supplies", "Meals & Entertainment", "Travel"
            ],
            "transaction_count_30d": 45,
            "average_daily_transactions": 1.5,
            "typical_transaction_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17],
            "known_locations": [
                {"city": "San Francisco", "state": "CA"},
                {"city": "New York", "state": "NY"}
            ],
            "account_age_days": 365,
            "previous_fraud_incidents": 0
        }
    
    def _extract_features(
        self,
        amount: float,
        merchant: str,
        category: str,
        timestamp: datetime,
        location: Dict,
        user_profile: Dict
    ) -> Dict:
        """
        Extract fraud detection features
        """
        features = {}
        
        # Amount-based features
        avg = user_profile["avg_transaction"]
        std = user_profile["std_transaction"]
        
        if amount and avg and std:
            z_score = abs((amount - avg) / std) if std > 0 else 0
            features["amount_zscore"] = min(z_score / 3, 1.0)  # Normalize to 0-1
            features["large_amount"] = 1.0 if amount > avg + (3 * std) else 0.0
        else:
            features["amount_zscore"] = 0.0
            features["large_amount"] = 0.0
        
        # Merchant novelty
        if merchant:
            is_known = merchant in user_profile.get("frequent_merchants", [])
            features["merchant_novelty"] = 0.0 if is_known else 1.0
        else:
            features["merchant_novelty"] = 0.5
        
        # Category match
        if category:
            is_typical = category in user_profile.get("typical_categories", [])
            features["category_mismatch"] = 0.0 if is_typical else 0.6
        else:
            features["category_mismatch"] = 0.3
        
        # Temporal features
        hour = timestamp.hour
        is_business_hours = hour in user_profile.get("typical_transaction_hours", range(9, 18))
        features["off_hours"] = 0.0 if is_business_hours else 0.8
        
        # Transaction velocity (simulated)
        # In production, query recent transactions
        features["velocity_1h"] = 0.2  # Placeholder
        features["velocity_24h"] = 0.1  # Placeholder
        
        # Location anomaly (simulated)
        features["location_distance"] = 0.1  # Placeholder
        
        return features
    
    def _ml_anomaly_detection(
        self,
        features: Dict,
        user_profile: Dict
    ) -> float:
        """
        Use Isolation Forest for anomaly detection
        """
        try:
            # Prepare feature vector
            feature_vector = np.array([[
                features.get("amount_zscore", 0),
                features.get("merchant_novelty", 0),
                features.get("category_mismatch", 0),
                features.get("off_hours", 0),
                features.get("velocity_1h", 0),
                features.get("velocity_24h", 0)
            ]])
            
            # In production, use pre-trained model
            # For demo, simulate score
            ml_score = np.random.uniform(20, 80)
            
            # Higher score = more anomalous
            return ml_score
            
        except Exception as e:
            logger.error(f"ML detection failed: {str(e)}")
            return 50.0  # Return neutral score on error
    
    def _apply_fraud_rules(
        self,
        features: Dict,
        user_profile: Dict
    ) -> float:
        """
        Apply rule-based fraud detection
        """
        rule_scores = []
        
        # Rule 1: Large Amount
        if features.get("large_amount", 0) > 0:
            rule_scores.append(("large_amount", 40))
        
        # Rule 2: Rapid Transactions
        if features.get("velocity_1h", 0) > 0.5:
            rule_scores.append(("rapid_transactions", 35))
        
        # Rule 3: New Merchant
        if features.get("merchant_novelty", 0) > 0.8:
            rule_scores.append(("new_merchant", 25))
        
        # Rule 4: Off-Hours Transaction
        if features.get("off_hours", 0) > 0.5:
            rule_scores.append(("off_hours", 15))
        
        # Rule 5: Location Anomaly
        if features.get("location_distance", 0) > 0.7:
            rule_scores.append(("location_anomaly", 30))
        
        # Calculate weighted score
        if rule_scores:
            total_score = sum(score for _, score in rule_scores)
            weighted_score = min(total_score, 100)
        else:
            weighted_score = 0
        
        return weighted_score
    
    def _calculate_composite_score(
        self,
        ml_score: float,
        rule_score: float
    ) -> float:
        """
        Combine ML and rule-based scores
        """
        # Weighted combination: 60% ML, 40% Rules
        composite = (ml_score * 0.6) + (rule_score * 0.4)
        return min(composite, 100)
    
    def _determine_response(self, risk_score: float) -> tuple:
        """
        Determine severity and recommended actions
        """
        if risk_score >= self.thresholds["critical"]:
            severity = "critical"
            actions = [
                "Block transaction immediately",
                "Require multi-factor authentication",
                "Notify security team",
                "Send SMS alert to user"
            ]
        elif risk_score >= self.thresholds["high"]:
            severity = "high"
            actions = [
                "Hold transaction for review",
                "Require 2FA verification",
                "Send email alert"
            ]
        elif risk_score >= self.thresholds["medium"]:
            severity = "medium"
            actions = [
                "Flag for manual review",
                "Send notification to user",
                "Monitor subsequent transactions"
            ]
        elif risk_score >= self.thresholds["low"]:
            severity = "low"
            actions = [
                "Log for analysis",
                "Continue monitoring"
            ]
        else:
            severity = "none"
            actions = ["Approve transaction"]
        
        return severity, actions
    
    def _classify_alert_type(self, features: Dict) -> str:
        """
        Classify the type of fraud alert
        """
        # Find highest scoring feature
        if features.get("large_amount", 0) > 0.7:
            return "unusual_amount"
        elif features.get("merchant_novelty", 0) > 0.7:
            return "suspicious_merchant"
        elif features.get("velocity_1h", 0) > 0.7:
            return "rapid_transactions"
        elif features.get("location_distance", 0) > 0.7:
            return "location_anomaly"
        elif features.get("category_mismatch", 0) > 0.7:
            return "category_mismatch"
        else:
            return "general_anomaly"
    
    def _generate_explanation(
        self,
        features: Dict,
        rule_score: float,
        severity: str
    ) -> str:
        """
        Generate human-readable explanation
        """
        explanations = []
        
        if features.get("large_amount", 0) > 0.5:
            explanations.append("Transaction amount significantly exceeds your typical spending")
        
        if features.get("merchant_novelty", 0) > 0.7:
            explanations.append("First-time transaction with this merchant")
        
        if features.get("off_hours", 0) > 0.5:
            explanations.append("Transaction occurred outside your normal hours")
        
        if features.get("velocity_1h", 0) > 0.5:
            explanations.append("Multiple transactions in short time period")
        
        if not explanations:
            return "Transaction pattern matches your normal behavior"
        
        return ". ".join(explanations) + "."
    
    async def _create_fraud_alert(self, analysis_result: Dict) -> str:
        """
        Create fraud alert record in database
        """
        alert_id = f"alert_{self._generate_analysis_id()}"
        
        # In production, insert into database
        logger.info(f"Creating fraud alert: {alert_id}")
        
        return alert_id
    
    def _generate_analysis_id(self) -> str:
        """Generate unique analysis ID"""
        from uuid import uuid4
        return uuid4().hex[:12]
    
    async def batch_analyze(
        self,
        transactions: List[Dict]
    ) -> List[Dict]:
        """
        Analyze multiple transactions in parallel
        """
        tasks = [
            self.analyze_transaction(**txn)
            for txn in transactions
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful = [r for r in results if not isinstance(r, Exception)]
        return successful
    
    def health_status(self) -> Dict:
        """Return agent health status"""
        return {
            "agent": self.name,
            "status": "healthy",
            "model": "IsolationForest",
            "thresholds": self.thresholds,
            "capabilities": [
                "Real-time Detection",
                "ML Anomaly Detection",
                "Rule-based Analysis",
                "Multi-factor Scoring"
            ]
        }
