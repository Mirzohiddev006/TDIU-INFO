import { useRef, useState } from 'react';
import toast from 'react-hot-toast';
import { Paperclip, X, Image as ImageIcon } from 'lucide-react';
import { useBroadcast } from '@/features/broadcast/api';
import { useAuth, canEdit } from '@/store/auth';
import { Button, Card, Label, Textarea } from '@/shared/ui';

export function BroadcastPage() {
  const [text, setText] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const bc = useBroadcast();
  const editable = canEdit(useAuth((s) => s.role));

  const isImage = file?.type.startsWith('image/');
  const previewUrl = isImage && file ? URL.createObjectURL(file) : null;

  const clearFile = () => { setFile(null); if (fileRef.current) fileRef.current.value = ''; };

  const send = () => {
    if (!text.trim() && !file) { toast.error('Matn yoki fayl kiriting.'); return; }
    if (!confirm('Xabar BARCHA foydalanuvchilarga yuboriladi. Davom etamizmi?')) return;
    bc.mutate({ text, file }, {
      onSuccess: (r) => {
        toast.success(`Yuborildi: ${r.sent}/${r.total} (xato: ${r.failed})`);
        setText(''); clearFile();
      },
      onError: () => toast.error('Yuborishda xato (bot ishlayaptimi? BOT_TOKEN sozlanganmi?)'),
    });
  };

  return (
    <div className="max-w-2xl">
      <h2 className="mb-2 text-2xl font-bold">Ommaviy xabar (broadcast)</h2>
      <p className="mb-6 text-sm text-slate-500">
        Matn, rasm yoki fayl barcha bot foydalanuvchilariga yuboriladi. HTML teglar (&lt;b&gt;) qo'llab-quvvatlanadi.
        Rasm/fayl bilan birga yozilgan matn izoh (caption) sifatida ketadi.
      </p>
      <Card className="space-y-4 p-6">
        <div>
          <Label>Xabar matni</Label>
          <Textarea rows={6} value={text} onChange={(e) => setText(e.target.value)}
            placeholder="E'lon matnini yozing..." disabled={!editable} />
        </div>

        <div>
          <Label>Rasm yoki fayl (ixtiyoriy)</Label>
          <input ref={fileRef} type="file" className="hidden" disabled={!editable}
            accept="image/*,.pdf,.doc,.docx,.xls,.xlsx,.zip"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
          {!file ? (
            <Button variant="outline" type="button" disabled={!editable}
              onClick={() => fileRef.current?.click()}>
              <Paperclip size={16} className="mr-2" /> Fayl tanlash
            </Button>
          ) : (
            <div className="flex items-center gap-3 rounded-lg border border-slate-200 bg-slate-50 p-3">
              {previewUrl
                ? <img src={previewUrl} alt="" className="h-14 w-14 rounded object-cover" />
                : <ImageIcon size={28} className="text-slate-400" />}
              <div className="min-w-0 flex-1">
                <div className="truncate text-sm font-medium text-slate-700">{file.name}</div>
                <div className="text-xs text-slate-400">{(file.size / 1024 / 1024).toFixed(2)} MB</div>
              </div>
              <button type="button" onClick={clearFile} className="text-slate-400 hover:text-red-500">
                <X size={18} />
              </button>
            </div>
          )}
        </div>

        {editable
          ? <Button onClick={send} disabled={bc.isPending}>
              {bc.isPending ? 'Yuborilmoqda...' : 'Hammaga yuborish'}
            </Button>
          : <p className="text-sm text-slate-400">Sizda yuborish huquqi yo'q.</p>}
      </Card>
    </div>
  );
}
