import axios from 'axios';
import { apiUrl } from '@/env';
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IBot,
  IStrategy,
  IBotCreate,
  IBotUpdate,
  IAccount,
} from './interfaces';
import { commitCreateBot } from './store/main/mutations';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(
      `${apiUrl}/api/v1/users/me`,
      authHeaders(token),
    );
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(
      `${apiUrl}/api/v1/users/me`,
      data,
      authHeaders(token),
    );
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(
      `${apiUrl}/api/v1/users/`,
      authHeaders(token),
    );
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(
      `${apiUrl}/api/v1/users/${userId}`,
      data,
      authHeaders(token),
    );
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async getBots(token: string) {
    return axios.get<IBot[]>(`${apiUrl}/api/v1/bots/`, authHeaders(token));
  },
  async deleteBot(id: number, token: string) {
    return axios.delete<IBot>(
      `${apiUrl}/api/v1/bots/${id}/`,
      authHeaders(token),
    );
  },
  async createBot(token: string, data: IBotCreate) {
    return axios.post<IBot>(`${apiUrl}/api/v1/bots/`, data, authHeaders(token));
  },
  async updateBot(token: string, data: IBotUpdate) {
    return axios.put<IBot>(
      `${apiUrl}/api/v1/bots/${data.id}/`,
      data,
      authHeaders(token),
    );
  },
  async getStrategies(token: string) {
    return axios.get<IStrategy[]>(
      `${apiUrl}/api/v1/strategies/`,
      authHeaders(token),
    );
  },
  async getAccounts(token: string) {
    return axios.get<IAccount[]>(
      `${apiUrl}/api/v1/accounts/`,
      authHeaders(token),
    );
  },
};
