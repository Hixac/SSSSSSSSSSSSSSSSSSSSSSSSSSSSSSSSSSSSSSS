import { api } from './client';
import type { User } from '../types';

export async function loginRequest(
  email: string,
  password: string
): Promise<void> {
  await api.post('/auth/login', { email, password });
}

export async function registerRequest(
  email: string,
  password: string
): Promise<void> {
  await api.post('/auth/register', { email, password });
}

export async function logoutRequest(): Promise<void> {
  await api.post('/auth/logout');
}

export async function meRequest(): Promise<User> {
  const response = await api.get<User>('/auth/me');
  return response.data;
}
