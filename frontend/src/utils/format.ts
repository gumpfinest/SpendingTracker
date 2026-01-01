/**
 * Shared utility functions for the SmartSpend frontend.
 */

/**
 * Format a number as USD currency.
 */
export const formatCurrency = (value: number, compact = false): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: compact ? 0 : 2,
    maximumFractionDigits: compact ? 0 : 2,
  }).format(value);
};

/**
 * Format a date string for display.
 */
export const formatDate = (dateString: string, options?: Intl.DateTimeFormatOptions): string => {
  const defaultOptions: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  };
  return new Date(dateString).toLocaleDateString('en-US', options || defaultOptions);
};

/**
 * Calculate percentage with zero-division protection.
 */
export const calculatePercentage = (part: number, total: number): number => {
  return total > 0 ? (part / total) * 100 : 0;
};

/**
 * Truncate a string to a specified length with ellipsis.
 */
export const truncate = (str: string, maxLength: number): string => {
  return str.length > maxLength ? `${str.substring(0, maxLength)}...` : str;
};

/**
 * Color palette for charts.
 */
export const CHART_COLORS = [
  '#0ea5e9', // sky-500
  '#22c55e', // green-500
  '#f59e0b', // amber-500
  '#ef4444', // red-500
  '#8b5cf6', // violet-500
  '#ec4899', // pink-500
  '#14b8a6', // teal-500
  '#f97316', // orange-500
];

/**
 * Get a color from the palette by index (cycles through).
 */
export const getChartColor = (index: number): string => {
  return CHART_COLORS[index % CHART_COLORS.length];
};
