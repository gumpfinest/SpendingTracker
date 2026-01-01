import React, { useEffect, useState } from 'react';
import { Formik, Form, Field } from 'formik';
import * as Yup from 'yup';
import { budgetService } from '../services/financeService';
import { Budget, CreateBudgetRequest } from '../types';
import { PlusIcon, TrashIcon } from '@heroicons/react/24/outline';
import { formatCurrency } from '../utils';
import { LoadingSpinner, inputClasses } from '../components/ui';

const CATEGORIES = [
  'Food & Dining',
  'Groceries',
  'Transportation',
  'Shopping',
  'Entertainment',
  'Bills & Utilities',
  'Healthcare',
  'Personal Care',
  'Education',
  'Travel',
  'Subscriptions',
  'Other',
];

const budgetSchema = Yup.object().shape({
  category: Yup.string().required('Category is required'),
  monthlyLimit: Yup.number().positive('Limit must be positive').required('Limit is required'),
});

const Budgets: React.FC = () => {
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  const currentMonth = new Date().getMonth() + 1;
  const currentYear = new Date().getFullYear();

  useEffect(() => {
    loadBudgets();
  }, []);

  const loadBudgets = async () => {
    try {
      setLoading(true);
      const data = await budgetService.getByMonth(currentMonth, currentYear);
      setBudgets(data);
    } catch (err) {
      console.error('Failed to load budgets', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (
    values: { category: string; monthlyLimit: number },
    { resetForm }: any
  ) => {
    try {
      const request: CreateBudgetRequest = {
        ...values,
        month: currentMonth,
        year: currentYear,
      };
      await budgetService.create(request);
      resetForm();
      setShowForm(false);
      loadBudgets();
    } catch (err) {
      console.error('Failed to create budget', err);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this budget?')) {
      try {
        await budgetService.delete(id);
        loadBudgets();
      } catch (err) {
        console.error('Failed to delete budget', err);
      }
    }
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 100) return 'bg-red-500';
    if (percentage >= 80) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Budgets</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Set and track spending limits for {new Date().toLocaleString('default', { month: 'long' })} {currentYear}
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <PlusIcon className="h-5 w-5 mr-2" />
          Add Budget
        </button>
      </div>

      {/* Add Budget Form */}
      {showForm && (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">New Budget</h2>
          <Formik
            initialValues={{ category: '', monthlyLimit: 0 }}
            validationSchema={budgetSchema}
            onSubmit={handleSubmit}
          >
            {({ errors, touched, isSubmitting }) => (
              <Form className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Category
                  </label>
                  <Field
                    as="select"
                    name="category"
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  >
                    <option value="">Select category</option>
                    {CATEGORIES.map((cat) => (
                      <option key={cat} value={cat}>
                        {cat}
                      </option>
                    ))}
                  </Field>
                  {errors.category && touched.category && (
                    <p className="text-sm text-red-600 dark:text-red-400 mt-1">{errors.category}</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Monthly Limit
                  </label>
                  <Field
                    name="monthlyLimit"
                    type="number"
                    step="1"
                    className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    placeholder="500"
                  />
                  {errors.monthlyLimit && touched.monthlyLimit && (
                    <p className="text-sm text-red-600 dark:text-red-400 mt-1">{errors.monthlyLimit}</p>
                  )}
                </div>

                <div className="flex items-end">
                  <button
                    type="submit"
                    disabled={isSubmitting}
                    className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
                  >
                    {isSubmitting ? 'Creating...' : 'Create Budget'}
                  </button>
                </div>
              </Form>
            )}
          </Formik>
        </div>
      )}

      {/* Budgets Grid */}
      {loading ? (
        <div className="flex items-center justify-center h-64">
          <LoadingSpinner size="lg" />
        </div>
      ) : budgets.length === 0 ? (
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-12 border border-gray-100 dark:border-gray-700 text-center">
          <p className="text-gray-500 dark:text-gray-400">No budgets set for this month. Create one to start tracking!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {budgets.map((budget) => (
            <div
              key={budget.id}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white">{budget.category}</h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {formatCurrency(budget.currentSpent)} of {formatCurrency(budget.monthlyLimit)}
                  </p>
                </div>
                <button
                  onClick={() => handleDelete(budget.id)}
                  className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                >
                  <TrashIcon className="h-5 w-5" />
                </button>
              </div>

              {/* Progress Bar */}
              <div className="mb-3">
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${getProgressColor(budget.percentageUsed)} transition-all`}
                    style={{ width: `${Math.min(budget.percentageUsed, 100)}%` }}
                  />
                </div>
              </div>

              <div className="flex justify-between text-sm">
                <span className={`font-medium ${
                  budget.percentageUsed >= 100 ? 'text-red-600 dark:text-red-400' : 'text-gray-600 dark:text-gray-400'
                }`}>
                  {budget.percentageUsed.toFixed(0)}% used
                </span>
                <span className={`font-medium ${
                  budget.remaining >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'
                }`}>
                  {formatCurrency(Math.abs(budget.remaining))} {budget.remaining >= 0 ? 'left' : 'over'}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Budgets;
