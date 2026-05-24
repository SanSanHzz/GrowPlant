<template>
  <div class="select-page">
    <div class="top-bar">
      <ThemeToggle />
    </div>
    <h1 class="title">Choose your plant</h1>
    <p class="subtitle">Each type grows differently based on your commits</p>
    <div class="grid">
      <div
        v-for="pt in plantStore.plantTypes"
        :key="pt.id"
        class="card"
        :class="{ selected: selected === pt.id }"
        @click="selected = pt.id"
      >
        <div class="preview">{{ emoji(pt.id) }}</div>
        <h3>{{ pt.name }}</h3>
        <p>{{ pt.description }}</p>
      </div>
    </div>
    <button class="confirm-btn" :disabled="!selected" @click="confirm">
      Grow this plant
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { usePlantStore } from "@/stores/plantStore";
import ThemeToggle from "@/components/ThemeToggle.vue";

const plantStore = usePlantStore();
const router = useRouter();
const selected = ref("");

onMounted(() => {
  plantStore.loadPlantTypes();
});

function emoji(id: string) {
  const map: Record<string, string> = {
    cactus: "🌵",
    bonsai: "🌳",
    cannabis: "🌿",
    fruit: "🍓",
  };
  return map[id] || "🌱";
}

async function confirm() {
  if (!selected.value) return;
  const result = await plantStore.choosePlant(selected.value);
  if (result) router.push("/dashboard");
}
</script>

<style scoped>
.top-bar {
  position: absolute;
  top: 1rem;
  right: 1rem;
}
.select-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem 2rem;
  min-height: 100vh;
  position: relative;
}
.title { font-size: 2rem; margin-bottom: 0.5rem; }
.subtitle { color: var(--text-secondary); margin-bottom: 2rem; }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  max-width: 900px;
  width: 100%;
}
.card {
  background: var(--bg-card);
  border: 2px solid var(--border);
  border-radius: 12px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
}
.card:hover { border-color: var(--accent); }
.card.selected { border-color: var(--accent); background: #1a3a1a; }
[data-theme="light"] .card.selected { background: #dcfce7; }
.preview { font-size: 3rem; margin-bottom: 0.75rem; }
.confirm-btn {
  margin-top: 2rem;
  background: var(--accent);
  color: #fff;
  border: none;
  padding: 0.75rem 3rem;
  border-radius: 8px;
  font-size: 1.125rem;
  font-weight: 600;
}
.confirm-btn:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
