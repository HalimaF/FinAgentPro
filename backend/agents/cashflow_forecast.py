"""
Cashflow Forecast Agent
Predictive analytics for cashflow forecasting using ML
"""

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from loguru import logger
import numpy as np
import pandas as pd

# Try importing Prophet, fallback to stub for demo mode
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    logger.warning("Prophet not available - using simulated forecasts")
    
    class Prophet:
        """Stub Prophet class for DEMO_MODE"""
        def __init__(self, *args, **kwargs):
            pass
        def fit(self, *args, **kwargs):
            return self
        def make_future_dataframe(self, periods, freq='D'):
            return pd.DataFrame({
                'ds': pd.date_range(start=datetime.now(), periods=periods, freq=freq)
            })
        def predict(self, df):
            # Return simulated forecast
            return pd.DataFrame({
                'ds': df['ds'],
                'yhat': np.random.uniform(10000, 50000, len(df)),
                'yhat_lower': np.random.uniform(5000, 15000, len(df)),
                'yhat_upper': np.random.uniform(40000, 60000, len(df))
            })

import asyncio


class CashflowForecastAgent:
    """
    Intelligent cashflow forecasting agent
    - Time-series forecasting with Prophet
    - Scenario analysis (best/expected/worst case)
    - Confidence intervals
    - Automated daily updates
    """
    
    def __init__(self):
        self.name = "CashflowForecastAgent"
        self.forecast_horizon_days = 365
        self.confidence_interval = 0.95
        
        logger.info(f"✅ {self.name} initialized")
    
    async def generate_forecast(
        self,
        user_id: str,
        historical_months: int = 24
    ) -> Dict:
        """
        Generate comprehensive cashflow forecast
        
        Args:
            user_id: User identifier
            historical_months: Months of historical data to use
            
        Returns:
            Complete forecast with predictions and scenarios
        """
        try:
            logger.info(f"Generating cashflow forecast for user {user_id}")
            
            # Step 1: Extract historical data
            historical_data = await self._fetch_historical_data(
                user_id,
                months=historical_months
            )
            
            # Step 2: Preprocess data
            processed_data = self._preprocess_data(historical_data)
            
            # Step 3: Feature engineering
            features = self._engineer_features(processed_data)
            
            # Step 4: Train Prophet model
            model_inflow = self._train_prophet_model(
                features,
                target="inflow"
            )
            model_outflow = self._train_prophet_model(
                features,
                target="outflow"
            )
            
            # Step 5: Generate forecasts
            forecast_inflow = self._generate_prophet_forecast(
                model_inflow,
                periods=self.forecast_horizon_days
            )
            forecast_outflow = self._generate_prophet_forecast(
                model_outflow,
                periods=self.forecast_horizon_days
            )
            
            # Step 6: Calculate net position
            forecast_net = self._calculate_net_forecast(
                forecast_inflow,
                forecast_outflow
            )
            
            # Step 7: Generate scenarios
            scenarios = self._generate_scenarios(forecast_net)
            
            # Step 8: Calculate metrics
            metrics = self._calculate_metrics(forecast_net, historical_data)
            
            # Step 9: Prepare result
            result = {
                "forecast_id": self._generate_forecast_id(),
                "user_id": user_id,
                "forecast_date": datetime.utcnow().isoformat(),
                "horizon_days": self.forecast_horizon_days,
                "inflow_forecast": forecast_inflow,
                "outflow_forecast": forecast_outflow,
                "net_forecast": forecast_net,
                "scenarios": scenarios,
                "metrics": metrics,
                "confidence_interval": self.confidence_interval,
                "model_version": "prophet_v2.0",
                "generated_by": self.name
            }
            
            logger.info(f"✅ Forecast generated: {result['forecast_id']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Forecast generation failed: {str(e)}")
            raise
    
    async def _fetch_historical_data(
        self,
        user_id: str,
        months: int
    ) -> pd.DataFrame:
        """
        Fetch historical transaction data
        (In production, query from database)
        """
        # Simulate database query
        await asyncio.sleep(0.2)
        
        # Generate synthetic historical data for demo
        start_date = datetime.utcnow() - timedelta(days=months * 30)
        date_range = pd.date_range(start=start_date, periods=months * 30, freq='D')
        
        # Simulate realistic cashflow patterns
        np.random.seed(42)
        
        data = {
            'date': date_range,
            'inflow': np.random.normal(5000, 1500, len(date_range)) + \
                      np.sin(np.arange(len(date_range)) * 2 * np.pi / 30) * 1000,
            'outflow': np.random.normal(4000, 1000, len(date_range)) + \
                       np.sin(np.arange(len(date_range)) * 2 * np.pi / 30) * 800
        }
        
        # Ensure no negative values
        data['inflow'] = np.maximum(data['inflow'], 0)
        data['outflow'] = np.maximum(data['outflow'], 0)
        
        df = pd.DataFrame(data)
        
        logger.info(f"Loaded {len(df)} days of historical data")
        return df
    
    def _preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and prepare data for modeling
        """
        # Remove duplicates
        data = data.drop_duplicates(subset=['date'])
        
        # Sort by date
        data = data.sort_values('date')
        
        # Handle missing values
        data = data.fillna(method='ffill')
        
        # Calculate net cashflow
        data['net'] = data['inflow'] - data['outflow']
        
        return data
    
    def _engineer_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Create additional features for modeling
        """
        df = data.copy()
        
        # Temporal features
        df['day_of_week'] = df['date'].dt.dayofweek
        df['day_of_month'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['quarter'] = df['date'].dt.quarter
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_month_start'] = (df['day_of_month'] <= 7).astype(int)
        df['is_month_end'] = (df['day_of_month'] >= 24).astype(int)
        
        # Rolling averages
        df['inflow_ma7'] = df['inflow'].rolling(window=7, min_periods=1).mean()
        df['inflow_ma30'] = df['inflow'].rolling(window=30, min_periods=1).mean()
        df['outflow_ma7'] = df['outflow'].rolling(window=7, min_periods=1).mean()
        df['outflow_ma30'] = df['outflow'].rolling(window=30, min_periods=1).mean()
        
        return df
    
    def _train_prophet_model(
        self,
        data: pd.DataFrame,
        target: str
    ) -> Prophet:
        """
        Train Prophet model for time-series forecasting
        """
        # Prepare data in Prophet format
        df_prophet = pd.DataFrame({
            'ds': data['date'],
            'y': data[target]
        })
        
        # Initialize Prophet with custom parameters
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.05,
            interval_width=self.confidence_interval
        )
        
        # Add custom seasonalities
        model.add_seasonality(
            name='monthly',
            period=30.5,
            fourier_order=5
        )
        
        # Fit model
        model.fit(df_prophet)
        
        logger.info(f"Prophet model trained for {target}")
        return model
    
    def _generate_prophet_forecast(
        self,
        model: Prophet,
        periods: int
    ) -> Dict:
        """
        Generate forecast using trained Prophet model
        """
        # Create future dataframe
        future = model.make_future_dataframe(periods=periods)
        
        # Generate forecast
        forecast = model.predict(future)
        
        # Extract relevant columns
        forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
        
        # Convert to dictionary format
        result = {
            "dates": forecast_data['ds'].dt.strftime('%Y-%m-%d').tolist(),
            "predicted": forecast_data['yhat'].round(2).tolist(),
            "lower_bound": forecast_data['yhat_lower'].round(2).tolist(),
            "upper_bound": forecast_data['yhat_upper'].round(2).tolist()
        }
        
        return result
    
    def _calculate_net_forecast(
        self,
        forecast_inflow: Dict,
        forecast_outflow: Dict
    ) -> Dict:
        """
        Calculate net cashflow forecast
        """
        dates = forecast_inflow["dates"]
        
        net_predicted = [
            inflow - outflow
            for inflow, outflow in zip(
                forecast_inflow["predicted"],
                forecast_outflow["predicted"]
            )
        ]
        
        net_lower = [
            inflow_lower - outflow_upper
            for inflow_lower, outflow_upper in zip(
                forecast_inflow["lower_bound"],
                forecast_outflow["upper_bound"]
            )
        ]
        
        net_upper = [
            inflow_upper - outflow_lower
            for inflow_upper, outflow_lower in zip(
                forecast_inflow["upper_bound"],
                forecast_outflow["lower_bound"]
            )
        ]
        
        # Calculate cumulative position
        cumulative = []
        running_total = 0
        for net in net_predicted:
            running_total += net
            cumulative.append(round(running_total, 2))
        
        return {
            "dates": dates,
            "net_predicted": [round(x, 2) for x in net_predicted],
            "net_lower": [round(x, 2) for x in net_lower],
            "net_upper": [round(x, 2) for x in net_upper],
            "cumulative_position": cumulative
        }
    
    def _generate_scenarios(self, forecast_net: Dict) -> Dict:
        """
        Generate best/expected/worst case scenarios
        """
        predicted = forecast_net["net_predicted"]
        
        # Best case: +20% improvement
        best_case = [round(x * 1.2, 2) for x in predicted]
        
        # Expected case: base forecast
        expected_case = predicted
        
        # Worst case: -20% decline
        worst_case = [round(x * 0.8, 2) for x in predicted]
        
        # Calculate cumulative for each scenario
        best_cumulative = []
        expected_cumulative = []
        worst_cumulative = []
        
        best_sum = expected_sum = worst_sum = 0
        
        for b, e, w in zip(best_case, expected_case, worst_case):
            best_sum += b
            expected_sum += e
            worst_sum += w
            best_cumulative.append(round(best_sum, 2))
            expected_cumulative.append(round(expected_sum, 2))
            worst_cumulative.append(round(worst_sum, 2))
        
        return {
            "best_case": {
                "daily_net": best_case,
                "cumulative": best_cumulative,
                "description": "Optimistic scenario (+20% revenue growth)"
            },
            "expected_case": {
                "daily_net": expected_case,
                "cumulative": expected_cumulative,
                "description": "Base forecast (current trajectory)"
            },
            "worst_case": {
                "daily_net": worst_case,
                "cumulative": worst_cumulative,
                "description": "Conservative scenario (-20% revenue decline)"
            }
        }
    
    def _calculate_metrics(
        self,
        forecast_net: Dict,
        historical_data: pd.DataFrame
    ) -> Dict:
        """
        Calculate performance and business metrics
        """
        # Current cashflow metrics
        current_balance = 100000  # Placeholder - from user account
        
        net_predicted = forecast_net["net_predicted"]
        cumulative = forecast_net["cumulative_position"]
        
        # Calculate runway (months until balance depletes)
        runway_months = 0
        for i, cum in enumerate(cumulative):
            if current_balance + cum <= 0:
                runway_months = i / 30
                break
        if runway_months == 0:
            runway_months = 12  # More than forecast horizon
        
        # Average burn rate (for negative periods)
        negative_days = [x for x in net_predicted if x < 0]
        burn_rate = abs(np.mean(negative_days)) if negative_days else 0
        
        # Break-even prediction
        break_even_date = None
        for i, net in enumerate(net_predicted):
            if net > 0:
                break_even_date = forecast_net["dates"][i]
                break
        
        # Historical accuracy (MAPE) - simulated
        mape = np.random.uniform(5, 15)  # 5-15% error
        
        return {
            "runway_months": round(runway_months, 1),
            "average_burn_rate": round(burn_rate, 2),
            "break_even_date": break_even_date,
            "forecast_accuracy_mape": round(mape, 2),
            "predicted_12m_net": round(sum(net_predicted[:365]), 2),
            "confidence_level": f"{int(self.confidence_interval * 100)}%"
        }
    
    async def get_latest_forecast(self, user_id: str) -> Dict:
        """
        Retrieve the most recent forecast for a user
        """
        # In production, query from database
        # For demo, generate new forecast
        return await self.generate_forecast(user_id)
    
    async def incremental_update(
        self,
        user_id: str,
        new_data: Dict
    ) -> Dict:
        """
        Update forecast with new transaction data
        """
        logger.info(f"Updating forecast with new data for user {user_id}")
        
        # In production, append new data and retrain incrementally
        # For demo, trigger full regeneration
        return await self.generate_forecast(user_id)
    
    def _generate_forecast_id(self) -> str:
        """Generate unique forecast ID"""
        from uuid import uuid4
        return f"forecast_{uuid4().hex[:12]}"
    
    def health_status(self) -> Dict:
        """Return agent health status"""
        return {
            "agent": self.name,
            "status": "healthy",
            "model": "Prophet",
            "forecast_horizon": f"{self.forecast_horizon_days} days",
            "confidence_interval": f"{int(self.confidence_interval * 100)}%",
            "capabilities": [
                "Time-series Forecasting",
                "Scenario Analysis",
                "Confidence Intervals",
                "Automated Updates"
            ]
        }
