"""
Transaction categorization endpoint.
Uses keyword matching and simple NLP to categorize transactions.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import re

from app.core.config import settings


router = APIRouter()


class CategorizeRequest(BaseModel):
    """Request model for categorization."""
    description: str


class CategorizeResponse(BaseModel):
    """Response model for categorization."""
    description: str
    category: str
    confidence: float
    matched_keywords: list[str]


def categorize_transaction(description: str) -> tuple[str, float, list[str]]:
    """
    Categorize a transaction based on its description.
    
    Args:
        description: Transaction description text
        
    Returns:
        Tuple of (category, confidence, matched_keywords)
    """
    description_lower = description.lower()
    
    best_category = "Uncategorized"
    best_score = 0
    matched_keywords = []
    
    for category, keywords in settings.CATEGORY_KEYWORDS.items():
        matches = []
        for keyword in keywords:
            # Use word boundary matching for better accuracy
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, description_lower) or keyword.lower() in description_lower:
                matches.append(keyword)
        
        if len(matches) > best_score:
            best_score = len(matches)
            best_category = category
            matched_keywords = matches
    
    # Calculate confidence based on number of matches
    if best_score == 0:
        confidence = 0.0
    elif best_score == 1:
        confidence = 0.7
    elif best_score == 2:
        confidence = 0.85
    else:
        confidence = 0.95
    
    return best_category, confidence, matched_keywords


@router.post("/categorize", response_model=CategorizeResponse)
async def categorize(request: CategorizeRequest):
    """
    Categorize a transaction based on its description.
    
    Uses keyword matching to determine the most likely category
    for the transaction.
    """
    if not request.description or len(request.description.strip()) == 0:
        raise HTTPException(status_code=400, detail="Description cannot be empty")
    
    category, confidence, keywords = categorize_transaction(request.description)
    
    return CategorizeResponse(
        description=request.description,
        category=category,
        confidence=confidence,
        matched_keywords=keywords
    )


@router.post("/categorize/batch")
async def categorize_batch(descriptions: list[str]):
    """
    Categorize multiple transactions at once.
    
    Args:
        descriptions: List of transaction descriptions
        
    Returns:
        List of categorization results
    """
    results = []
    for desc in descriptions:
        category, confidence, keywords = categorize_transaction(desc)
        results.append({
            "description": desc,
            "category": category,
            "confidence": confidence,
            "matched_keywords": keywords
        })
    
    return {"results": results}
