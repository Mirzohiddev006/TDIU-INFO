import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import type { Section } from '@/shared/api/types';

export function useSections() {
  return useQuery({ queryKey: ['sections'], queryFn: async () => (await api.get<Section[]>('/sections')).data });
}
export function useSaveSection() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (s: { key: string; title: string; body: string }) =>
      (await api.put(`/sections/${s.key}`, { title: s.title, body: s.body })).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['sections'] }),
  });
}
