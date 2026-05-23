import type { DashboardData, DropHistory } from "@/types/plant";

const API = "/api";

function headers(): Record<string, string> {
  const token = localStorage.getItem("session_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function fetchDashboard(limit = 20): Promise<DashboardData | null> {
  const res = await fetch(`${API}/dashboard?limit=${limit}`, {
    headers: headers(),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function fetchDropHistory(
  cursor?: string,
  limit = 50,
): Promise<DropHistory | null> {
  const params = new URLSearchParams({ limit: String(limit) });
  if (cursor) params.set("cursor", cursor);
  const res = await fetch(`${API}/dashboard/history?${params}`, {
    headers: headers(),
  });
  if (!res.ok) return null;
  return res.json();
}
