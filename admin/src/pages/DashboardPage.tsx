import { Users, Activity, HelpCircle, TrendingUp } from 'lucide-react';
import { useStats } from '@/features/stats/api';
import { Card } from '@/shared/ui';

const cardStyles = [
  { icon: Users, bg: 'bg-blue-50', fg: 'text-blue-600' },
  { icon: Activity, bg: 'bg-emerald-50', fg: 'text-emerald-600' },
  { icon: HelpCircle, bg: 'bg-amber-50', fg: 'text-amber-600' },
];

export function DashboardPage() {
  const { data, isLoading } = useStats();
  if (isLoading) return <p className="text-slate-500">Yuklanmoqda...</p>;

  const cards = [
    { label: 'Foydalanuvchilar', value: data?.users ?? 0 },
    { label: 'Jami amallar', value: data?.actions ?? 0 },
    { label: 'Javobsiz savollar', value: data?.unanswered ?? 0 },
  ];
  const top = data?.top_sections ?? [];
  const maxCount = Math.max(1, ...top.map((s) => s.count));

  return (
    <div>
      <h2 className="mb-1 text-2xl font-bold text-slate-800">Statistika</h2>
      <p className="mb-6 text-sm text-slate-500">Bot foydalanuvchilari va faollik ko'rsatkichlari.</p>
      <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
        {cards.map((c, i) => {
          const S = cardStyles[i];
          return (
            <Card key={c.label} className="flex items-center gap-4 p-5">
              <div className={`flex h-12 w-12 items-center justify-center rounded-xl ${S.bg}`}>
                <S.icon className={S.fg} size={22} />
              </div>
              <div>
                <p className="text-sm text-slate-500">{c.label}</p>
                <p className="text-2xl font-bold text-slate-800">{c.value.toLocaleString()}</p>
              </div>
            </Card>
          );
        })}
      </div>
      <Card className="p-6">
        <h3 className="mb-4 flex items-center gap-2 font-semibold text-slate-800"><TrendingUp size={18} className="text-blue-600" /> Mashhur bo'limlar</h3>
        {top.length ? (
          <div className="space-y-3">
            {top.map((s) => (
              <div key={s.section}>
                <div className="mb-1 flex justify-between text-sm">
                  <span className="text-slate-600">{s.section}</span>
                  <span className="font-semibold text-slate-700">{s.count}</span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
                  <div className="h-full rounded-full bg-blue-500" style={{ width: `${(s.count / maxCount) * 100}%` }} />
                </div>
              </div>
            ))}
          </div>
        ) : <p className="text-sm text-slate-400">Hozircha ma'lumot yo'q. Bot ishlatila boshlagach bu yerda statistika paydo bo'ladi.</p>}
      </Card>
    </div>
  );
}
