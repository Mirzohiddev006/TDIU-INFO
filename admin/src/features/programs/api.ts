import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import type { Program } from '@/shared/api/types';

export function usePrograms(facultyId?: number) {
  return useQuery({
    queryKey: ['programs', facultyId ?? 'all'],
    queryFn: async () => (await api.get<Program[]>('/programs', { params: facultyId ? { faculty_id: facultyId } : {} })).data,
  });
}
export function useSaveProgram() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (p: Partial<Program> & { faculty_id: number; code: string; name: string }) =>
      p.id ? (await api.put(`/programs/${p.id}`, p)).data : (await api.post('/programs', p)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['programs'] }),
  });
}
export function useDeleteProgram() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => (await api.delete(`/programs/${id}`)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['programs'] }),
  });
}
