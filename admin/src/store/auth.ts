import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Role } from '@/shared/api/types';

interface AuthState {
  token: string | null;
  role: Role | null;
  username: string | null;
  setAuth: (token: string, role: Role, username: string) => void;
  logout: () => void;
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      role: null,
      username: null,
      setAuth: (token, role, username) => set({ token, role, username }),
      logout: () => set({ token: null, role: null, username: null }),
    }),
    { name: 'tdiu-admin-auth' },
  ),
);

export const canEdit = (role: Role | null) => role === 'super' || role === 'content';
