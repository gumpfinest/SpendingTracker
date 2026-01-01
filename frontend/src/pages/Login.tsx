import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline';
import { inputClasses, primaryButtonClasses, labelClasses, errorClasses } from '../components/ui';

const loginSchema = Yup.object().shape({
  username: Yup.string().required('Username is required'),
  password: Yup.string().required('Password is required'),
});

const Login: React.FC = () => {
  const { login } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (values: { username: string; password: string }) => {
    try {
      setError(null);
      await login(values.username, values.password);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Invalid username or password');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-500 to-primary-700 dark:from-gray-900 dark:to-gray-800 py-12 px-4 sm:px-6 lg:px-8 transition-colors">
      {/* Theme toggle button */}
      <button
        onClick={toggleTheme}
        className="absolute top-4 right-4 p-2 rounded-lg bg-white/20 hover:bg-white/30 dark:bg-gray-800/50 dark:hover:bg-gray-800/70 text-white transition-colors"
        title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
      >
        {theme === 'dark' ? <SunIcon className="h-6 w-6" /> : <MoonIcon className="h-6 w-6" />}
      </button>

      <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 transition-colors">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">💰 SmartSpend</h1>
          <p className="text-gray-600 dark:text-gray-400">Your AI-Powered Finance Assistant</p>
        </div>

        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">Welcome back</h2>

        {error && (
          <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 rounded-lg text-sm">
            {error}
          </div>
        )}

        <Formik
          initialValues={{ username: '', password: '' }}
          validationSchema={loginSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form className="space-y-4">
              <div>
                <label htmlFor="username" className={labelClasses}>Username</label>
                <Field type="text" name="username" className={inputClasses} placeholder="Enter your username" />
                <ErrorMessage name="username" component="p" className={errorClasses} />
              </div>

              <div>
                <label htmlFor="password" className={labelClasses}>Password</label>
                <Field type="password" name="password" className={inputClasses} placeholder="••••••••" />
                <ErrorMessage name="password" component="p" className={errorClasses} />
              </div>

              <button type="submit" disabled={isSubmitting} className={`w-full py-3 ${primaryButtonClasses}`}>
                {isSubmitting ? 'Signing in...' : 'Sign in'}
              </button>
            </Form>
          )}
        </Formik>

        <p className="mt-6 text-center text-gray-600 dark:text-gray-400">
          Don't have an account?{' '}
          <Link to="/register" className="text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300 font-medium">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
