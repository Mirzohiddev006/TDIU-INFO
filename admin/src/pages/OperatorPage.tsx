import { useState } from 'react';
import toast from 'react-hot-toast';
import { useChats, useMessages, useReply, useCloseChat } from '@/features/operator/api';
import { Button, Card, Input } from '@/shared/ui';

export function OperatorPage() {
  const [sel, setSel] = useState<number | null>(null);
  const [text, setText] = useState('');
  const { data: chats } = useChats('open');
  const { data: messages } = useMessages(sel);
  const reply = useReply();
  const closeChat = useCloseChat();

  const send = () => {
    if (sel == null || !text.trim()) return;
    reply.mutate({ chatId: sel, text }, {
      onSuccess: () => setText(''),
      onError: () => toast.error('Yuborib bo\'lmadi'),
    });
  };

  return (
    <div>
      <h2 className="mb-6 text-2xl font-bold">Operator — jonli yordam</h2>
      <div className="flex gap-4" style={{ height: '70vh' }}>
        <Card className="w-72 shrink-0 overflow-y-auto p-2">
          <p className="px-2 py-1 text-xs font-semibold text-slate-400">OCHIQ SUHBATLAR ({chats?.length ?? 0})</p>
          {chats?.length ? chats.map((c) => (
            <button key={c.id} onClick={() => setSel(c.id)}
              className={`block w-full rounded-lg px-3 py-2 text-left text-sm ${sel === c.id ? 'bg-blue-50 text-blue-700' : 'hover:bg-slate-100'}`}>
              <div className="font-medium">{c.name || c.username || c.user_id}</div>
              <div className="truncate text-xs text-slate-400">{c.last_message || '—'}</div>
            </button>
          )) : <p className="px-2 py-4 text-sm text-slate-400">Ochiq suhbat yo'q.</p>}
        </Card>

        <Card className="flex flex-1 flex-col p-4">
          {sel == null ? (
            <div className="flex flex-1 items-center justify-center text-slate-400">Suhbatni tanlang</div>
          ) : (
            <>
              <div className="mb-2 flex justify-end">
                <Button variant="outline" size="sm" onClick={() => closeChat.mutate(sel, { onSuccess: () => { toast.success('Yopildi'); setSel(null); } })}>Suhbatni yopish</Button>
              </div>
              <div className="flex-1 space-y-2 overflow-y-auto rounded-lg bg-slate-50 p-3">
                {messages?.map((m) => (
                  <div key={m.id} className={`flex ${m.sender === 'operator' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[75%] rounded-2xl px-3 py-2 text-sm ${m.sender === 'operator' ? 'bg-blue-600 text-white' : 'bg-white border border-slate-200'}`}>{m.text}</div>
                  </div>
                ))}
                {!messages?.length && <p className="text-center text-sm text-slate-400">Xabarlar yo'q</p>}
              </div>
              <div className="mt-3 flex gap-2">
                <Input value={text} onChange={(e) => setText(e.target.value)} placeholder="Javob yozing..."
                  onKeyDown={(e) => e.key === 'Enter' && send()} />
                <Button onClick={send} disabled={reply.isPending}>Yuborish</Button>
              </div>
            </>
          )}
        </Card>
      </div>
    </div>
  );
}
