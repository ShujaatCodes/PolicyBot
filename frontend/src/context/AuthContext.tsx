import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { jwtDecode } from 'jwt-decode';

export interface AuthUser {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'employee';
}

interface JWTPayload {
  sub: string;
  email: string;
  role: 'admin' | 'employee';
  name: string;
  exp: number;
}

interface AuthContextType {
  user: AuthUser | null;
  login: (token: string) => void;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      try {
        const payload = jwtDecode<JWTPayload>(token);
        if (payload.exp * 1000 > Date.now()) {
          setUser({
            id: parseInt(payload.sub),
            email: payload.email,
            role: payload.role,
            name: payload.name,
          });
        } else {
          localStorage.removeItem('access_token');
        }
      } catch {
        localStorage.removeItem('access_token');
      }
    }
    setIsLoading(false);
  }, []);

  const login = (token: string) => {
    localStorage.setItem('access_token', token);
    const payload = jwtDecode<JWTPayload>(token);
    setUser({
      id: parseInt(payload.sub),
      email: payload.email,
      role: payload.role,
      name: payload.name,
    });
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
