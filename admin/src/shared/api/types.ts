export interface Faculty { id: number; slug: string; name: string; description: string | null; sort_order: number; }
export interface Program { id: number; slug: string; faculty_id: number; code: string; name: string; form: string; lang: string; sort_order: number; }
export interface Admission { id: number; program_id: number; year: string; grant_places: number | null; contract_places: number | null; passing_grant: number | null; passing_contract: number | null; }
export interface Contract { id: number; program_id: number; year: string; form: string; amount: number | null; }
export interface ProgramAdmission { program: Program; admission: Admission | null; contract: Contract | null; }
export interface Faq { id: number; question: string; answer: string; category: string | null; keywords: string | null; sort_order: number; }
export interface Section { id: number; key: string; title: string; body: string; }
export interface Stats { users: number; actions: number; top_sections: { section: string; count: number }[]; unanswered: number; }
export type Role = 'super' | 'content' | 'operator';
