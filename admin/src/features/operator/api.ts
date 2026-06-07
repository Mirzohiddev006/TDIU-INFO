import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '@/shared/api/client';

export interface OpChat { id: number; user_id: number; status: string; name: string | null; username: string | null; last_message: string | null; }
export interface OpMessage { id: number; sender: string; text: string; }

export function useChats(status: string = 'open') {
  return useQuery({
    queryKey: ['op-chats', status],
    queryFn: async () => (await api.get<OpChat[]>('/operator/chats', { params: { status } })).data,
    refetchInterval: 10000,
  });
}
export function useMessages(chatId: number | null) {
  return useQuery({
    queryKey: ['op-messages', chatId],
    enabled: chatId != null,
    queryFn: async () => (await api.get<OpMessage[]>(`/operator/chats/${chatId}/messages`)).data,
    refetchInterval: 5000,
  });
}
export function useReply() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ chatId, text }: { chatId: number; text: string }) =>
      (await api.post(`/operator/chats/${chatId}/reply`, { text })).data,
    onSuccess: (_d, v) => qc.invalidateQueries({ queryKey: ['op-messages', v.chatId] }),
  });
}
export function useCloseChat() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (chatId: number) => (await api.post(`/operator/chats/${chatId}/close`, {})).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['op-chats'] }),
  });
}
