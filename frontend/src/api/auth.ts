import client from './client';

export interface RegisterPayload {
  name: string;
  email: string;
  password: string;
  role: 'admin' | 'employee';
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: 'admin' | 'employee';
}

export const register = (payload: RegisterPayload) =>
  client.post<TokenResponse>('/auth/register', payload);

export const login = (payload: LoginPayload) =>
  client.post<TokenResponse>('/auth/login', payload);

export const getMe = () =>
  client.get<User>('/auth/me');
