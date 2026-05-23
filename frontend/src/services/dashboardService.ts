import type { DashboardData, DropHistory } from "@/types/plant";

const API = "/api";

export async function fetchDashboard(limit = 20): Promise<DashboardData | null> {
  const res = await fetch(`${API}/dashboard?limit=${limit}`, {
    credentials: "include",
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
    credentials: "include",
  });
  if (!res.ok) return null;
  return res.json();
}
