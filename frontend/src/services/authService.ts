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

export async function getAuthStatus(): Promise<AuthStatus> {
  const res = await fetch(`${API_BASE}/auth/status`, {
    credentials: "include",
  });
  if (!res.ok) return { authenticated: false, user: null };
  return res.json();
}

export async function logout(): Promise<void> {
  await fetch(`${API_BASE}/auth/logout`, {
    method: "POST",
    credentials: "include",
  });
}
