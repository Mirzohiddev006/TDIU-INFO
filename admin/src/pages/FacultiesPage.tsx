import { useState } from 'react';
import toast from 'react-hot-toast';
import { Trash2, Plus } from 'lucide-react';
import { useDeleteFaculty, useFaculties, useSaveFaculty } from '@/features/faculties/api';
import { useAuth, canEdit } from '@/store/auth';
import { Button, Card, Input } from '@/shared/ui';

export function FacultiesPage() {
  const { data, isLoading } = useFaculties();
  const save = useSaveFaculty();
  const del = useDeleteFaculty();
  const editable = canEdit(useAuth((s) => s.role));
  const [name, setName] = useState('');

  if (isLoading) return <p>Yuklanmoqda...</p>;
  return (
    <div>
      <h2 className="mb-6 text-2xl font-bold">Fakultetlar</h2>
      {editable && (
        <Card className="mb-4 flex gap-2 p-4">
          <Input placeholder="Yangi fakultet nomi" value={name} onChange={(e) => setName(e.target.value)} />
          <Button onClick={() => name && save.mutate({ name }, { onSuccess: () => { setName(''); toast.success('Qo\'shildi'); } })}><Plus size={16} /> Qo'shish</Button>
        </Card>
      )}
      <Card>
        {data?.map((f) => (
          <div key={f.id} className="flex items-center justify-between border-b border-slate-100 px-4 py-3 last:border-0">
            <span className="font-medium">{f.name}</span>
            {editable && <Button variant="danger" size="sm" onClick={() => del.mutate(f.id, { onSuccess: () => toast.success('O\'chirildi') })}><Trash2 size={14} /></Button>}
          </div>
        ))}
      </Card>
    </div>
  );
}
