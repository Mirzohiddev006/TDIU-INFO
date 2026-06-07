import { useMutation } from '@tanstack/react-query';
import { api } from '@/shared/api/client';

interface BroadcastResult { total: number; sent: number; failed: number; }

export function useBroadcast() {
  return useMutation({
    mutationFn: async (text: string) => (await api.post<BroadcastResult>('/broadcast', { text })).data,
  });
}
