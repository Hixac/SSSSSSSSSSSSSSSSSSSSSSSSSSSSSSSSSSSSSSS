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
  signup: (name: string, email: string, password: string) => Promise<void>;
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
      // After successful login, we could re-fetch user info
      // or rely on the cookie for subsequent requests.
      // To update the UI, we need the user data. If the login endpoint
      // returns user info, use it. Otherwise, call /auth/me again.
      if (response.data.user) {
        setUser(response.data.user);
      } else {
        // Optionally fetch user info
        const userResponse = await api.get('/auth/me');
        setUser(userResponse.data);
      }
    } catch (error) {
      // Handle error (re-throw with a message)
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

  const signup = async () => {
    try {
      await api.post('/auth/register')
      const userResponse = await api.get('/auth/me');
      setUser(userResponse.data)
      console.log(userResponse.data)
    } catch (error) {
      console.error('Signup error', error)
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
