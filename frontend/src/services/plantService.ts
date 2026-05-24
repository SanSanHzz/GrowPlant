import type { PlantType, Plant, PlantList } from "@/types/plant";

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

export async function fetchMyPlants(): Promise<PlantList | null> {
  const res = await fetch(`${API}/plants/mine`, { headers: headers() });
  if (!res.ok) return null;
  return res.json();
}

export async function renamePlant(plantId: string, name: string): Promise<Plant | null> {
  const res = await fetch(`${API}/plants/${plantId}/name`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify({ name }),
  });
  if (!res.ok) return null;
  return res.json();
}

export async function deletePlant(plantId: string): Promise<boolean> {
  const res = await fetch(`${API}/plants/${plantId}`, {
    method: "DELETE",
    headers: headers(),
  });
  return res.ok;
}

export async function activatePlant(plantId: string): Promise<Plant | null> {
  const res = await fetch(`${API}/plants/activate`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ plant_id: plantId }),
  });
  if (!res.ok) return null;
  return res.json();
}
