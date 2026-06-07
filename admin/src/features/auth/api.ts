import { useMutation } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import type { Role } from '@/shared/api/types';

interface LoginResp { access_token: string; token_type: string; role: Role; username: string; }

export function useLogin() {
  return useMutation({
    mutationFn: async (data: { username: string; password: string }) => {
      const res = await api.post<LoginResp>('/auth/login', data);
      return res.data;
    },
  });
}
