import { useState, useEffect } from 'react';
import { authAPI } from '../services/api';

export function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        const response = await authAPI.getCurrentUser();
        if (response.success) {
          setUser(response.data);
          setIsAuthenticated(true);
        } else {
          localStorage.removeItem('accessToken');
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const register = async (userData) => {
    const response = await authAPI.register(userData);
    return response;
  };

  const login = async (email, password) => {
    const response = await authAPI.login(email, password);
    if (response.success) {
      setIsAuthenticated(true);
      const userResponse = await authAPI.getCurrentUser();
      if (userResponse.success) {
        setUser(userResponse.data);
      }
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