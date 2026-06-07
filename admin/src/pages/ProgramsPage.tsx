import { useFaculties } from '@/features/faculties/api';
import { usePrograms } from '@/features/programs/api';
import { Card, Badge } from '@/shared/ui';

export function ProgramsPage() {
  const { data: programs, isLoading } = usePrograms();
  const { data: faculties } = useFaculties();
  if (isLoading) return <p>Yuklanmoqda...</p>;
  const facName = (id: number) => faculties?.find((f) => f.id === id)?.name ?? '—';
  return (
    <div>
      <h2 className="mb-6 text-2xl font-bold">Yo'nalishlar ({programs?.length ?? 0})</h2>
      <Card className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-50 text-left text-xs font-semibold text-slate-500">
            <tr><th className="px-4 py-3">Nomi</th><th className="px-4 py-3">Kodi</th><th className="px-4 py-3">Fakultet</th><th className="px-4 py-3">Shakl</th></tr>
          </thead>
          <tbody>
            {programs?.map((p) => (
              <tr key={p.id} className="border-b border-slate-100">
                <td className="px-4 py-2 text-sm font-medium">{p.name}</td>
                <td className="px-4 py-2"><Badge className="bg-slate-100 text-slate-700">{p.code}</Badge></td>
                <td className="px-4 py-2 text-sm text-slate-500">{facName(p.faculty_id)}</td>
                <td className="px-4 py-2 text-sm">{p.form}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
