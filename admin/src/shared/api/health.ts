import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import { env } from '@/shared/config/env';

export function useHealth() {
  return useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const t0 = performance.now();
      await api.get('/health', { timeout: 8000 });
      return Math.round(performance.now() - t0);
    },
    retry: false,
    refetchInterval: 30000,
  });
}

export const apiBaseUrl = env.apiUrl;
