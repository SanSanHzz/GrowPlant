const API_BASE = "/api";

export interface User {
  id: string;
  github_id: number;
  username: string;
  display_name: string | null;
  avatar_url: string | null;
}

export interface AuthStatus {
  authenticated: boolean;
  user: User | null;
}

function headers(): Record<string, string> {
  const token = localStorage.getItem("session_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function getAuthStatus(): Promise<AuthStatus> {
  const res = await fetch(`${API_BASE}/auth/status`, {
    headers: { ...headers(), "Content-Type": "application/json" },
  });
  if (!res.ok) return { authenticated: false, user: null };
  return res.json();
}

export async function logout(): Promise<void> {
  await fetch(`${API_BASE}/auth/logout`, {
    method: "POST",
    headers: headers(),
  });
  localStorage.removeItem("session_token");
}
