<template>
  <div class="dashboard">
    <header class="header">
      <div>
        <h1>Your {{ plantType }}</h1>
        <p class="stage-name">{{ store.plant?.current_stage_name || "seed" }}</p>
      </div>
      <UserMenu :user="userStore.user" @logout="handleLogout" />
    </header>

    <div v-if="!store.plant" class="loading">Loading your plant...</div>

    <template v-else>
      <div class="main-area">
        <PlantCanvas
          :stage="store.plant.current_stage"
          :max-stage="store.plant.max_stage_reached"
        />
        <div class="stats-panel">
          <DropCounter :total="store.plant.total_drops" />
          <ProgressBar
            :stage-name="store.plant.current_stage_name"
            :pct="store.plant.stage_progress_pct"
            :drops-in-stage="store.plant.drops_in_stage"
            :drops-to-next="store.plant.drops_to_next_stage"
            :max-stage="store.plant.max_stage_reached"
          />
        </div>
      </div>

      <DropHistory :drops="store.recentDrops" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/userStore";
import { useDropsStore } from "@/stores/dropsStore";
import { usePlantStore } from "@/stores/plantStore";
import PlantCanvas from "@/components/plant/PlantCanvas.vue";
import DropCounter from "@/components/dashboard/DropCounter.vue";
import ProgressBar from "@/components/dashboard/ProgressBar.vue";
import DropHistory from "@/components/dashboard/DropHistory.vue";
import UserMenu from "@/components/auth/UserMenu.vue";

const userStore = useUserStore();
const store = useDropsStore();
const plantStore = usePlantStore();
const router = useRouter();

const plantType = computed(() => {
  const pt = plantStore.plantTypes.find(
    (t) => t.id === store.plant?.plant_type,
  );
  return pt?.name || store.plant?.plant_type || "Plant";
});

onMounted(() => {
  store.refresh();
});

function handleLogout() {
  userStore.logout();
  router.push("/");
}
</script>

<style scoped>
.dashboard {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 100vh;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
}
.stage-name {
  color: var(--accent);
  text-transform: capitalize;
  font-size: 1.25rem;
}
.loading {
  text-align: center;
  padding: 4rem;
  color: var(--text-secondary);
}
.main-area {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  margin-bottom: 2rem;
}
.stats-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>
