"""
Configuration settings for the AI Agent Service.
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Service configuration
    SERVICE_NAME: str = "smartspend-ai-agent"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # OpenAI configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://backend:8080"
    ]
    
    # AI Agent prompts
    SYSTEM_PROMPT: str = """You are SmartSpend AI, a friendly and knowledgeable personal finance assistant. 
Your role is to help users understand their spending habits, provide actionable financial advice, 
and answer questions about budgeting, saving, and investing.

Guidelines:
- Be concise but helpful
- Use simple language, avoid jargon
- Provide specific, actionable advice when possible
- Be encouraging and supportive
- If you don't have enough information, ask clarifying questions
- Never give specific investment advice or guarantee returns
- Focus on general financial literacy and budgeting tips"""

    ADVICE_PROMPT_TEMPLATE: str = """Based on the following financial data, provide personalized financial advice:

Financial Summary:
- Total Balance: ${total_balance}
- Monthly Income: ${monthly_income}
- Monthly Expenses: ${monthly_expenses}
- Monthly Savings: ${monthly_savings}
- Savings Rate: {savings_rate}%

Spending by Category:
{category_breakdown}

Please provide:
1. An overall assessment of the user's financial health
2. 2-3 specific, actionable recommendations
3. One area they're doing well in
4. One area for improvement

Keep your response concise and friendly."""

    class Config:
        env_file = ".env"


settings = Settings()
