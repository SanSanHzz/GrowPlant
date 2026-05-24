import { defineStore } from "pinia";
import { ref } from "vue";
import {
  fetchPlantTypes,
  selectPlant,
  fetchMyPlants,
  activatePlant,
} from "@/services/plantService";
import type { PlantType, Plant } from "@/types/plant";

export const usePlantStore = defineStore("plant", () => {
  const plantTypes = ref<PlantType[]>([]);
  const plants = ref<Plant[]>([]);
  const activePlant = ref<Plant | null>(null);
  const loading = ref(false);

  async function loadPlantTypes() {
    plantTypes.value = await fetchPlantTypes();
  }

  async function loadPlants() {
    loading.value = true;
    const data = await fetchMyPlants();
    if (data) {
      plants.value = data.plants;
      activePlant.value =
        data.plants.find((p) => p.id === data.active_plant_id) || null;
    }
    loading.value = false;
  }

  async function choosePlant(plantType: string) {
    const result = await selectPlant(plantType);
    if (result) {
      await loadPlants();
    }
    return result;
  }

  async function switchActive(plantId: string) {
    const result = await activatePlant(plantId);
    if (result) {
      activePlant.value = result;
      plants.value = plants.value.map((p) => ({
        ...p,
        is_active: p.id === plantId,
      }));
    }
    return result;
  }

  return {
    plantTypes,
    plants,
    activePlant,
    loading,
    loadPlantTypes,
    loadPlants,
    choosePlant,
    switchActive,
  };
});
