import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Wifi, WifiOff, Loader2 } from 'lucide-react';
import { useLogin } from '@/features/auth/api';
import { useAuth } from '@/store/auth';
import { Button, Input, Label } from '@/shared/ui';
import { useHealth, apiBaseUrl } from '@/shared/api/health';

export function LoginPage() {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('');
  const login = useLogin();
  const setAuth = useAuth((s) => s.setAuth);
  const nav = useNavigate();
  const health = useHealth();

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login.mutate({ username, password }, {
      onSuccess: (d) => { setAuth(d.access_token, d.role, d.username); toast.success('Xush kelibsiz!'); nav('/'); },
      onError: () => toast.error("Login yoki parol noto'g'ri, yoki API ulanmagan"),
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800 p-4">
      <div className="w-full max-w-sm">
        <div className="mb-6 text-center text-white">
          <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-2xl bg-white/15 text-2xl font-bold backdrop-blur">T</div>
          <h1 className="text-2xl font-bold">TDIU Admin</h1>
          <p className="mt-1 text-sm text-blue-100">Boshqaruv paneliga kirish</p>
        </div>
        <div className="rounded-2xl bg-white p-7 shadow-xl">
          <form onSubmit={onSubmit} className="space-y-4">
            <div><Label>Login</Label><Input value={username} onChange={(e) => setUsername(e.target.value)} autoFocus /></div>
            <div><Label>Parol</Label><Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" /></div>
            <Button type="submit" className="w-full" disabled={login.isPending}>
              {login.isPending ? <><Loader2 size={16} className="animate-spin" /> Kirilmoqda...</> : 'Kirish'}
            </Button>
          </form>
          <div className="mt-5 flex items-center gap-2 rounded-lg bg-slate-50 p-2.5 text-xs">
            {health.isSuccess ? <Wifi size={14} className="text-emerald-600" /> : <WifiOff size={14} className="text-red-500" />}
            <div className="min-w-0">
              <div className={health.isSuccess ? 'text-emerald-700' : 'text-red-600'}>
                {health.isSuccess ? 'API ulangan' : health.isLoading ? 'API tekshirilmoqda...' : 'API ulanmadi'}
              </div>
              <div className="truncate text-slate-400" title={apiBaseUrl}>{apiBaseUrl}</div>
            </div>
          </div>
        </div>
        <p className="mt-4 text-center text-xs text-blue-100/80">Toshkent davlat iqtisodiyot universiteti</p>
      </div>
    </div>
  );
}
