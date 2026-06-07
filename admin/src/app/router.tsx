import { createBrowserRouter, Navigate } from 'react-router-dom';
import { useAuth } from '@/store/auth';
import { Layout } from '@/widgets/Layout';
import { LoginPage } from '@/pages/LoginPage';
import { DashboardPage } from '@/pages/DashboardPage';
import { AdmissionPage } from '@/pages/AdmissionPage';
import { FacultiesPage } from '@/pages/FacultiesPage';
import { ProgramsPage } from '@/pages/ProgramsPage';
import { SectionsPage } from '@/pages/SectionsPage';
import { FaqPage } from '@/pages/FaqPage';
import { BroadcastPage } from '@/pages/BroadcastPage';
import { OperatorPage } from '@/pages/OperatorPage';
import type { ReactNode } from 'react';

function Protected({ children }: { children: ReactNode }) {
  const token = useAuth((s) => s.token);
  return token ? <>{children}</> : <Navigate to="/login" replace />;
}

export const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    path: '/',
    element: <Protected><Layout /></Protected>,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'admission', element: <AdmissionPage /> },
      { path: 'faculties', element: <FacultiesPage /> },
      { path: 'programs', element: <ProgramsPage /> },
      { path: 'sections', element: <SectionsPage /> },
      { path: 'faq', element: <FaqPage /> },
      { path: 'operator', element: <OperatorPage /> },
      { path: 'broadcast', element: <BroadcastPage /> },
    ],
  },
]);
