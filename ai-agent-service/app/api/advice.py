"""
Financial advice endpoint.
Generates personalized financial advice based on user data.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Optional

from app.core.agent import agent


router = APIRouter()


class AdviceRequest(BaseModel):
    """Request model for financial advice."""
    user_id: int
    financial_data: Dict


class AdviceResponse(BaseModel):
    """Response model for financial advice."""
    user_id: int
    advice: str
    ai_generated: bool


@router.post("/advice", response_model=AdviceResponse)
async def get_financial_advice(request: AdviceRequest):
    """
    Get personalized financial advice based on user's financial data.
    
    Uses AI when available, falls back to rule-based advice otherwise.
    """
    advice = agent.get_advice(request.financial_data)
    
    return AdviceResponse(
        user_id=request.user_id,
        advice=advice,
        ai_generated=agent.openai_available
    )


@router.post("/advice/quick")
async def get_quick_tip():
    """Get a random quick financial tip."""
    tips = [
        "💡 Save at least 20% of your income if possible.",
        "💡 Pay yourself first - set up automatic savings transfers.",
        "💡 Review subscriptions monthly and cancel unused ones.",
        "💡 Use the 24-hour rule before making non-essential purchases.",
        "💡 Build an emergency fund with 3-6 months of expenses.",
        "💡 Pay more than the minimum on credit cards when possible.",
        "💡 Track every expense for one month to understand your spending.",
        "💡 Set specific, measurable financial goals.",
        "💡 Review your budget at the end of each month.",
        "💡 Look for ways to increase income, not just cut expenses."
    ]
    
    import random
    return {"tip": random.choice(tips)}
