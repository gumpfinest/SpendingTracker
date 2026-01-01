"""
Spending forecast endpoint.
Uses linear regression to predict future spending patterns.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


router = APIRouter()


class Transaction(BaseModel):
    """Transaction model for forecast input."""
    id: int
    description: str
    amount: float
    type: str  # INCOME or EXPENSE
    category: Optional[str] = None
    date: str  # ISO format date string


class ForecastRequest(BaseModel):
    """Request model for forecast."""
    user_id: int
    transactions: List[Transaction]
    forecast_months: int = 6


class MonthlyForecast(BaseModel):
    """Monthly forecast data."""
    month: str
    predicted_spending: float
    predicted_income: float
    predicted_savings: float
    confidence_lower: float
    confidence_upper: float


class ForecastResponse(BaseModel):
    """Response model for forecast."""
    user_id: int
    forecasts: List[MonthlyForecast]
    average_monthly_spending: float
    average_monthly_income: float
    spending_trend: str  # "increasing", "decreasing", "stable"
    savings_rate: float
    advice: str


def calculate_forecast(transactions: List[Transaction], months: int = 6) -> dict:
    """
    Calculate spending forecast using linear regression.
    
    Args:
        transactions: List of historical transactions
        months: Number of months to forecast
        
    Returns:
        Dictionary containing forecast data
    """
    if not transactions:
        return {
            "forecasts": [],
            "average_monthly_spending": 0,
            "average_monthly_income": 0,
            "spending_trend": "stable",
            "savings_rate": 0,
            "advice": "Add some transactions to get personalized forecasts."
        }
    
    # Convert to DataFrame
    data = []
    for t in transactions:
        try:
            date = datetime.fromisoformat(t.date.replace('Z', '+00:00'))
        except:
            date = datetime.now()
        
        data.append({
            "date": date,
            "amount": float(t.amount),
            "type": t.type,
            "category": t.category or "Uncategorized"
        })
    
    df = pd.DataFrame(data)
    df['month'] = df['date'].dt.to_period('M')
    
    # Aggregate by month
    monthly_spending = df[df['type'] == 'EXPENSE'].groupby('month')['amount'].sum()
    monthly_income = df[df['type'] == 'INCOME'].groupby('month')['amount'].sum()
    
    # Ensure we have enough data
    if len(monthly_spending) < 2:
        avg_spending = monthly_spending.mean() if len(monthly_spending) > 0 else 0
        avg_income = monthly_income.mean() if len(monthly_income) > 0 else 0
        
        forecasts = []
        current_date = datetime.now()
        for i in range(months):
            future_date = current_date + timedelta(days=30 * (i + 1))
            forecasts.append({
                "month": future_date.strftime("%Y-%m"),
                "predicted_spending": float(avg_spending),
                "predicted_income": float(avg_income),
                "predicted_savings": float(avg_income - avg_spending),
                "confidence_lower": float(avg_spending * 0.8),
                "confidence_upper": float(avg_spending * 1.2)
            })
        
        return {
            "forecasts": forecasts,
            "average_monthly_spending": float(avg_spending),
            "average_monthly_income": float(avg_income),
            "spending_trend": "stable",
            "savings_rate": float((avg_income - avg_spending) / avg_income * 100) if avg_income > 0 else 0,
            "advice": "Keep tracking your expenses to get more accurate forecasts."
        }
    
    # Prepare data for regression
    X = np.array(range(len(monthly_spending))).reshape(-1, 1)
    y_spending = monthly_spending.values
    
    # Fit linear regression for spending
    model_spending = LinearRegression()
    model_spending.fit(X, y_spending)
    
    # Calculate trend
    slope = model_spending.coef_[0]
    if slope > 50:
        trend = "increasing"
    elif slope < -50:
        trend = "decreasing"
    else:
        trend = "stable"
    
    # Generate forecasts
    forecasts = []
    current_date = datetime.now()
    
    for i in range(months):
        future_X = np.array([[len(monthly_spending) + i]])
        predicted_spending = max(0, model_spending.predict(future_X)[0])
        
        # Use average income for prediction (income is usually more stable)
        avg_income = monthly_income.mean() if len(monthly_income) > 0 else 0
        
        future_date = current_date + timedelta(days=30 * (i + 1))
        
        # Calculate confidence interval (simple approach)
        std_dev = monthly_spending.std() if len(monthly_spending) > 1 else predicted_spending * 0.1
        
        forecasts.append({
            "month": future_date.strftime("%Y-%m"),
            "predicted_spending": round(float(predicted_spending), 2),
            "predicted_income": round(float(avg_income), 2),
            "predicted_savings": round(float(avg_income - predicted_spending), 2),
            "confidence_lower": round(float(max(0, predicted_spending - 1.96 * std_dev)), 2),
            "confidence_upper": round(float(predicted_spending + 1.96 * std_dev), 2)
        })
    
    avg_spending = float(monthly_spending.mean())
    avg_income = float(monthly_income.mean()) if len(monthly_income) > 0 else 0
    savings_rate = ((avg_income - avg_spending) / avg_income * 100) if avg_income > 0 else 0
    
    # Generate advice based on analysis
    if savings_rate < 10:
        advice = "Your savings rate is low. Consider cutting back on discretionary spending to build your emergency fund."
    elif savings_rate < 20:
        advice = "You're saving a decent amount. Try to increase it to 20% for better financial security."
    elif trend == "increasing":
        advice = "Your spending is trending upward. Review your recent expenses to identify areas to cut back."
    elif trend == "decreasing":
        advice = "Great job! Your spending is decreasing. Keep up the good financial habits."
    else:
        advice = "Your finances look stable. Consider investing your extra savings for long-term growth."
    
    return {
        "forecasts": forecasts,
        "average_monthly_spending": round(avg_spending, 2),
        "average_monthly_income": round(avg_income, 2),
        "spending_trend": trend,
        "savings_rate": round(savings_rate, 2),
        "advice": advice
    }


@router.post("/forecast", response_model=ForecastResponse)
async def get_forecast(request: ForecastRequest):
    """
    Generate spending forecast for the next N months.
    
    Uses historical transaction data to predict future spending
    patterns using linear regression.
    """
    result = calculate_forecast(request.transactions, request.forecast_months)
    
    return ForecastResponse(
        user_id=request.user_id,
        forecasts=[MonthlyForecast(**f) for f in result["forecasts"]],
        average_monthly_spending=result["average_monthly_spending"],
        average_monthly_income=result["average_monthly_income"],
        spending_trend=result["spending_trend"],
        savings_rate=result["savings_rate"],
        advice=result["advice"]
    )
