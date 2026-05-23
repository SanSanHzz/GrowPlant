import { defineStore } from "pinia";
import { ref } from "vue";
import {
  fetchPlantTypes,
  selectPlant,
  fetchMyPlant,
} from "@/services/plantService";
import type { PlantType, Plant } from "@/types/plant";

export const usePlantStore = defineStore("plant", () => {
  const plantTypes = ref<PlantType[]>([]);
  const plant = ref<Plant | null>(null);
  const loading = ref(false);

  async function loadPlantTypes() {
    plantTypes.value = await fetchPlantTypes();
  }

  async function choosePlant(plantType: string) {
    const result = await selectPlant(plantType);
    if (result) plant.value = result;
    return result;
  }

  async function refreshPlant() {
    loading.value = true;
    plant.value = await fetchMyPlant();
    loading.value = false;
  }

  return { plantTypes, plant, loading, loadPlantTypes, choosePlant, refreshPlant };
});
