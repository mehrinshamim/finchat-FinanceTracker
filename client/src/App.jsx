// src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from '@/components/ui/toaster';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/DashBoard';
import Profile from './pages/Profile';
import Transactions from './pages/Transactions';
import LentMoney from './pages/LentMoney';
import BudgetReport from './pages/BudgetReport';
import Categories from './pages/Categories';

const PrivateRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/" element={
                <PrivateRoute>
                  <Dashboard />
                </PrivateRoute>
              } />
              <Route path="/profile" element={
                <PrivateRoute>
                  <Profile />
                </PrivateRoute>
              } />
              <Route path="/transactions" element={
                <PrivateRoute>
                  <Transactions />
                </PrivateRoute>
              } />
              <Route path="/lent-money" element={
                <PrivateRoute>
                  <LentMoney />
                </PrivateRoute>
              } />
              <Route path="/budget-report" element={
                <PrivateRoute>
                  <BudgetReport />
                </PrivateRoute>
              } />
              <Route path="/categories" element={
                <PrivateRoute>
                  <Categories />
                </PrivateRoute>
              } />
            </Routes>
          </main>
          <Toaster />
        </div>
      </Router>
    </AuthProvider>
  );
};

export default App;