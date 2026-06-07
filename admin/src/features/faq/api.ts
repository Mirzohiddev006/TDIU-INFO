import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import type { Faq } from '@/shared/api/types';

export function useFaq() {
  return useQuery({ queryKey: ['faq'], queryFn: async () => (await api.get<Faq[]>('/faq')).data });
}
export function useSaveFaq() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (f: Partial<Faq> & { question: string; answer: string }) =>
      f.id ? (await api.put(`/faq/${f.id}`, f)).data : (await api.post('/faq', f)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['faq'] }),
  });
}
export function useDeleteFaq() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => (await api.delete(`/faq/${id}`)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['faq'] }),
  });
}
