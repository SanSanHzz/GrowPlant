import type { PlantType, Plant } from "@/types/plant";

const API = "/api";

export async function fetchPlantTypes(): Promise<PlantType[]> {
  const res = await fetch(`${API}/plants/types`);
  if (!res.ok) return [];
  return res.json();
}

export async function selectPlant(plantType: string): Promise<Plant | null> {
  const res = await fetch(`${API}/plants/select`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ plant_type: plantType }),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function fetchMyPlant(): Promise<Plant | null> {
  const res = await fetch(`${API}/plants/mine`, { credentials: "include" });
  if (!res.ok) return null;
  return res.json();
}
