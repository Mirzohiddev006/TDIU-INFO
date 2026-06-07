import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import type { Faculty } from '@/shared/api/types';

export function useFaculties() {
  return useQuery({ queryKey: ['faculties'], queryFn: async () => (await api.get<Faculty[]>('/faculties')).data });
}
export function useSaveFaculty() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (f: Partial<Faculty> & { name: string }) =>
      f.id ? (await api.put(`/faculties/${f.id}`, f)).data : (await api.post('/faculties', f)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['faculties'] }),
  });
}
export function useDeleteFaculty() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: number) => (await api.delete(`/faculties/${id}`)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['faculties'] }),
  });
}
