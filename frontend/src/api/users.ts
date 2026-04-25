import client from './client';
import type { User } from './auth';

export interface UserListResponse {
  users: User[];
  total: number;
}

export const listUsers = () =>
  client.get<UserListResponse>('/users/');

export const deleteUser = (userId: number) =>
  client.delete(`/users/${userId}`);
