import { useQuery } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import type { Stats } from '@/shared/api/types';

export function useStats() {
  return useQuery({ queryKey: ['stats'], queryFn: async () => (await api.get<Stats>('/stats')).data });
}
