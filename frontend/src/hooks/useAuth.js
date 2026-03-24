import { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const register = async (userData) => {
    const response = await authAPI.register(userData);
    if (response.success) {
    }
    return response;
  };

  const login = async (email, password) => {
    const response = await authAPI.login(email, password);
    if (response.success) {
      setIsAuthenticated(true);
    }
    return response;
  };

  const logout = async () => {
    await authAPI.logout();
    setIsAuthenticated(false);
    setUser(null);
  };

  return {
    user,
    loading,
    isAuthenticated,
    register,
    login,
    logout
  };
}