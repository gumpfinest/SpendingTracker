"""
Shared utility functions for data processing.
"""

from datetime import datetime
from typing import List, Dict, Any
import pandas as pd

from app.core.models import Transaction


def parse_date(date_str: str) -> datetime:
    """
    Parse a date string to datetime object.
    Handles ISO format with optional timezone.
    
    Args:
        date_str: Date string in ISO format
        
    Returns:
        datetime object
    """
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except (ValueError, AttributeError):
        return datetime.now()


def transactions_to_dataframe(transactions: List[Transaction]) -> pd.DataFrame:
    """
    Convert a list of transactions to a pandas DataFrame.
    
    Args:
        transactions: List of Transaction objects
        
    Returns:
        DataFrame with parsed dates and month column
    """
    if not transactions:
        return pd.DataFrame(columns=['id', 'description', 'amount', 'type', 'category', 'date', 'month'])
    
    data = [{
        "id": t.id,
        "description": t.description,
        "amount": float(t.amount),
        "type": t.type,
        "category": t.category or "Uncategorized",
        "date": parse_date(t.date)
    } for t in transactions]
    
    df = pd.DataFrame(data)
    df['month'] = df['date'].dt.to_period('M')
    return df


def round_currency(value: float, decimals: int = 2) -> float:
    """Round a currency value to specified decimal places."""
    return round(float(value), decimals)


def calculate_percentage(part: float, total: float) -> float:
    """Calculate percentage with zero-division protection."""
    return round(part / total * 100, 2) if total > 0 else 0.0


def get_empty_analysis_result() -> Dict[str, Any]:
    """Return empty analysis result for when there are no transactions."""
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
