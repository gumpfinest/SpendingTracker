"""
Spending forecast endpoint.
Uses linear regression to predict future spending patterns.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

from app.core.models import Transaction
from app.core.utils import transactions_to_dataframe, round_currency, calculate_percentage


router = APIRouter()


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


def _get_empty_forecast(months: int) -> dict:
    """Return empty forecast result."""
    return {
        "forecasts": [],
        "average_monthly_spending": 0,
        "average_monthly_income": 0,
        "spending_trend": "stable",
        "savings_rate": 0,
        "advice": "Add some transactions to get personalized forecasts."
    }


def _generate_simple_forecast(monthly_spending, monthly_income, months: int) -> dict:
    """Generate simple forecast when insufficient data for regression."""
    avg_spending = monthly_spending.mean() if len(monthly_spending) > 0 else 0
    avg_income = monthly_income.mean() if len(monthly_income) > 0 else 0
    
    forecasts = []
    current_date = datetime.now()
    for i in range(months):
        future_date = current_date + timedelta(days=30 * (i + 1))
        forecasts.append({
            "month": future_date.strftime("%Y-%m"),
            "predicted_spending": round_currency(avg_spending),
            "predicted_income": round_currency(avg_income),
            "predicted_savings": round_currency(avg_income - avg_spending),
            "confidence_lower": round_currency(avg_spending * 0.8),
            "confidence_upper": round_currency(avg_spending * 1.2)
        })
    
    return {
        "forecasts": forecasts,
        "average_monthly_spending": round_currency(avg_spending),
        "average_monthly_income": round_currency(avg_income),
        "spending_trend": "stable",
        "savings_rate": calculate_percentage(avg_income - avg_spending, avg_income) if avg_income > 0 else 0,
        "advice": "Keep tracking your expenses to get more accurate forecasts."
    }


def _determine_trend(slope: float) -> str:
    """Determine spending trend based on regression slope."""
    if slope > 50:
        return "increasing"
    elif slope < -50:
        return "decreasing"
    return "stable"


def _generate_advice(savings_rate: float, trend: str) -> str:
    """Generate financial advice based on analysis."""
    if savings_rate < 10:
        return "Your savings rate is low. Consider cutting back on discretionary spending to build your emergency fund."
    elif savings_rate < 20:
        return "You're saving a decent amount. Try to increase it to 20% for better financial security."
    elif trend == "increasing":
        return "Your spending is trending upward. Review your recent expenses to identify areas to cut back."
    elif trend == "decreasing":
        return "Great job! Your spending is decreasing. Keep up the good financial habits."
    return "Your finances look stable. Consider investing your extra savings for long-term growth."


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
        return _get_empty_forecast(months)
    
    df = transactions_to_dataframe(transactions)
    
    # Aggregate by month
    monthly_spending = df[df['type'] == 'EXPENSE'].groupby('month')['amount'].sum()
    monthly_income = df[df['type'] == 'INCOME'].groupby('month')['amount'].sum()
    
    # Need at least 2 data points for regression
    if len(monthly_spending) < 2:
        return _generate_simple_forecast(monthly_spending, monthly_income, months)
    
    # Fit linear regression for spending
    X = np.array(range(len(monthly_spending))).reshape(-1, 1)
    y_spending = monthly_spending.values
    
    model = LinearRegression()
    model.fit(X, y_spending)
    
    trend = _determine_trend(model.coef_[0])
    avg_income = float(monthly_income.mean()) if len(monthly_income) > 0 else 0
    std_dev = monthly_spending.std() if len(monthly_spending) > 1 else 0
    
    # Generate forecasts
    forecasts = []
    current_date = datetime.now()
    
    for i in range(months):
        future_X = np.array([[len(monthly_spending) + i]])
        predicted_spending = max(0, model.predict(future_X)[0])
        future_date = current_date + timedelta(days=30 * (i + 1))
        
        forecasts.append({
            "month": future_date.strftime("%Y-%m"),
            "predicted_spending": round_currency(predicted_spending),
            "predicted_income": round_currency(avg_income),
            "predicted_savings": round_currency(avg_income - predicted_spending),
            "confidence_lower": round_currency(max(0, predicted_spending - 1.96 * std_dev)),
            "confidence_upper": round_currency(predicted_spending + 1.96 * std_dev)
        })
    
    avg_spending = float(monthly_spending.mean())
    savings_rate = calculate_percentage(avg_income - avg_spending, avg_income)
    
    return {
        "forecasts": forecasts,
        "average_monthly_spending": round_currency(avg_spending),
        "average_monthly_income": round_currency(avg_income),
        "spending_trend": trend,
        "savings_rate": savings_rate,
        "advice": _generate_advice(savings_rate, trend)
    }


@router.post("/forecast", response_model=ForecastResponse)
async def get_forecast(request: ForecastRequest):
    """
    Generate spending forecast for the next N months.
    Uses historical transaction data to predict future spending patterns.
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
