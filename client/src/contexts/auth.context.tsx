import axios from 'axios';
import React, { createContext, useState, useContext, useEffect, type ReactNode } from 'react';
import api from '../api';

interface User {
  email: string;
  name: string;
  surname: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  signup: (name: string, surname: string, email: string, password: string) => Promise<void>;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check authentication status on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const response = await api.get('/auth/me');
        setUser(response.data);  // assuming response contains user info
      } catch (error) {
        // Not authenticated or error – user remains null
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };
    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await api.post('/auth/login', { email, password });
      if (response.data.user) {
        setUser(response.data.user);
      } else {
        const userResponse = await api.get('/auth/me');
        setUser(userResponse.data);
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.detail || 'Login failed');
      }
      throw new Error('Network error');
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
      setUser(null);
    } catch (error) {
      console.error('Logout error', error);
    }
  };

  const signup = async (name: string, surname: string, email: string, password: string) => {
    try {
      await api.post('/auth/register', { name, surname, email, password })
      const userResponse = await api.get('/auth/me');
      setUser(userResponse.data)
      console.log(userResponse.data)
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.detail || 'Login failed');
      }
      throw new Error('Network error');
    }
  }

  const value = {
    user,
    isAuthenticated: !!user,
    login,
    logout,
    signup,
    isLoading,
  };

  return (
    <AuthContext.Provider value={value}>
     {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
};
