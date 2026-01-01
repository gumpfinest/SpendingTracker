import React from 'react';

/**
 * Shared UI component class names for consistent styling.
 */

// Form input styles
export const inputClasses = 
  'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 transition-colors';

// Primary button styles
export const primaryButtonClasses = 
  'px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed';

// Secondary/outline button styles
export const secondaryButtonClasses = 
  'px-4 py-2 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors';

// Danger button styles
export const dangerButtonClasses = 
  'px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50';

// Card container styles
export const cardClasses = 
  'bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 border border-gray-100 dark:border-gray-700';

// Form label styles
export const labelClasses = 
  'block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1';

// Error message styles
export const errorClasses = 
  'text-sm text-red-600 dark:text-red-400 mt-1';

// Page header styles
export const pageHeaderClasses = 
  'text-3xl font-bold text-gray-900 dark:text-white';

// Page subtitle styles
export const pageSubtitleClasses = 
  'text-gray-600 dark:text-gray-400';

// Loading spinner component
export const LoadingSpinner: React.FC<{ size?: 'sm' | 'md' | 'lg' }> = ({ size = 'md' }) => {
  const sizeClasses = {
    sm: 'h-6 w-6',
    md: 'h-12 w-12',
    lg: 'h-16 w-16',
  };
  
  return (
    <div className="flex items-center justify-center">
      <div className={`animate-spin rounded-full border-b-2 border-primary-600 ${sizeClasses[size]}`}></div>
    </div>
  );
};

// Error alert component
export const ErrorAlert: React.FC<{ message: string }> = ({ message }) => (
  <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 p-4 rounded-lg">
    {message}
  </div>
);
