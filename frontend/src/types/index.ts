// API Types

export interface User {
  id: number;
  username: string;
  name: string;
}

export interface AuthResponse {
  token: string;
  type: string;
  userId: number;
  username: string;
  name: string;
}

export interface Transaction {
  id: number;
  description: string;
  amount: number;
  type: 'INCOME' | 'EXPENSE';
  category: string | null;
  status: 'PENDING' | 'CATEGORIZED' | 'PROCESSED';
  transactionDate: string;
  notes: string | null;
  createdAt: string;
}

export interface CreateTransactionRequest {
  description: string;
  amount: number;
  type: 'INCOME' | 'EXPENSE';
  category?: string;
  transactionDate?: string;
  notes?: string;
}

export interface Budget {
  id: number;
  category: string;
  monthlyLimit: number;
  currentSpent: number;
  remaining: number;
  percentageUsed: number;
  month: number;
  year: number;
}

export interface CreateBudgetRequest {
  category: string;
  monthlyLimit: number;
  month: number;
  year: number;
}

export interface DashboardSummary {
  totalBalance: number;
  monthlyIncome: number;
  monthlyExpenses: number;
  monthlySavings: number;
  spendingByCategory: Record<string, number>;
  recentTransactions: Transaction[];
}

export interface SpendingForecast {
  forecasts: MonthlyForecast[];
  average_monthly_spending: number;
  average_monthly_income: number;
  spending_trend: 'increasing' | 'decreasing' | 'stable';
  savings_rate: number;
  advice: string;
}

export interface MonthlyForecast {
  month: string;
  predicted_spending: number;
  predicted_income: number;
  predicted_savings: number;
  confidence_lower: number;
  confidence_upper: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface AiAdvice {
  summary: string;
  recommendations: string[];
  savingsOpportunities: string[];
}

export interface SpendingSummary {
  totalIncome: number;
  totalExpenses: number;
  categoryBreakdown: Record<string, number>;
}

export interface AiChatRequest {
  message: string;
  context?: {
    recentTransactions?: Transaction[];
    budgets?: Budget[];
  };
}

export interface AiChatResponse {
  response: string;
  suggestions?: string[];
}

export interface SpendingPattern {
  pattern: string;
  description: string;
  impact: 'positive' | 'negative' | 'neutral';
}
