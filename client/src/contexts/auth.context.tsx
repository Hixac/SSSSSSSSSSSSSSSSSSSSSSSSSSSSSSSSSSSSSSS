import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { loginRequest, logoutRequest, meRequest, registerRequest } from '../api/auth';
import type { User } from '../types';

type AuthStatus = 'loading' | 'authenticated' | 'unauthenticated';

interface AuthContextType {
  user: User | null;
  status: AuthStatus;
  login: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [status, setStatus] = useState<AuthStatus>('loading');

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const currentUser = await meRequest();
        if (!cancelled) {
          setUser(currentUser);
          setStatus('authenticated');
        }
      } catch {
        if (!cancelled) {
          setUser(null);
          setStatus('unauthenticated');
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const login = async (email: string, password: string) => {
    await loginRequest(email, password);
    setUser({ email });
    setStatus('authenticated');
  };

  const signup = async (email: string, password: string) => {
    await registerRequest(email, password);
    setUser({ email });
    setStatus('authenticated');
  };

  const logout = async () => {
    try {
      await logoutRequest();
    } catch {
      // Session may already be invalid — clear local state anyway.
    }
    setUser(null);
    setStatus('unauthenticated');
  };

  return (
    <AuthContext.Provider value={{ user, status, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
