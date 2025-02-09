
// src/contexts/AuthContext.jsx
import React, { createContext, useContext, useState } from 'react';
import { api } from '../utils/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const login = async (credentials) => {
    try {
      const response = await api.post('/login', credentials);
      setUser(response.data.user);
      setIsAuthenticated(true);
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  const logout = async () => {
    try {
      await api.get('/logout');
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      throw error;
    }
  };

  const register = async (userData) => {
    try {
      const response = await api.post('/register', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
