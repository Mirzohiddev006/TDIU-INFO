declare global {
  interface Window {
    __API_URL__?: string;
  }
}

export const env = {
  apiUrl:
    (typeof window !== "undefined" && window.__API_URL__) ||
    (import.meta.env.VITE_API_URL as string | undefined) ||
    "http://localhost:8000/api",
} as const;
