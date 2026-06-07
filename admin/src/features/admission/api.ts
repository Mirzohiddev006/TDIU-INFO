import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/client';
import type { ProgramAdmission } from '@/shared/api/types';

export function useOverview() {
  return useQuery({ queryKey: ['admission-overview'], queryFn: async () => (await api.get<ProgramAdmission[]>('/admission/overview')).data });
}
export function useSetScores() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ programId, data }: { programId: number; data: Record<string, number | null> }) =>
      (await api.put(`/admission/${programId}/scores`, data)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admission-overview'] }),
  });
}
export function useSetContract() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ programId, data }: { programId: number; data: { form: string; amount: number | null } }) =>
      (await api.put(`/admission/${programId}/contract`, data)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admission-overview'] }),
  });
}
