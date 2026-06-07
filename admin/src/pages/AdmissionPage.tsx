import { useState } from 'react';
import toast from 'react-hot-toast';
import { useOverview, useSetContract, useSetScores } from '@/features/admission/api';
import { useAuth, canEdit } from '@/store/auth';
import { Button, Card, Input } from '@/shared/ui';
import type { ProgramAdmission } from '@/shared/api/types';

function Row({ row, editable }: { row: ProgramAdmission; editable: boolean }) {
  const setScores = useSetScores();
  const setContract = useSetContract();
  const [pg, setPg] = useState(row.admission?.passing_grant ?? '');
  const [pgr, setPgr] = useState(row.admission?.passing_grant_ru ?? '');
  const [pc, setPc] = useState(row.admission?.passing_contract ?? '');
  const [pcr, setPcr] = useState(row.admission?.passing_contract_ru ?? '');
  const [gp, setGp] = useState(row.admission?.grant_places ?? '');
  const [cp, setCp] = useState(row.admission?.contract_places ?? '');
  const [amt, setAmt] = useState(row.contract?.amount ?? '');

  const num = (v: string | number) => (v === '' ? null : Number(v));

  const save = async () => {
    await setScores.mutateAsync({ programId: row.program.id, data: {
      passing_grant: num(pg), passing_grant_ru: num(pgr),
      passing_contract: num(pc), passing_contract_ru: num(pcr),
      grant_places: num(gp), contract_places: num(cp),
    }});
    await setContract.mutateAsync({ programId: row.program.id, data: { form: row.program.form, amount: num(amt) } });
    toast.success('Saqlandi: ' + row.program.name);
  };

  const cells: [string | number, (s: string) => void, string][] = [
    [pg, setPg as (s: string) => void, 'w-20'],
    [pgr, setPgr as (s: string) => void, 'w-20'],
    [pc, setPc as (s: string) => void, 'w-20'],
    [pcr, setPcr as (s: string) => void, 'w-20'],
    [gp, setGp as (s: string) => void, 'w-16'],
    [cp, setCp as (s: string) => void, 'w-16'],
  ];

  return (
    <tr className="border-b border-slate-100 hover:bg-slate-50">
      <td className="px-3 py-2 text-sm">
        <div className="font-medium">{row.program.name}</div>
        <div className="text-xs text-slate-400">{row.program.code}</div>
      </td>
      {cells.map(([v, set, w], i) => (
        <td key={i} className="px-1 py-2"><Input className={'h-8 ' + w} value={v as string} disabled={!editable}
          onChange={(e) => set(e.target.value)} /></td>
      ))}
      <td className="px-1 py-2"><Input className="h-8 w-32" value={amt as string} disabled={!editable}
        onChange={(e) => setAmt(e.target.value)} /></td>
      <td className="px-2 py-2">{editable && <Button size="sm" onClick={save}>Saqlash</Button>}</td>
    </tr>
  );
}

export function AdmissionPage() {
  const { data, isLoading } = useOverview();
  const role = useAuth((s) => s.role);
  const editable = canEdit(role);
  if (isLoading) return <p>Yuklanmoqda...</p>;
  return (
    <div>
      <h2 className="mb-2 text-2xl font-bold">O'tish bali / Kvota / Kontrakt</h2>
      <p className="mb-6 text-sm text-slate-500">Qiymatlarni kiriting va Saqlash bosing — botda darhol aks etadi. Bo'sh qoldirilsa "tez orada".</p>
      <Card className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-slate-50 text-left text-xs font-semibold text-slate-500">
            <tr>
              <th className="px-3 py-3">Yo'nalish</th>
              <th className="px-1 py-3">Grant (Uz)</th>
              <th className="px-1 py-3">Grant (Ru)</th>
              <th className="px-1 py-3">Kontr. (Uz)</th>
              <th className="px-1 py-3">Kontr. (Ru)</th>
              <th className="px-1 py-3">Grant o'rin</th>
              <th className="px-1 py-3">Kontr. o'rin</th>
              <th className="px-1 py-3">Kontrakt summa</th>
              <th></th>
            </tr>
          </thead>
          <tbody>{data?.map((r) => <Row key={r.program.id} row={r} editable={editable} />)}</tbody>
        </table>
      </Card>
    </div>
  );
}
