import { useMutation } from '@tanstack/react-query';
import { api } from '@/shared/api/client';

interface BroadcastResult { total: number; sent: number; failed: number; }
interface BroadcastInput { text: string; file?: File | null; }

export function useBroadcast() {
  return useMutation({
    mutationFn: async ({ text, file }: BroadcastInput) => {
      const form = new FormData();
      form.append('text', text);
      if (file) form.append('file', file);
      const { data } = await api.post<BroadcastResult>('/broadcast', form);
      return data;
    },
  });
}
