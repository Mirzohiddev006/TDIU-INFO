import { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import { useSaveSection, useSections } from '@/features/sections/api';
import { useAuth, canEdit } from '@/store/auth';
import { Button, Card, Input, Label, Textarea } from '@/shared/ui';

export function SectionsPage() {
  const { data, isLoading } = useSections();
  const save = useSaveSection();
  const editable = canEdit(useAuth((s) => s.role));
  const [sel, setSel] = useState<string>('');
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');

  useEffect(() => {
    if (data && !sel && data[0]) { setSel(data[0].key); setTitle(data[0].title); setBody(data[0].body); }
  }, [data, sel]);

  const pick = (key: string) => {
    const s = data?.find((x) => x.key === key);
    if (s) { setSel(key); setTitle(s.title); setBody(s.body); }
  };
  if (isLoading) return <p>Yuklanmoqda...</p>;
  return (
    <div>
      <h2 className="mb-6 text-2xl font-bold">Bo'lim matnlari</h2>
      <div className="flex gap-4">
        <Card className="w-56 shrink-0 p-2">
          {data?.map((s) => (
            <button key={s.key} onClick={() => pick(s.key)}
              className={`block w-full rounded-lg px-3 py-2 text-left text-sm ${sel === s.key ? 'bg-blue-50 text-blue-700' : 'hover:bg-slate-100'}`}>{s.title}</button>
          ))}
        </Card>
        <Card className="flex-1 space-y-4 p-6">
          <div><Label>Sarlavha</Label><Input value={title} onChange={(e) => setTitle(e.target.value)} disabled={!editable} /></div>
          <div><Label>Matn (HTML qo'llab-quvvatlanadi)</Label><Textarea rows={14} value={body} onChange={(e) => setBody(e.target.value)} disabled={!editable} /></div>
          {editable && <Button onClick={() => save.mutate({ key: sel, title, body }, { onSuccess: () => toast.success('Saqlandi') })}>Saqlash</Button>}
        </Card>
      </div>
    </div>
  );
}
