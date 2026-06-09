import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { BarChart3, Building2, GraduationCap, HelpCircle, LogOut, FileText, ScrollText, MessageSquare, Megaphone, Wifi, WifiOff } from 'lucide-react';
import { useAuth } from '@/store/auth';
import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui';
import { useHealth, apiBaseUrl } from '@/shared/api/health';

const nav = [
  { to: '/', label: 'Statistika', icon: BarChart3, end: true },
  { to: '/admission', label: 'Ball / Kvota / Kontrakt', icon: ScrollText },
  { to: '/faculties', label: 'Fakultetlar', icon: Building2 },
  { to: '/programs', label: "Yo'nalishlar", icon: GraduationCap },
  { to: '/sections', label: "Bo'lim matnlari", icon: FileText },
  { to: '/faq', label: 'FAQ', icon: HelpCircle },
  { to: '/operator', label: 'Operator', icon: MessageSquare },
  { to: '/broadcast', label: 'Ommaviy xabar', icon: Megaphone },
];

const roleLabel: Record<string, string> = { super: 'Super-admin', content: 'Kontent-menejer', operator: 'Operator' };

function ApiStatus() {
  const { isSuccess, isError, data, isLoading } = useHealth();
  const ok = isSuccess;
  return (
    <div className="rounded-lg border border-slate-200 bg-slate-50 p-2.5 text-xs">
      <div className="mb-1 flex items-center gap-1.5 font-medium">
        {ok ? <Wifi size={14} className="text-emerald-600" /> : <WifiOff size={14} className="text-red-500" />}
        <span className={ok ? 'text-emerald-700' : isLoading ? 'text-slate-500' : 'text-red-600'}>
          {ok ? `Ulangan (${data}ms)` : isLoading ? 'Tekshirilmoqda...' : 'Ulanmadi'}
        </span>
      </div>
      <div className="truncate text-slate-400" title={apiBaseUrl}>{apiBaseUrl}</div>
      {isError && <div className="mt-1 text-red-500">API manzilini config.js / VITE_API_URL da tekshiring</div>}
    </div>
  );
}

export function Layout() {
  const { username, role, logout } = useAuth();
  const navg = useNavigate();
  return (
    <div className="flex min-h-screen">
      <aside className="flex w-64 shrink-0 flex-col border-r border-slate-200 bg-white">
        <div className="flex items-center gap-2.5 border-b border-slate-200 p-5">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-600 font-bold text-white">T</div>
          <div>
            <h1 className="text-sm font-bold leading-tight text-slate-800">TDIU Admin</h1>
            <p className="text-xs text-slate-400">Boshqaruv paneli</p>
          </div>
        </div>
        <nav className="flex-1 space-y-1 overflow-y-auto p-3">
          {nav.map((n) => (
            <NavLink key={n.to} to={n.to} end={n.end}
              className={({ isActive }) => cn('flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition', isActive ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-600 hover:bg-slate-100')}>
              <n.icon size={18} /> {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="space-y-2 border-t border-slate-200 p-3">
          <ApiStatus />
          <div className="flex items-center gap-2 px-1">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-100 text-sm font-semibold text-blue-700">
              {(username || 'A').charAt(0).toUpperCase()}
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm font-medium text-slate-700">{username}</p>
              <p className="text-xs text-slate-400">{roleLabel[role || ''] || role}</p>
            </div>
          </div>
          <Button variant="outline" className="w-full justify-center text-slate-600" size="sm" onClick={() => { logout(); navg('/login'); }}>
            <LogOut size={16} /> Chiqish
          </Button>
        </div>
      </aside>
      <main className="flex-1 overflow-auto p-8">
        <div className="mx-auto max-w-6xl"><Outlet /></div>
      </main>
    </div>
  );
}
