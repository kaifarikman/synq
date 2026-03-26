import { useEffect, useRef, useState } from 'react';
import { authAPI } from '../services/api';
import { AuthContext } from './auth-context';

function normalizeError(response, fallbackDetail) {
  return {
    success: false,
    status: response?.status ?? 500,
    detail: response?.detail || fallbackDetail,
    data: response?.data ?? null,
  };
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const initializedRef = useRef(false);

  useEffect(() => {
    if (initializedRef.current) {
      return;
    }

    initializedRef.current = true;

    async function restoreSession() {
      const token = localStorage.getItem('accessToken');

      if (!token) {
        setLoading(false);
        return;
      }

      const response = await authAPI.getCurrentUser();
      if (response.success) {
        setUser(response.data);
        setIsAuthenticated(true);
      } else {
        localStorage.removeItem('accessToken');
      }

      setLoading(false);
    }

    restoreSession();
  }, []);

  const register = async (userData) => {
    const response = await authAPI.register(userData);
    if (!response.success) {
      return normalizeError(response, 'Ошибка регистрации');
    }
    return response;
  };

  const confirmEmail = async (email, code) => {
    const response = await authAPI.confirmEmail(email, code);
    if (!response.success) {
      return normalizeError(response, 'Ошибка подтверждения email');
    }
    return response;
  };

  const login = async (email, password) => {
    const response = await authAPI.login(email, password);
    if (!response.success) {
      return normalizeError(response, 'Ошибка входа');
    }

    const userResponse = await authAPI.getCurrentUser();
    if (!userResponse.success) {
      localStorage.removeItem('accessToken');
      setIsAuthenticated(false);
      setUser(null);
      return normalizeError(
        userResponse,
        'Не удалось получить данные пользователя',
      );
    }

    setUser(userResponse.data);
    setIsAuthenticated(true);

    return response;
  };

  const logout = async () => {
    await authAPI.logout();
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated,
        register,
        confirmEmail,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
