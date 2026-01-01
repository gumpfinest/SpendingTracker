import React, { useEffect, useState } from 'react';
import { analyticsService, aiService } from '../services/financeService';
import { DashboardSummary, SpendingForecast, AiAdvice } from '../types';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  Legend,
  AreaChart,
  Area,
} from 'recharts';
import { LightBulbIcon, ArrowTrendingUpIcon, ChartBarIcon } from '@heroicons/react/24/outline';
import { formatCurrency } from '../utils';
import { LoadingSpinner } from '../components/ui';

const Analytics: React.FC = () => {
  const [dashboard, setDashboard] = useState<DashboardSummary | null>(null);
  const [forecast, setForecast] = useState<SpendingForecast | null>(null);
  const [advice, setAdvice] = useState<AiAdvice | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState<'week' | 'month' | 'year'>('month');

  useEffect(() => {
    loadAnalytics();
  }, [selectedPeriod]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const [dashboardData, forecastData] = await Promise.all([
        analyticsService.getDashboard(),
        analyticsService.getForecast(),
      ]);
      setDashboard(dashboardData);
      setForecast(forecastData);

      // Load AI advice
      try {
        const adviceData = await aiService.getAdvice({
          totalIncome: dashboardData.monthlyIncome,
          totalExpenses: dashboardData.monthlyExpenses,
          categoryBreakdown: dashboardData.spendingByCategory,
        });
        setAdvice(adviceData);
      } catch (err) {
        console.error('Failed to load AI advice', err);
      }
    } catch (err) {
      console.error('Failed to load analytics', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Prepare chart data
  const categoryData = dashboard?.spendingByCategory
    ? Object.entries(dashboard.spendingByCategory).map(([name, value]) => ({
        name,
        amount: value,
      }))
    : [];

  const forecastChartData = forecast?.forecasts || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Analytics</h1>
          <p className="text-gray-600 dark:text-gray-400">Deep insights into your spending patterns</p>
        </div>
        <div className="flex space-x-2">
          {(['week', 'month', 'year'] as const).map((period) => (
            <button
              key={period}
              onClick={() => setSelectedPeriod(period)}
              className={`px-4 py-2 rounded-lg capitalize ${
                selectedPeriod === period
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              {period}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Total Income</p>
          <p className="text-2xl font-bold text-green-600 dark:text-green-400">
            {formatCurrency(dashboard?.monthlyIncome || 0)}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Total Expenses</p>
          <p className="text-2xl font-bold text-red-600 dark:text-red-400">
            {formatCurrency(dashboard?.monthlyExpenses || 0)}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Net Savings</p>
          <p className={`text-2xl font-bold ${
            (dashboard?.monthlyIncome || 0) - (dashboard?.monthlyExpenses || 0) >= 0
              ? 'text-green-600 dark:text-green-400'
              : 'text-red-600 dark:text-red-400'
          }`}>
            {formatCurrency((dashboard?.monthlyIncome || 0) - (dashboard?.monthlyExpenses || 0))}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Savings Rate</p>
          <p className="text-2xl font-bold text-primary-600 dark:text-primary-400">
            {dashboard?.monthlyIncome
              ? (((dashboard.monthlyIncome - dashboard.monthlyExpenses) / dashboard.monthlyIncome) * 100).toFixed(1)
              : 0}%
          </p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Category Breakdown */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <div className="flex items-center mb-4">
            <ChartBarIcon className="h-5 w-5 text-primary-600 dark:text-primary-400 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Spending by Category</h2>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={categoryData} layout="horizontal">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fontSize: 12 }} angle={-45} textAnchor="end" height={80} />
              <YAxis tickFormatter={(v) => `$${v}`} />
              <Tooltip formatter={(value: number) => formatCurrency(value)} />
              <Bar dataKey="amount" fill="#059669" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Spending Forecast */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <div className="flex items-center mb-4">
            <ArrowTrendingUpIcon className="h-5 w-5 text-primary-600 dark:text-primary-400 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Spending Forecast</h2>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={forecastChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis tickFormatter={(v) => `$${v}`} />
              <Tooltip formatter={(value: number) => formatCurrency(value)} />
              <Legend />
              <Area
                type="monotone"
                dataKey="predicted_spending"
                name="Predicted Spending"
                stroke="#059669"
                fill="#d1fae5"
                strokeWidth={2}
              />
              <Area
                type="monotone"
                dataKey="predicted_income"
                name="Predicted Income"
                stroke="#3b82f6"
                fill="#dbeafe"
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* AI Insights */}
      {advice && (
        <div className="bg-gradient-to-r from-primary-50 to-emerald-50 dark:from-primary-900/30 dark:to-emerald-900/30 rounded-xl shadow-sm p-6 border border-primary-100 dark:border-primary-800">
          <div className="flex items-center mb-4">
            <LightBulbIcon className="h-6 w-6 text-primary-600 dark:text-primary-400 mr-2" />
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">AI-Powered Insights</h2>
          </div>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium text-gray-800 dark:text-gray-200 mb-2">Summary</h3>
              <p className="text-gray-600 dark:text-gray-400">{advice.summary}</p>
            </div>
            <div>
              <h3 className="font-medium text-gray-800 dark:text-gray-200 mb-2">Recommendations</h3>
              <ul className="space-y-2">
                {advice.recommendations.map((rec, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="w-6 h-6 bg-primary-600 text-white rounded-full flex items-center justify-center text-sm mr-3 mt-0.5 flex-shrink-0">
                      {idx + 1}
                    </span>
                    <span className="text-gray-600 dark:text-gray-400">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
            {advice.savingsOpportunities && advice.savingsOpportunities.length > 0 && (
              <div>
                <h3 className="font-medium text-gray-800 dark:text-gray-200 mb-2">Savings Opportunities</h3>
                <div className="flex flex-wrap gap-2">
                  {advice.savingsOpportunities.map((opp, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-full text-sm"
                    >
                      {opp}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Monthly Trend */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Income vs Expenses Trend</h2>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={forecastChartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis tickFormatter={(v) => `$${v}`} />
            <Tooltip formatter={(value: number) => formatCurrency(value)} />
            <Legend />
            <Line
              type="monotone"
              dataKey="predicted_spending"
              name="Expenses"
              stroke="#ef4444"
              strokeWidth={2}
              dot={{ r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="predicted_income"
              name="Income"
              stroke="#059669"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={{ r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Analytics;
