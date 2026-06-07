import { useStats } from '@/features/stats/api';
import { Card } from '@/shared/ui';

export function DashboardPage() {
  const { data, isLoading } = useStats();
  if (isLoading) return <p>Yuklanmoqda...</p>;
  const cards = [
    { label: 'Foydalanuvchilar', value: data?.users ?? 0 },
    { label: 'Jami amallar', value: data?.actions ?? 0 },
    { label: 'Javobsiz savollar', value: data?.unanswered ?? 0 },
  ];
  return (
    <div>
      <h2 className="mb-6 text-2xl font-bold">Statistika</h2>
      <div className="mb-8 grid grid-cols-3 gap-4">
        {cards.map((c) => (
          <Card key={c.label} className="p-6">
            <p className="text-sm text-slate-500">{c.label}</p>
            <p className="mt-2 text-3xl font-bold text-blue-700">{c.value}</p>
          </Card>
        ))}
      </div>
      <Card className="p-6">
        <h3 className="mb-4 font-semibold">Mashhur bo'limlar</h3>
        {data?.top_sections.length ? (
          <ul className="space-y-2">
            {data.top_sections.map((s) => (
              <li key={s.section} className="flex justify-between text-sm">
                <span>{s.section}</span><span className="font-semibold">{s.count}</span>
              </li>
            ))}
          </ul>
        ) : <p className="text-sm text-slate-400">Hozircha ma'lumot yo'q.</p>}
      </Card>
    </div>
  );
}
