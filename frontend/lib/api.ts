const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "/api/v1";

async function request(path: string, options: RequestInit = {}) {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  const token = typeof localStorage !== "undefined" ? localStorage.getItem("lt_token") : null;
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(body || `API error ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

export const api = {
  get: (path: string) => request(path),
  post: (path: string, body?: unknown) =>
    request(path, { method: "POST", body: body ? JSON.stringify(body) : undefined }),
};

export function setToken(token: string | null) {
  if (typeof localStorage !== "undefined") {
    if (token) localStorage.setItem("lt_token", token);
    else localStorage.removeItem("lt_token");
  }
}

export function getToken(): string | null {
  if (typeof localStorage === "undefined") return null;
  return localStorage.getItem("lt_token");
}
