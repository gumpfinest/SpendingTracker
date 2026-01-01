"""
Spending analysis endpoint.
Provides detailed breakdown of spending patterns and insights.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

from app.core.models import Transaction
from app.core.utils import (
    transactions_to_dataframe,
    round_currency,
    calculate_percentage,
    get_empty_analysis_result
)


router = APIRouter()


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
        return get_empty_analysis_result()
    
    df = transactions_to_dataframe(transactions)
    
    # Basic totals
    total_income = df[df['type'] == 'INCOME']['amount'].sum()
    total_expenses = df[df['type'] == 'EXPENSE']['amount'].sum()
    net_balance = total_income - total_expenses
    
    # Category breakdown
    expenses_df = df[df['type'] == 'EXPENSE']
    category_breakdown = _calculate_category_breakdown(expenses_df)
    
    # Monthly breakdown
    monthly_breakdown = _calculate_monthly_breakdown(df, expenses_df)
    
    # Top spending categories
    top_categories = [cb['category'] for cb in category_breakdown[:5]]
    
    # Detect unusual transactions
    unusual_transactions = _detect_unusual_transactions(expenses_df)
    
    # Generate insights
    insights = _generate_insights(
        category_breakdown, total_income, net_balance,
        monthly_breakdown, unusual_transactions
    )
    
    return {
        "total_transactions": len(transactions),
        "total_income": round_currency(total_income),
        "total_expenses": round_currency(total_expenses),
        "net_balance": round_currency(net_balance),
        "category_breakdown": category_breakdown,
        "monthly_breakdown": monthly_breakdown,
        "top_spending_categories": top_categories,
        "unusual_transactions": unusual_transactions,
        "insights": insights
    }


def _calculate_category_breakdown(expenses_df) -> List[dict]:
    """Calculate spending breakdown by category."""
    if expenses_df.empty:
        return []
    
    stats = expenses_df.groupby('category').agg({
        'amount': ['sum', 'count', 'mean']
    }).reset_index()
    stats.columns = ['category', 'total_spent', 'transaction_count', 'average_transaction']
    
    total_spent = stats['total_spent'].sum()
    
    breakdown = [{
        "category": row['category'],
        "total_spent": round_currency(row['total_spent']),
        "transaction_count": int(row['transaction_count']),
        "average_transaction": round_currency(row['average_transaction']),
        "percentage_of_total": calculate_percentage(row['total_spent'], total_spent),
        "trend": "stable"
    } for _, row in stats.iterrows()]
    
    return sorted(breakdown, key=lambda x: x['total_spent'], reverse=True)


def _calculate_monthly_breakdown(df, expenses_df) -> List[dict]:
    """Calculate monthly spending and income breakdown."""
    monthly_data = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
    
    breakdown = []
    for month in monthly_data.index:
        month_expenses = expenses_df[expenses_df['month'] == month]
        top_cat = "N/A"
        if not month_expenses.empty:
            top_cat = month_expenses.groupby('category')['amount'].sum().idxmax()
        
        income = float(monthly_data.loc[month, 'INCOME']) if 'INCOME' in monthly_data.columns else 0
        spending = float(monthly_data.loc[month, 'EXPENSE']) if 'EXPENSE' in monthly_data.columns else 0
        
        breakdown.append({
            "month": str(month),
            "total_spending": round_currency(spending),
            "total_income": round_currency(income),
            "net_savings": round_currency(income - spending),
            "top_category": top_cat
        })
    
    return breakdown


def _detect_unusual_transactions(expenses_df) -> List[dict]:
    """Detect unusually large transactions using statistical analysis."""
    if len(expenses_df) <= 5:
        return []
    
    mean_expense = expenses_df['amount'].mean()
    std_expense = expenses_df['amount'].std()
    threshold = mean_expense + 2 * std_expense
    
    outliers = expenses_df[expenses_df['amount'] > threshold]
    
    return [{
        "id": row['id'],
        "description": row['description'],
        "amount": round_currency(row['amount']),
        "reason": f"Amount is {round(row['amount']/mean_expense, 1)}x your average expense"
    } for _, row in outliers.iterrows()]


def _generate_insights(category_breakdown, total_income, net_balance,
                       monthly_breakdown, unusual_transactions) -> List[str]:
    """Generate actionable insights from the analysis."""
    insights = []
    
    if category_breakdown:
        top = category_breakdown[0]
        insights.append(
            f"Your highest spending category is {top['category']}, "
            f"accounting for {top['percentage_of_total']:.1f}% of expenses."
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
        recent = monthly_breakdown[-1]['total_spending']
        prev = monthly_breakdown[-2]['total_spending']
        if recent > prev * 1.2:
            insights.append("📈 Your spending increased by more than 20% compared to last month.")
        elif recent < prev * 0.8:
            insights.append("📉 Great! Your spending decreased by more than 20% compared to last month.")
    
    if unusual_transactions:
        insights.append(f"🔍 We detected {len(unusual_transactions)} unusually large transaction(s).")
    
    return insights


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
    """Get detailed analysis for a specific spending category."""
    transactions = [t for t in request.transactions if t.category == category]
    
    if not transactions:
        raise HTTPException(status_code=404, detail=f"No transactions found for category: {category}")
    
    df = transactions_to_dataframe(transactions)
    
    return {
        "category": category,
        "total_spent": round_currency(df['amount'].sum()),
        "transaction_count": len(df),
        "average_transaction": round_currency(df['amount'].mean()),
        "min_transaction": round_currency(df['amount'].min()),
        "max_transaction": round_currency(df['amount'].max()),
        "recent_transactions": [
            {"description": row['description'], "amount": round_currency(row['amount']), "date": str(row['date'])}
            for _, row in df.nlargest(5, 'date').iterrows()
        ]
    }
