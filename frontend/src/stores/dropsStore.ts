import { defineStore } from "pinia";
import { ref } from "vue";
import { fetchDashboard, fetchDropHistory } from "@/services/dashboardService";
import type { PlantState, DropItem } from "@/types/plant";

export const useDropsStore = defineStore("drops", () => {
  const plant = ref<PlantState | null>(null);
  const recentDrops = ref<DropItem[]>([]);
  const stats = ref({
    total_commits: 0,
    total_pr_merges: 0,
    repositories_contributing: [] as string[],
    first_drop_at: null as string | null,
    last_drop_at: null as string | null,
  });
  const loading = ref(false);

  async function refresh() {
    loading.value = true;
    const data = await fetchDashboard();
    if (data) {
      plant.value = data.plant;
      recentDrops.value = data.recent_drops;
      stats.value = data.stats;
    }
    loading.value = false;
  }

  async function loadMore(cursor?: string) {
    const data = await fetchDropHistory(cursor);
    return data;
  }

  return { plant, recentDrops, stats, loading, refresh, loadMore };
});
