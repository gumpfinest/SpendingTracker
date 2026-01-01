"""
Spending patterns analysis endpoint.
Analyzes transaction patterns and provides insights.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


router = APIRouter()


class Transaction(BaseModel):
    """Transaction model for pattern analysis."""
    id: int
    description: str
    amount: float
    type: str
    category: Optional[str] = None
    date: str


class PatternsRequest(BaseModel):
    """Request model for pattern analysis."""
    user_id: int
    transactions: List[Transaction]


class SpendingPattern(BaseModel):
    """A detected spending pattern."""
    pattern_type: str
    description: str
    impact: str  # "positive", "negative", "neutral"
    recommendation: Optional[str] = None


class PatternsResponse(BaseModel):
    """Response model for pattern analysis."""
    user_id: int
    patterns: List[SpendingPattern]
    spending_personality: str
    risk_score: int  # 1-10, higher = more financial risk
    strengths: List[str]
    areas_for_improvement: List[str]


def analyze_patterns(transactions: List[Transaction]) -> dict:
    """
    Analyze transaction patterns to identify spending behaviors.
    
    Args:
        transactions: List of user transactions
        
    Returns:
        Dictionary containing pattern analysis results
    """
    if not transactions:
        return {
            "patterns": [],
            "spending_personality": "Unknown",
            "risk_score": 5,
            "strengths": [],
            "areas_for_improvement": ["Add transactions to analyze your spending patterns"]
        }
    
    patterns = []
    strengths = []
    improvements = []
    
    # Parse transactions
    expense_transactions = []
    income_transactions = []
    
    for t in transactions:
        try:
            date = datetime.fromisoformat(t.date.replace('Z', '+00:00'))
        except:
            date = datetime.now()
        
        tx_data = {
            "amount": float(t.amount),
            "category": t.category or "Uncategorized",
            "description": t.description.lower(),
            "date": date,
            "day_of_week": date.weekday(),
            "hour": date.hour
        }
        
        if t.type == "EXPENSE":
            expense_transactions.append(tx_data)
        else:
            income_transactions.append(tx_data)
    
    # Pattern 1: Weekend spending
    weekend_spending = sum(t["amount"] for t in expense_transactions if t["day_of_week"] >= 5)
    weekday_spending = sum(t["amount"] for t in expense_transactions if t["day_of_week"] < 5)
    
    if weekend_spending > weekday_spending * 0.5 and len(expense_transactions) >= 5:
        patterns.append({
            "pattern_type": "weekend_spender",
            "description": "You tend to spend significantly more on weekends",
            "impact": "negative",
            "recommendation": "Plan weekend activities in advance to avoid impulse spending"
        })
        improvements.append("Reduce weekend impulse spending")
    
    # Pattern 2: Category concentration
    category_spending = defaultdict(float)
    for t in expense_transactions:
        category_spending[t["category"]] += t["amount"]
    
    total_spending = sum(category_spending.values())
    for category, amount in category_spending.items():
        if total_spending > 0:
            percentage = (amount / total_spending) * 100
            if percentage > 40:
                patterns.append({
                    "pattern_type": "category_heavy",
                    "description": f"{category} accounts for {percentage:.0f}% of your spending",
                    "impact": "neutral",
                    "recommendation": f"Review if {category} spending aligns with your priorities"
                })
    
    # Pattern 3: Small frequent purchases
    small_purchases = [t for t in expense_transactions if t["amount"] < 20]
    if len(small_purchases) > len(expense_transactions) * 0.6:
        total_small = sum(t["amount"] for t in small_purchases)
        patterns.append({
            "pattern_type": "small_purchases",
            "description": f"Many small purchases adding up to ${total_small:.2f}",
            "impact": "negative",
            "recommendation": "Small purchases can add up quickly. Consider tracking these more carefully."
        })
        improvements.append("Monitor small, frequent purchases")
    
    # Pattern 4: Large irregular expenses
    if expense_transactions:
        amounts = [t["amount"] for t in expense_transactions]
        avg_expense = sum(amounts) / len(amounts)
        large_expenses = [t for t in expense_transactions if t["amount"] > avg_expense * 3]
        
        if large_expenses:
            patterns.append({
                "pattern_type": "irregular_large",
                "description": f"Found {len(large_expenses)} unusually large expense(s)",
                "impact": "neutral",
                "recommendation": "Plan for large expenses by setting aside money in advance"
            })
    
    # Pattern 5: Consistent income
    if len(income_transactions) >= 2:
        income_amounts = [t["amount"] for t in income_transactions]
        if max(income_amounts) - min(income_amounts) < sum(income_amounts) / len(income_amounts) * 0.1:
            patterns.append({
                "pattern_type": "stable_income",
                "description": "Your income is consistent and predictable",
                "impact": "positive",
                "recommendation": None
            })
            strengths.append("Stable, predictable income")
    
    # Pattern 6: Subscription detection
    subscription_keywords = ["netflix", "spotify", "hulu", "subscription", "monthly", "membership"]
    subscriptions = [t for t in expense_transactions 
                     if any(kw in t["description"] for kw in subscription_keywords)]
    
    if subscriptions:
        total_subs = sum(t["amount"] for t in subscriptions)
        patterns.append({
            "pattern_type": "subscriptions",
            "description": f"Detected {len(subscriptions)} subscription payment(s) totaling ${total_subs:.2f}",
            "impact": "neutral",
            "recommendation": "Review subscriptions regularly and cancel any you don't use"
        })
    
    # Calculate risk score
    risk_score = 5
    negative_patterns = sum(1 for p in patterns if p["impact"] == "negative")
    positive_patterns = sum(1 for p in patterns if p["impact"] == "positive")
    
    if total_spending > 0 and income_transactions:
        total_income = sum(t["amount"] for t in income_transactions)
        if total_spending > total_income:
            risk_score += 2
            improvements.append("Spending exceeds income")
        elif total_spending < total_income * 0.7:
            risk_score -= 2
            strengths.append("Good savings rate")
    
    risk_score += negative_patterns
    risk_score -= positive_patterns
    risk_score = max(1, min(10, risk_score))
    
    # Determine spending personality
    if not patterns:
        personality = "Balanced Spender"
    elif risk_score <= 3:
        personality = "Savvy Saver"
    elif risk_score <= 5:
        personality = "Balanced Spender"
    elif risk_score <= 7:
        personality = "Casual Spender"
    else:
        personality = "Spontaneous Spender"
    
    # Add default strength if none found
    if not strengths:
        strengths.append("You're tracking your finances - that's a great start!")
    
    return {
        "patterns": patterns,
        "spending_personality": personality,
        "risk_score": risk_score,
        "strengths": strengths,
        "areas_for_improvement": improvements if improvements else ["Keep up the good work!"]
    }


@router.post("/patterns", response_model=PatternsResponse)
async def analyze_spending_patterns(request: PatternsRequest):
    """
    Analyze user's spending patterns and provide behavioral insights.
    
    Identifies patterns like weekend spending, category concentration,
    and provides a spending personality assessment.
    """
    result = analyze_patterns(request.transactions)
    
    return PatternsResponse(
        user_id=request.user_id,
        patterns=[SpendingPattern(**p) for p in result["patterns"]],
        spending_personality=result["spending_personality"],
        risk_score=result["risk_score"],
        strengths=result["strengths"],
        areas_for_improvement=result["areas_for_improvement"]
    )
