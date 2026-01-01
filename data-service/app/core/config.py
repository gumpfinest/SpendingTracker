"""
Configuration settings for the Data Service.
"""

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Service configuration
    SERVICE_NAME: str = "smartspend-data-service"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://backend:8080"
    ]
    
    # Category keywords mapping
    CATEGORY_KEYWORDS: dict = {
        "Food & Dining": [
            "restaurant", "cafe", "coffee", "starbucks", "mcdonald", "burger",
            "pizza", "sushi", "thai", "chinese", "indian", "mexican", "italian",
            "doordash", "ubereats", "grubhub", "dining", "lunch", "dinner",
            "breakfast", "snack", "bakery", "deli"
        ],
        "Groceries": [
            "grocery", "supermarket", "walmart", "target", "costco", "safeway",
            "kroger", "whole foods", "trader joe", "aldi", "publix", "food mart"
        ],
        "Transportation": [
            "uber", "lyft", "taxi", "gas", "fuel", "shell", "chevron", "exxon",
            "parking", "toll", "transit", "metro", "bus", "train", "airline",
            "flight", "car rental", "hertz", "enterprise"
        ],
        "Shopping": [
            "amazon", "ebay", "etsy", "mall", "store", "shop", "retail",
            "clothing", "shoes", "electronics", "best buy", "apple store",
            "home depot", "lowes", "ikea", "furniture"
        ],
        "Entertainment": [
            "netflix", "spotify", "hulu", "disney", "hbo", "movie", "cinema",
            "theater", "concert", "game", "gaming", "steam", "playstation",
            "xbox", "nintendo", "ticket", "event"
        ],
        "Bills & Utilities": [
            "electric", "water", "gas bill", "internet", "phone", "mobile",
            "verizon", "at&t", "t-mobile", "comcast", "utility", "insurance",
            "rent", "mortgage", "hoa"
        ],
        "Healthcare": [
            "doctor", "hospital", "clinic", "pharmacy", "cvs", "walgreens",
            "medical", "dental", "dentist", "vision", "optometrist", "health",
            "prescription", "medicine"
        ],
        "Personal Care": [
            "salon", "spa", "haircut", "barber", "gym", "fitness", "yoga",
            "massage", "beauty", "cosmetics", "sephora", "ulta"
        ],
        "Education": [
            "tuition", "school", "college", "university", "course", "udemy",
            "coursera", "book", "textbook", "education", "learning"
        ],
        "Travel": [
            "hotel", "airbnb", "booking", "expedia", "vacation", "resort",
            "travel", "trip", "tourism"
        ],
        "Subscriptions": [
            "subscription", "membership", "monthly", "annual", "premium",
            "pro plan", "plus"
        ],
        "Income": [
            "salary", "paycheck", "deposit", "transfer in", "refund",
            "reimbursement", "dividend", "interest", "bonus"
        ]
    }
    
    class Config:
        env_file = ".env"


settings = Settings()
