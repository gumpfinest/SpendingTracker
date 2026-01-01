import api from './api';
import {
  Transaction,
  CreateTransactionRequest,
  Budget,
  CreateBudgetRequest,
  DashboardSummary,
  SpendingForecast,
  AiAdvice,
  SpendingSummary,
  AiChatResponse,
} from '../types';

export const transactionService = {
  async getAll(): Promise<Transaction[]> {
    const response = await api.get<Transaction[]>('/transactions');
    return response.data;
  },

  async create(data: CreateTransactionRequest): Promise<Transaction> {
    const response = await api.post<Transaction>('/transactions', data);
    return response.data;
  },

  async update(id: number, data: Partial<CreateTransactionRequest>): Promise<Transaction> {
    const response = await api.put<Transaction>(`/transactions/${id}`, data);
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/transactions/${id}`);
  },
};

export const budgetService = {
  async getByMonth(month: number, year: number): Promise<Budget[]> {
    const response = await api.get<Budget[]>('/budgets', {
      params: { month, year },
    });
    return response.data;
  },

  async create(data: CreateBudgetRequest): Promise<Budget> {
    const response = await api.post<Budget>('/budgets', data);
    return response.data;
  },

  async update(id: number, monthlyLimit: number): Promise<Budget> {
    const response = await api.put<Budget>(`/budgets/${id}`, { monthlyLimit });
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/budgets/${id}`);
  },
};

export const analyticsService = {
  async getDashboard(): Promise<DashboardSummary> {
    const response = await api.get<DashboardSummary>('/analytics/dashboard');
    return response.data;
  },

  async getForecast(): Promise<SpendingForecast> {
    const response = await api.get<SpendingForecast>('/analytics/forecast');
    return response.data;
  },

  async getAnalysis(): Promise<any> {
    const response = await api.get('/analytics/analysis');
    return response.data;
  },
};

export const aiService = {
  async getAdvice(summary: SpendingSummary): Promise<AiAdvice> {
    const response = await api.post<AiAdvice>('/ai/advice', summary);
    return response.data;
  },

  async chat(message: string, context?: any): Promise<AiChatResponse> {
    const response = await api.post<AiChatResponse>('/ai/chat', { message, context });
    return response.data;
  },

  async getPatterns(): Promise<any> {
    const response = await api.get('/ai/patterns');
    return response.data;
  },
};
