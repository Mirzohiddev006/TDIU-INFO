declare global {
  interface Window {
    __API_URL__?: string;
  }
}

const FALLBACK_API = "https://tdiu-bot-api.onrender.com/api";

export const env = {
  apiUrl:
    (typeof window !== "undefined" && window.__API_URL__) ||
    (import.meta.env.VITE_API_URL as string | undefined) ||
    FALLBACK_API,
} as const;
