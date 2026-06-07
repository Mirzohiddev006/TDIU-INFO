import { useState } from 'react';
import toast from 'react-hot-toast';
import { useBroadcast } from '@/features/broadcast/api';
import { useAuth, canEdit } from '@/store/auth';
import { Button, Card, Label, Textarea } from '@/shared/ui';

export function BroadcastPage() {
  const [text, setText] = useState('');
  const bc = useBroadcast();
  const editable = canEdit(useAuth((s) => s.role));

  const send = () => {
    if (!text.trim()) return;
    if (!confirm("Xabar BARCHA foydalanuvchilarga yuboriladi. Davom etamizmi?")) return;
    bc.mutate(text, {
      onSuccess: (r) => { toast.success(`Yuborildi: ${r.sent}/${r.total} (xato: ${r.failed})`); setText(''); },
      onError: () => toast.error('Yuborishda xato (bot ishlayaptimi?)'),
    });
  };

  return (
    <div className="max-w-2xl">
      <h2 className="mb-2 text-2xl font-bold">Ommaviy xabar (broadcast)</h2>
      <p className="mb-6 text-sm text-slate-500">Matn barcha bot foydalanuvchilariga yuboriladi. HTML teglar (&lt;b&gt;) qo'llab-quvvatlanadi.</p>
      <Card className="space-y-4 p-6">
        <div><Label>Xabar matni</Label><Textarea rows={6} value={text} onChange={(e) => setText(e.target.value)} placeholder="E'lon matnini yozing..." disabled={!editable} /></div>
        {editable
          ? <Button onClick={send} disabled={bc.isPending}>{bc.isPending ? 'Yuborilmoqda...' : 'Hammaga yuborish'}</Button>
          : <p className="text-sm text-slate-400">Sizda yuborish huquqi yo'q.</p>}
      </Card>
    </div>
  );
}
