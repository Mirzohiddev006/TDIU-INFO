import { useState } from 'react';
import toast from 'react-hot-toast';
import { Trash2, Plus } from 'lucide-react';
import { useDeleteFaq, useFaq, useSaveFaq } from '@/features/faq/api';
import { useAuth, canEdit } from '@/store/auth';
import { Button, Card, Input, Label, Textarea } from '@/shared/ui';

export function FaqPage() {
  const { data, isLoading } = useFaq();
  const save = useSaveFaq();
  const del = useDeleteFaq();
  const editable = canEdit(useAuth((s) => s.role));
  const [q, setQ] = useState('');
  const [a, setA] = useState('');
  const [kw, setKw] = useState('');

  if (isLoading) return <p>Yuklanmoqda...</p>;
  const add = () => {
    if (!q || !a) return;
    save.mutate({ question: q, answer: a, keywords: kw }, { onSuccess: () => { setQ(''); setA(''); setKw(''); toast.success('Qo\'shildi'); } });
  };
  return (
    <div>
      <h2 className="mb-6 text-2xl font-bold">FAQ — savol-javoblar</h2>
      {editable && (
        <Card className="mb-6 space-y-3 p-4">
          <div><Label>Savol</Label><Input value={q} onChange={(e) => setQ(e.target.value)} /></div>
          <div><Label>Javob</Label><Textarea rows={3} value={a} onChange={(e) => setA(e.target.value)} /></div>
          <div><Label>Kalit so'zlar (vergul bilan)</Label><Input value={kw} onChange={(e) => setKw(e.target.value)} placeholder="kontrakt, narx, summa" /></div>
          <Button onClick={add}><Plus size={16} /> Qo'shish</Button>
        </Card>
      )}
      <div className="space-y-3">
        {data?.map((f) => (
          <Card key={f.id} className="p-4">
            <div className="flex justify-between">
              <p className="font-semibold">{f.question}</p>
              {editable && <Button variant="danger" size="sm" onClick={() => del.mutate(f.id, { onSuccess: () => toast.success('O\'chirildi') })}><Trash2 size={14} /></Button>}
            </div>
            <p className="mt-1 text-sm text-slate-600">{f.answer}</p>
            {f.keywords && <p className="mt-2 text-xs text-slate-400">🔑 {f.keywords}</p>}
          </Card>
        ))}
      </div>
    </div>
  );
}
