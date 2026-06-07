import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { BarChart3, Building2, GraduationCap, HelpCircle, LogOut, FileText, ScrollText, MessageSquare, Megaphone } from 'lucide-react';
import { useAuth } from '@/store/auth';
import { cn } from '@/shared/lib/cn';
import { Button } from '@/shared/ui';

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

export function Layout() {
  const { username, role, logout } = useAuth();
  const navg = useNavigate();
  return (
    <div className="flex min-h-screen">
      <aside className="flex w-64 flex-col border-r border-slate-200 bg-white">
        <div className="border-b border-slate-200 p-5">
          <h1 className="text-lg font-bold text-blue-700">TDIU Admin</h1>
          <p className="text-xs text-slate-500">{username} · {role}</p>
        </div>
        <nav className="flex-1 space-y-1 p-3">
          {nav.map((n) => (
            <NavLink key={n.to} to={n.to} end={n.end}
              className={({ isActive }) => cn('flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium', isActive ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-100')}>
              <n.icon size={18} /> {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-slate-200 p-3">
          <Button variant="ghost" className="w-full justify-start text-slate-600" onClick={() => { logout(); navg('/login'); }}>
            <LogOut size={18} /> Chiqish
          </Button>
        </div>
      </aside>
      <main className="flex-1 overflow-auto p-8"><Outlet /></main>
    </div>
  );
}
