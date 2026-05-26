<template>
  <div class="dashboard">
    <header class="header">
      <div>
        <h1>Your {{ plantType }}</h1>
        <p class="stage-name">{{ store.plant?.current_stage_name || "seed" }}</p>
      </div>
      <div class="header-right">
        <ThemeToggle />
        <UserMenu :user="userStore.user" @logout="handleLogout" />
      </div>
    </header>

    <div v-if="!store.plant && !store.loading" class="empty-state">
      <p>No active plant. Select one below.</p>
    </div>

    <div v-if="store.loading && !store.plant" class="loading">Loading your plant...</div>

    <template v-if="store.plant">
      <div class="main-area">
        <div class="plant-wrapper">
          <WaterDrop :trigger="dropTrigger" @done="dropTrigger = 0" />
          <StageTransition :trigger="stageTrigger" @done="stageTrigger = 0" />
          <PlantCanvas
            :stage="store.plant.current_stage"
            :sub-stage="subStage"
            :max-stage="store.plant.max_stage_reached"
          />
        </div>
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

    <MyPlants
      :plants="plantStore.plants"
      @add="showModal = true"
      @switch="handleSwitchPlant"
      @refresh="handleRefresh"
    />

    <AddPlantModal
      v-if="showModal"
      :plant-types="plantStore.plantTypes"
      @close="showModal = false"
      @select="handleAddPlant"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, computed, ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/userStore";
import { useDropsStore } from "@/stores/dropsStore";
import { usePlantStore } from "@/stores/plantStore";
import { connectEventStream } from "@/services/eventService";
import PlantCanvas from "@/components/plant/PlantCanvas.vue";
import WaterDrop from "@/components/plant/WaterDrop.vue";
import StageTransition from "@/components/plant/StageTransition.vue";
import DropCounter from "@/components/dashboard/DropCounter.vue";
import ProgressBar from "@/components/dashboard/ProgressBar.vue";
import DropHistory from "@/components/dashboard/DropHistory.vue";
import MyPlants from "@/components/dashboard/MyPlants.vue";
import AddPlantModal from "@/components/dashboard/AddPlantModal.vue";
import UserMenu from "@/components/auth/UserMenu.vue";
import ThemeToggle from "@/components/ThemeToggle.vue";

const userStore = useUserStore();
const store = useDropsStore();
const plantStore = usePlantStore();
const router = useRouter();

const dropTrigger = ref(0);
const stageTrigger = ref(0);
const showModal = ref(false);
let disconnectStream: (() => void) | null = null;

const plantType = computed(() => {
  const pt = plantStore.plantTypes.find(
    (t) => t.id === store.plant?.plant_type,
  );
  return pt?.name || store.plant?.plant_type || "Plant";
});

const stageThresholds: Record<number, number> = { 1: 5, 2: 15, 3: 30, 4: 50, 5: 0 };

const subStage = computed(() => {
  if (!store.plant) return 0;
  const stage = store.plant.current_stage;
  if (stage >= 5) return 2;
  const needed = stageThresholds[stage] || 1;
  const prevThreshold = stage === 1 ? 0 : stageThresholds[stage - 1];
  const range = needed - prevThreshold;
  if (range <= 0) return 2;
  const progress = store.plant.total_drops - prevThreshold;
  return Math.min(2, Math.max(0, (progress / range) * 2));
});

onMounted(async () => {
  plantStore.loadPlantTypes();
  await plantStore.loadPlants();
  await store.refresh();

  disconnectStream = await connectEventStream({
    onDropReceived: (data) => {
      dropTrigger.value++;
      if (store.plant) {
        store.plant.total_drops = data.total_drops;
      }
    },
    onStageAdvanced: (data) => {
      stageTrigger.value++;
      store.refresh();
    },
  });
});

onUnmounted(() => {
  disconnectStream?.();
});

async function handleLogout() {
  await userStore.logout();
  router.push("/");
}

async function handleSwitchPlant(plantId: string) {
  await plantStore.switchActive(plantId);
  await store.refresh();
}

async function handleRefresh() {
  await plantStore.loadPlants();
  await store.refresh();
}

async function handleAddPlant(plantType: string) {
  await plantStore.choosePlant(plantType);
  showModal.value = false;
  await plantStore.loadPlants();
  await store.refresh();
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
.header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.stage-name {
  color: var(--accent);
  text-transform: capitalize;
  font-size: 1.25rem;
}
.loading, .empty-state {
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
.plant-wrapper {
  position: relative;
  flex-shrink: 0;
}
.stats-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
</style>
