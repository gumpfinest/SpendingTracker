"""
Shared Pydantic models for the Data Service.
"""

from pydantic import BaseModel
from typing import Optional


class Transaction(BaseModel):
    """Transaction model for data processing endpoints."""
    id: int
    description: str
    amount: float
    type: str  # INCOME or EXPENSE
    category: Optional[str] = None
    date: str  # ISO format date string
