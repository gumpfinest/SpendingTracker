"""
AI Agent - Core AI functionality.
Provides AI capabilities using OpenAI or rule-based fallback.
"""

from typing import Dict, List, Optional
import os

from app.core.config import settings


class FinancialAIAgent:
    """AI Agent for financial advice and analysis."""
    
    def __init__(self):
        self.openai_available = False
        self.client = None
        
        # Try to initialize OpenAI client
        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.openai_available = True
            except Exception as e:
                print(f"OpenAI not available: {e}")
    
    def get_advice(self, financial_data: Dict) -> str:
        """
        Generate financial advice based on user's financial data.
        
        Args:
            financial_data: Dictionary containing financial metrics
            
        Returns:
            Personalized financial advice string
        """
        if self.openai_available:
            return self._get_ai_advice(financial_data)
        return self._get_rule_based_advice(financial_data)
    
    def _get_ai_advice(self, financial_data: Dict) -> str:
        """Generate advice using OpenAI."""
        try:
            # Format the data for the prompt
            total_balance = financial_data.get('totalBalance', 0)
            monthly_income = financial_data.get('monthlyIncome', 0)
            monthly_expenses = financial_data.get('monthlyExpenses', 0)
            monthly_savings = financial_data.get('monthlySavings', 0)
            spending_by_category = financial_data.get('spendingByCategory', {})
            
            savings_rate = (monthly_savings / monthly_income * 100) if monthly_income > 0 else 0
            
            category_breakdown = "\n".join([
                f"- {cat}: ${amount:.2f}" 
                for cat, amount in spending_by_category.items()
            ]) or "No category data available"
            
            prompt = settings.ADVICE_PROMPT_TEMPLATE.format(
                total_balance=f"{total_balance:,.2f}",
                monthly_income=f"{monthly_income:,.2f}",
                monthly_expenses=f"{monthly_expenses:,.2f}",
                monthly_savings=f"{monthly_savings:,.2f}",
                savings_rate=f"{savings_rate:.1f}",
                category_breakdown=category_breakdown
            )
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": settings.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error getting AI advice: {e}")
            return self._get_rule_based_advice(financial_data)
    
    def _get_rule_based_advice(self, financial_data: Dict) -> str:
        """Generate advice using rules when AI is not available."""
        monthly_income = financial_data.get('monthlyIncome', 0)
        monthly_expenses = financial_data.get('monthlyExpenses', 0)
        monthly_savings = financial_data.get('monthlySavings', 0)
        spending_by_category = financial_data.get('spendingByCategory', {})
        
        advice_parts = []
        
        # Savings rate analysis
        if monthly_income > 0:
            savings_rate = (monthly_savings / monthly_income) * 100
            
            if savings_rate < 0:
                advice_parts.append(
                    "⚠️ **Alert**: You're spending more than you earn this month. "
                    "Review your expenses immediately and identify non-essential spending to cut."
                )
            elif savings_rate < 10:
                advice_parts.append(
                    "📊 **Savings Rate**: Your current savings rate is below 10%. "
                    "Financial experts recommend saving at least 20% of your income. "
                    "Consider the 50/30/20 rule: 50% needs, 30% wants, 20% savings."
                )
            elif savings_rate < 20:
                advice_parts.append(
                    f"📊 **Good Progress**: You're saving {savings_rate:.1f}% of your income. "
                    "Try to increase this to 20% by cutting discretionary spending."
                )
            else:
                advice_parts.append(
                    f"🌟 **Excellent**: You're saving {savings_rate:.1f}% of your income! "
                    "Consider investing your extra savings in a diversified portfolio."
                )
        
        # Category-specific advice
        if spending_by_category:
            total_expenses = sum(spending_by_category.values())
            
            for category, amount in spending_by_category.items():
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                
                if category == "Food & Dining" and percentage > 25:
                    advice_parts.append(
                        f"🍽️ **Food & Dining** accounts for {percentage:.1f}% of your spending. "
                        "Consider meal prepping or cooking at home more often to reduce this."
                    )
                elif category == "Entertainment" and percentage > 15:
                    advice_parts.append(
                        f"🎬 **Entertainment** spending is {percentage:.1f}% of expenses. "
                        "Look for free or low-cost alternatives for entertainment."
                    )
                elif category == "Shopping" and percentage > 20:
                    advice_parts.append(
                        f"🛍️ **Shopping** represents {percentage:.1f}% of your spending. "
                        "Try implementing a 24-hour rule before non-essential purchases."
                    )
        
        # Emergency fund advice
        if monthly_expenses > 0:
            emergency_fund_target = monthly_expenses * 6
            advice_parts.append(
                f"💰 **Emergency Fund Goal**: Aim to save ${emergency_fund_target:,.0f} "
                f"(6 months of expenses) for financial security."
            )
        
        return "\n\n".join(advice_parts) if advice_parts else (
            "Start tracking your income and expenses to receive personalized financial advice."
        )
    
    def chat(self, message: str, context: Dict) -> str:
        """
        Handle chat messages from users.
        
        Args:
            message: User's message
            context: Financial context for the conversation
            
        Returns:
            AI response string
        """
        if self.openai_available:
            return self._ai_chat(message, context)
        return self._rule_based_chat(message, context)
    
    def _ai_chat(self, message: str, context: Dict) -> str:
        """Handle chat using OpenAI."""
        try:
            context_str = f"""
User's Financial Context:
- Total Balance: ${context.get('totalBalance', 0):,.2f}
- Monthly Income: ${context.get('monthlyIncome', 0):,.2f}
- Monthly Expenses: ${context.get('monthlyExpenses', 0):,.2f}
"""
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": settings.SYSTEM_PROMPT + "\n\n" + context_str},
                    {"role": "user", "content": message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in AI chat: {e}")
            return self._rule_based_chat(message, context)
    
    def _rule_based_chat(self, message: str, context: Dict) -> str:
        """Handle chat using rules when AI is not available."""
        message_lower = message.lower()
        
        # Simple keyword-based responses
        if any(word in message_lower for word in ["save", "saving", "savings"]):
            return (
                "Great question about savings! Here are some tips:\n"
                "1. Start with the 50/30/20 rule\n"
                "2. Set up automatic transfers to savings\n"
                "3. Track your spending to find areas to cut\n"
                "4. Build an emergency fund with 3-6 months of expenses"
            )
        
        if any(word in message_lower for word in ["budget", "budgeting"]):
            return (
                "Budgeting is key to financial success! Try these steps:\n"
                "1. List all your income sources\n"
                "2. Track every expense for a month\n"
                "3. Categorize spending (needs vs wants)\n"
                "4. Set realistic limits for each category\n"
                "5. Review and adjust monthly"
            )
        
        if any(word in message_lower for word in ["invest", "investing", "investment"]):
            return (
                "Smart thinking about investing! General tips:\n"
                "1. First, pay off high-interest debt\n"
                "2. Build an emergency fund\n"
                "3. Take advantage of employer 401(k) matching\n"
                "4. Consider low-cost index funds for beginners\n"
                "Note: Consider consulting a financial advisor for personalized advice."
            )
        
        if any(word in message_lower for word in ["debt", "loan", "credit"]):
            return (
                "Managing debt is important! Consider:\n"
                "1. List all debts with interest rates\n"
                "2. Pay minimums on all, extra on highest rate (avalanche method)\n"
                "3. Or pay smallest debts first for motivation (snowball method)\n"
                "4. Avoid taking on new debt while paying off existing"
            )
        
        if any(word in message_lower for word in ["spend", "spending", "expense"]):
            monthly_expenses = context.get('monthlyExpenses', 0)
            return (
                f"Your current monthly expenses are ${monthly_expenses:,.2f}.\n"
                "Tips to reduce spending:\n"
                "1. Review subscriptions and cancel unused ones\n"
                "2. Cook at home more often\n"
                "3. Use the 24-hour rule for non-essential purchases\n"
                "4. Look for free entertainment options"
            )
        
        # Default response
        return (
            "I'm here to help with your finances! You can ask me about:\n"
            "• Saving money and building an emergency fund\n"
            "• Creating and sticking to a budget\n"
            "• Managing debt effectively\n"
            "• Understanding your spending patterns\n"
            "• General investment principles\n\n"
            "What would you like to know more about?"
        )


# Global agent instance
agent = FinancialAIAgent()
