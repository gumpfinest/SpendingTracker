"""
Spending analysis endpoint.
Provides detailed breakdown of spending patterns and insights.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import pandas as pd
import numpy as np


router = APIRouter()


class Transaction(BaseModel):
    """Transaction model for analysis input."""
    id: int
    description: str
    amount: float
    type: str  # INCOME or EXPENSE
    category: Optional[str] = None
    date: str  # ISO format date string


class AnalyzeRequest(BaseModel):
    """Request model for analysis."""
    user_id: int
    transactions: List[Transaction]


class CategoryBreakdown(BaseModel):
    """Category spending breakdown."""
    category: str
    total_spent: float
    transaction_count: int
    average_transaction: float
    percentage_of_total: float
    trend: str  # "up", "down", "stable"


class MonthlyBreakdown(BaseModel):
    """Monthly spending breakdown."""
    month: str
    total_spending: float
    total_income: float
    net_savings: float
    top_category: str


class AnalyzeResponse(BaseModel):
    """Response model for analysis."""
    user_id: int
    total_transactions: int
    total_income: float
    total_expenses: float
    net_balance: float
    category_breakdown: List[CategoryBreakdown]
    monthly_breakdown: List[MonthlyBreakdown]
    top_spending_categories: List[str]
    unusual_transactions: List[Dict]
    insights: List[str]


def analyze_transactions(transactions: List[Transaction]) -> dict:
    """
    Perform comprehensive analysis on transactions.
    
    Args:
        transactions: List of transactions to analyze
        
    Returns:
        Dictionary containing analysis results
    """
    if not transactions:
        return {
            "total_transactions": 0,
            "total_income": 0,
            "total_expenses": 0,
            "net_balance": 0,
            "category_breakdown": [],
            "monthly_breakdown": [],
            "top_spending_categories": [],
            "unusual_transactions": [],
            "insights": ["Add transactions to get spending insights."]
        }
    
    # Convert to DataFrame
    data = []
    for t in transactions:
        try:
            date = datetime.fromisoformat(t.date.replace('Z', '+00:00'))
        except:
            date = datetime.now()
        
        data.append({
            "id": t.id,
            "description": t.description,
            "amount": float(t.amount),
            "type": t.type,
            "category": t.category or "Uncategorized",
            "date": date
        })
    
    df = pd.DataFrame(data)
    df['month'] = df['date'].dt.to_period('M')
    
    # Basic totals
    total_income = df[df['type'] == 'INCOME']['amount'].sum()
    total_expenses = df[df['type'] == 'EXPENSE']['amount'].sum()
    net_balance = total_income - total_expenses
    
    # Category breakdown
    expenses_df = df[df['type'] == 'EXPENSE']
    category_stats = expenses_df.groupby('category').agg({
        'amount': ['sum', 'count', 'mean']
    }).reset_index()
    
    category_stats.columns = ['category', 'total_spent', 'transaction_count', 'average_transaction']
    
    # Calculate percentage
    total_spent = category_stats['total_spent'].sum()
    category_stats['percentage_of_total'] = (
        category_stats['total_spent'] / total_spent * 100 if total_spent > 0 else 0
    )
    
    # Simple trend calculation (would need more data for real trend)
    category_stats['trend'] = 'stable'
    
    category_breakdown = []
    for _, row in category_stats.iterrows():
        category_breakdown.append({
            "category": row['category'],
            "total_spent": round(float(row['total_spent']), 2),
            "transaction_count": int(row['transaction_count']),
            "average_transaction": round(float(row['average_transaction']), 2),
            "percentage_of_total": round(float(row['percentage_of_total']), 2),
            "trend": row['trend']
        })
    
    # Sort by total spent
    category_breakdown.sort(key=lambda x: x['total_spent'], reverse=True)
    
    # Monthly breakdown
    monthly_data = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
    
    monthly_breakdown = []
    for month in monthly_data.index:
        month_expenses = expenses_df[expenses_df['month'] == month]
        top_cat = "N/A"
        if not month_expenses.empty:
            top_cat = month_expenses.groupby('category')['amount'].sum().idxmax()
        
        income = float(monthly_data.loc[month, 'INCOME']) if 'INCOME' in monthly_data.columns else 0
        spending = float(monthly_data.loc[month, 'EXPENSE']) if 'EXPENSE' in monthly_data.columns else 0
        
        monthly_breakdown.append({
            "month": str(month),
            "total_spending": round(spending, 2),
            "total_income": round(income, 2),
            "net_savings": round(income - spending, 2),
            "top_category": top_cat
        })
    
    # Top spending categories
    top_categories = [cb['category'] for cb in category_breakdown[:5]]
    
    # Detect unusual transactions (simple outlier detection)
    unusual_transactions = []
    if len(expenses_df) > 5:
        mean_expense = expenses_df['amount'].mean()
        std_expense = expenses_df['amount'].std()
        threshold = mean_expense + 2 * std_expense
        
        outliers = expenses_df[expenses_df['amount'] > threshold]
        for _, row in outliers.iterrows():
            unusual_transactions.append({
                "id": row['id'],
                "description": row['description'],
                "amount": round(float(row['amount']), 2),
                "reason": f"Amount is {round(row['amount']/mean_expense, 1)}x your average expense"
            })
    
    # Generate insights
    insights = []
    
    if category_breakdown:
        top_category = category_breakdown[0]
        insights.append(
            f"Your highest spending category is {top_category['category']}, "
            f"accounting for {top_category['percentage_of_total']:.1f}% of expenses."
        )
    
    if total_income > 0:
        savings_rate = (net_balance / total_income) * 100
        if savings_rate < 0:
            insights.append("⚠️ You're spending more than you earn. Review your expenses to find areas to cut.")
        elif savings_rate < 20:
            insights.append(f"Your savings rate is {savings_rate:.1f}%. Try to aim for 20% or more.")
        else:
            insights.append(f"Great job! You're saving {savings_rate:.1f}% of your income.")
    
    if len(monthly_breakdown) >= 2:
        recent_spending = monthly_breakdown[-1]['total_spending']
        prev_spending = monthly_breakdown[-2]['total_spending']
        if recent_spending > prev_spending * 1.2:
            insights.append("📈 Your spending increased by more than 20% compared to last month.")
        elif recent_spending < prev_spending * 0.8:
            insights.append("📉 Great! Your spending decreased by more than 20% compared to last month.")
    
    if unusual_transactions:
        insights.append(f"🔍 We detected {len(unusual_transactions)} unusually large transaction(s).")
    
    return {
        "total_transactions": len(transactions),
        "total_income": round(float(total_income), 2),
        "total_expenses": round(float(total_expenses), 2),
        "net_balance": round(float(net_balance), 2),
        "category_breakdown": category_breakdown,
        "monthly_breakdown": monthly_breakdown,
        "top_spending_categories": top_categories,
        "unusual_transactions": unusual_transactions,
        "insights": insights
    }


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_spending(request: AnalyzeRequest):
    """
    Perform comprehensive analysis on user's transactions.
    
    Provides category breakdown, monthly trends, and actionable insights.
    """
    result = analyze_transactions(request.transactions)
    
    return AnalyzeResponse(
        user_id=request.user_id,
        total_transactions=result["total_transactions"],
        total_income=result["total_income"],
        total_expenses=result["total_expenses"],
        net_balance=result["net_balance"],
        category_breakdown=[CategoryBreakdown(**cb) for cb in result["category_breakdown"]],
        monthly_breakdown=[MonthlyBreakdown(**mb) for mb in result["monthly_breakdown"]],
        top_spending_categories=result["top_spending_categories"],
        unusual_transactions=result["unusual_transactions"],
        insights=result["insights"]
    )


@router.post("/analyze/category/{category}")
async def analyze_category(category: str, request: AnalyzeRequest):
    """
    Get detailed analysis for a specific spending category.
    """
    transactions = [t for t in request.transactions if t.category == category]
    
    if not transactions:
        raise HTTPException(status_code=404, detail=f"No transactions found for category: {category}")
    
    # Convert to DataFrame
    data = []
    for t in transactions:
        try:
            date = datetime.fromisoformat(t.date.replace('Z', '+00:00'))
        except:
            date = datetime.now()
        
        data.append({
            "description": t.description,
            "amount": float(t.amount),
            "date": date
        })
    
    df = pd.DataFrame(data)
    
    return {
        "category": category,
        "total_spent": round(float(df['amount'].sum()), 2),
        "transaction_count": len(df),
        "average_transaction": round(float(df['amount'].mean()), 2),
        "min_transaction": round(float(df['amount'].min()), 2),
        "max_transaction": round(float(df['amount'].max()), 2),
        "recent_transactions": [
            {"description": row['description'], "amount": round(row['amount'], 2), "date": str(row['date'])}
            for _, row in df.nlargest(5, 'date').iterrows()
        ]
    }
