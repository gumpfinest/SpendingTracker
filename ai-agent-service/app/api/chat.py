"""
Chat endpoint.
Handles conversational AI interactions with users.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Optional, List

from app.core.agent import agent


router = APIRouter()


class ChatMessage(BaseModel):
    """A single chat message."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Request model for chat."""
    user_id: int
    message: str
    context: Dict = {}
    history: List[ChatMessage] = []


class ChatResponse(BaseModel):
    """Response model for chat."""
    user_id: int
    response: str
    suggestions: List[str]


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Chat with the financial AI assistant.
    
    Provides conversational support for financial questions
    with context-aware responses.
    """
    response = agent.chat(request.message, request.context)
    
    # Generate follow-up suggestions based on the conversation
    suggestions = generate_suggestions(request.message)
    
    return ChatResponse(
        user_id=request.user_id,
        response=response,
        suggestions=suggestions
    )


def generate_suggestions(message: str) -> List[str]:
    """Generate follow-up question suggestions based on the user's message."""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["save", "saving"]):
        return [
            "How do I create an emergency fund?",
            "What's the best way to save for retirement?",
            "How can I save money on groceries?"
        ]
    
    if any(word in message_lower for word in ["budget", "spending"]):
        return [
            "What budgeting method should I use?",
            "How can I track my expenses better?",
            "What are common budget mistakes?"
        ]
    
    if any(word in message_lower for word in ["invest", "stock"]):
        return [
            "How do I start investing with little money?",
            "What are index funds?",
            "Should I pay off debt or invest?"
        ]
    
    if any(word in message_lower for word in ["debt", "loan", "credit"]):
        return [
            "How do I pay off debt faster?",
            "What's the debt avalanche method?",
            "How can I improve my credit score?"
        ]
    
    # Default suggestions
    return [
        "How can I save more money?",
        "Help me create a budget",
        "What's a good savings rate?"
    ]


@router.get("/chat/starters")
async def get_conversation_starters():
    """Get suggested conversation starters for new users."""
    return {
        "starters": [
            {
                "title": "💰 Savings Help",
                "prompt": "How can I save more money each month?"
            },
            {
                "title": "📊 Budget Review",
                "prompt": "Can you help me understand my spending habits?"
            },
            {
                "title": "🎯 Financial Goals",
                "prompt": "How do I set realistic financial goals?"
            },
            {
                "title": "📈 Investment Basics",
                "prompt": "What should I know about starting to invest?"
            },
            {
                "title": "💳 Debt Management",
                "prompt": "What's the best way to pay off my debt?"
            },
            {
                "title": "🏦 Emergency Fund",
                "prompt": "How much should I have in an emergency fund?"
            }
        ]
    }
