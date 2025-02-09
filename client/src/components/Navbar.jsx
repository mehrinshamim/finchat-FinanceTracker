import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/Button';

const Navbar = () => {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  if (!isAuthenticated) return null;

  return (
    <nav className="bg-white shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold">
            FinChat
          </Link>
          
          <div className="flex space-x-4">
            <Link to="/" className="text-gray-700 hover:text-gray-900">
              Dashboard
            </Link>
            <Link to="/transactions" className="text-gray-700 hover:text-gray-900">
              Transactions
            </Link>
            <Link to="/lent-money" className="text-gray-700 hover:text-gray-900">
              Lent Money
            </Link>
            <Link to="/budget-report" className="text-gray-700 hover:text-gray-900">
              Budget
            </Link>
            <Link to="/categories" className="text-gray-700 hover:text-gray-900">
              Categories
            </Link>
            <Link to="/profile" className="text-gray-700 hover:text-gray-900">
              Profile
            </Link>
            <Button variant="ghost" onClick={handleLogout}>
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;