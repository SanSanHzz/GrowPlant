import type { PlantType, Plant } from "@/types/plant";

const API = "/api";

function headers(): Record<string, string> {
  const token = localStorage.getItem("session_token");
  return token
    ? { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }
    : { "Content-Type": "application/json" };
}

export async function fetchPlantTypes(): Promise<PlantType[]> {
  const res = await fetch(`${API}/plants/types`);
  if (!res.ok) return [];
  return res.json();
}

export async function selectPlant(plantType: string): Promise<Plant | null> {
  const res = await fetch(`${API}/plants/select`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ plant_type: plantType }),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function fetchMyPlant(): Promise<Plant | null> {
  const res = await fetch(`${API}/plants/mine`, { headers: headers() });
  if (!res.ok) return null;
  return res.json();
}
