import axios from 'axios';
import { env } from '@/shared/config/env';
import { useAuth } from '@/store/auth';

export const api = axios.create({ baseURL: env.apiUrl });

api.interceptors.request.use((config) => {
  const token = useAuth.getState().token;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (error) => {
    if (error?.response?.status === 401) {
      useAuth.getState().logout();
    }
    return Promise.reject(error);
  },
);
