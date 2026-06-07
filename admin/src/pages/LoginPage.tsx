import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useLogin } from '@/features/auth/api';
import { useAuth } from '@/store/auth';
import { Button, Card, Input, Label } from '@/shared/ui';

export function LoginPage() {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('');
  const login = useLogin();
  const setAuth = useAuth((s) => s.setAuth);
  const nav = useNavigate();

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login.mutate({ username, password }, {
      onSuccess: (d) => { setAuth(d.access_token, d.role, d.username); toast.success('Xush kelibsiz!'); nav('/'); },
      onError: () => toast.error("Login yoki parol noto'g'ri"),
    });
  };

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-sm p-8">
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-blue-700">TDIU Admin</h1>
          <p className="mt-1 text-sm text-slate-500">Boshqaruv paneliga kirish</p>
        </div>
        <form onSubmit={onSubmit} className="space-y-4">
          <div><Label>Login</Label><Input value={username} onChange={(e) => setUsername(e.target.value)} autoFocus /></div>
          <div><Label>Parol</Label><Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></div>
          <Button type="submit" className="w-full" disabled={login.isPending}>{login.isPending ? 'Kirilmoqda...' : 'Kirish'}</Button>
        </form>
      </Card>
    </div>
  );
}
