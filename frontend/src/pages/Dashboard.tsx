import React, { useEffect, useState } from 'react';
import { analyticsService, transactionService } from '../services/financeService';
import { DashboardSummary } from '../types';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from 'recharts';
import { formatCurrency, CHART_COLORS } from '../utils';
import { PlusIcon, XMarkIcon, BanknotesIcon, ArrowTrendingUpIcon } from '@heroicons/react/24/outline';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { LoadingSpinner } from '../components/ui';

const incomeSchema = Yup.object().shape({
  description: Yup.string().required('Description is required'),
  amount: Yup.number().positive('Amount must be positive').required('Amount is required'),
});

const expenseSchema = Yup.object().shape({
  description: Yup.string().required('Description is required'),
  amount: Yup.number().positive('Amount must be positive').required('Amount is required'),
});

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showIncomeModal, setShowIncomeModal] = useState(false);
  const [showExpenseModal, setShowExpenseModal] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      setLoading(true);
      const data = await analyticsService.getDashboard();
      setSummary(data);
    } catch (err) {
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const handleAddIncome = async (values: { description: string; amount: number }, { resetForm }: any) => {
    try {
      setSubmitting(true);
      await transactionService.create({
        description: values.description,
        amount: values.amount,
        type: 'INCOME',
        transactionDate: new Date().toISOString(),
      });
      resetForm();
      setShowIncomeModal(false);
      await loadDashboard();
    } catch (err) {
      console.error('Failed to add income', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleAddExpense = async (values: { description: string; amount: number }, { resetForm }: any) => {
    try {
      setSubmitting(true);
      await transactionService.create({
        description: values.description,
        amount: values.amount,
        type: 'EXPENSE',
        transactionDate: new Date().toISOString(),
      });
      resetForm();
      setShowExpenseModal(false);
      await loadDashboard();
    } catch (err) {
      console.error('Failed to add expense', err);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 p-4 rounded-lg">
        {error}
      </div>
    );
  }

  const pieChartData = summary?.spendingByCategory
    ? Object.entries(summary.spendingByCategory).map(([name, value]) => ({
        name,
        value,
      }))
    : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
          <p className="text-gray-600 dark:text-gray-400">Welcome back! Here's your financial overview.</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowIncomeModal(true)}
            className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <ArrowTrendingUpIcon className="h-5 w-5 mr-2" />
            Add Income
          </button>
          <button
            onClick={() => setShowExpenseModal(true)}
            className="flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            <BanknotesIcon className="h-5 w-5 mr-2" />
            Add Expense
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Balance</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">
            {formatCurrency(summary?.totalBalance || 0)}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Income</p>
          <p className="text-3xl font-bold text-green-600 dark:text-green-400 mt-2">
            +{formatCurrency(summary?.monthlyIncome || 0)}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Expenses</p>
          <p className="text-3xl font-bold text-red-600 dark:text-red-400 mt-2">
            -{formatCurrency(summary?.monthlyExpenses || 0)}
          </p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Monthly Savings</p>
          <p className={`text-3xl font-bold mt-2 ${
            (summary?.monthlySavings || 0) >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
          }`}>
            {formatCurrency(summary?.monthlySavings || 0)}
          </p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Spending by Category */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Spending by Category</h2>
          {pieChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieChartData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {pieChartData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: number) => formatCurrency(value)} />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
              No spending data available
            </div>
          )}
        </div>

        {/* Recent Transactions */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Recent Transactions</h2>
          <div className="space-y-3">
            {summary?.recentTransactions && summary.recentTransactions.length > 0 ? (
              summary.recentTransactions.slice(0, 6).map((transaction) => (
                <div
                  key={transaction.id}
                  className="flex items-center justify-between py-2 border-b border-gray-100 dark:border-gray-700 last:border-0"
                >
                  <div>
                    <p className="font-medium text-gray-900 dark:text-white">{transaction.description}</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {transaction.category || 'Uncategorized'} • {new Date(transaction.transactionDate).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </p>
                  </div>
                  <p className={`font-semibold ${
                    transaction.type === 'INCOME' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                  }`}>
                    {transaction.type === 'INCOME' ? '+' : '-'}
                    {formatCurrency(transaction.amount)}
                  </p>
                </div>
              ))
            ) : (
              <div className="text-center text-gray-500 dark:text-gray-400 py-8">
                No transactions yet. Add your first transaction!
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Add Income Modal */}
      {showIncomeModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-md w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <ArrowTrendingUpIcon className="h-5 w-5 mr-2 text-green-600" />
                Add Income
              </h2>
              <button
                onClick={() => setShowIncomeModal(false)}
                className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                <XMarkIcon className="h-5 w-5" />
              </button>
            </div>

            <Formik
              initialValues={{ description: '', amount: 0 }}
              validationSchema={incomeSchema}
              onSubmit={handleAddIncome}
            >
              {({ errors, touched, isSubmitting }) => (
                <Form className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Description
                    </label>
                    <Field
                      name="description"
                      type="text"
                      placeholder="e.g., Salary, Freelance payment"
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                    {errors.description && touched.description && (
                      <p className="text-sm text-red-600 dark:text-red-400 mt-1">{errors.description}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Amount
                    </label>
                    <Field
                      name="amount"
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="0.00"
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                    {errors.amount && touched.amount && (
                      <p className="text-sm text-red-600 dark:text-red-400 mt-1">{errors.amount}</p>
                    )}
                  </div>

                  <div className="flex gap-3 pt-2">
                    <button
                      type="button"
                      onClick={() => setShowIncomeModal(false)}
                      className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={isSubmitting || submitting}
                      className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
                    >
                      {isSubmitting || submitting ? (
                        <span className="flex items-center justify-center">
                          <LoadingSpinner size="sm" />
                          <span className="ml-2">Adding...</span>
                        </span>
                      ) : (
                        'Add Income'
                      )}
                    </button>
                  </div>
                </Form>
              )}
            </Formik>
          </div>
        </div>
      )}

      {/* Add Expense Modal */}
      {showExpenseModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-xl max-w-md w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
                <BanknotesIcon className="h-5 w-5 mr-2 text-red-600" />
                Add Expense
              </h2>
              <button
                onClick={() => setShowExpenseModal(false)}
                className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                <XMarkIcon className="h-5 w-5" />
              </button>
            </div>

            <Formik
              initialValues={{ description: '', amount: 0 }}
              validationSchema={expenseSchema}
              onSubmit={handleAddExpense}
            >
              {({ errors, touched, isSubmitting }) => (
                <Form className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Description
                    </label>
                    <Field
                      name="description"
                      type="text"
                      placeholder="e.g., Groceries, Uber ride"
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-red-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                    {errors.description && touched.description && (
                      <p className="text-sm text-red-600 dark:text-red-400 mt-1">{errors.description}</p>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Amount
                    </label>
                    <Field
                      name="amount"
                      type="number"
                      step="0.01"
                      min="0"
                      placeholder="0.00"
                      className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-red-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    />
                    {errors.amount && touched.amount && (
                      <p className="text-sm text-red-600 dark:text-red-400 mt-1">{errors.amount}</p>
                    )}
                  </div>

                  <div className="flex gap-3 pt-2">
                    <button
                      type="button"
                      onClick={() => setShowExpenseModal(false)}
                      className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={isSubmitting || submitting}
                      className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors"
                    >
                      {isSubmitting || submitting ? (
                        <span className="flex items-center justify-center">
                          <LoadingSpinner size="sm" />
                          <span className="ml-2">Adding...</span>
                        </span>
                      ) : (
                        'Add Expense'
                      )}
                    </button>
                  </div>
                </Form>
              )}
            </Formik>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
