<template>
  <Teleport to="body">
    <div class="overlay" @click.self="$emit('close')">
      <div class="modal">
        <h2>Choose a new plant</h2>
        <p class="sub">Select a species to add to your garden</p>
        <div class="grid">
          <div
            v-for="pt in plantTypes"
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
        <div class="actions">
          <button class="btn cancel" @click="$emit('close')">Cancel</button>
          <button
            class="btn confirm"
            :disabled="!selected"
            @click="confirm"
          >
            Add Plant
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { PlantType } from "@/types/plant";

const props = defineProps<{ plantTypes: PlantType[] }>();
const emit = defineEmits<{ close: []; select: [type: string] }>();

const selected = ref("");

function emoji(id: string) {
  const map: Record<string, string> = {
    cactus: "🌵",
    bonsai: "🌳",
    cannabis: "🌿",
    fruit: "🍓",
  };
  return map[id] || "🌱";
}

function confirm() {
  if (selected.value) emit("select", selected.value);
}
</script>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.modal {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 2rem;
  max-width: 600px;
  width: 90%;
}
.modal h2 {
  text-align: center;
  margin-bottom: 0.25rem;
}
.sub {
  text-align: center;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}
.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}
.card {
  background: var(--bg-card);
  border: 2px solid var(--border);
  border-radius: 12px;
  padding: 1.25rem;
  text-align: center;
  cursor: pointer;
  transition: border-color 0.2s;
}
.card:hover {
  border-color: var(--accent);
}
.card.selected {
  border-color: var(--accent);
  background: color-mix(in srgb, var(--accent) 10%, var(--bg-card));
}
.preview {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}
.card h3 {
  font-size: 1rem;
  margin-bottom: 0.25rem;
}
.card p {
  font-size: 0.8rem;
  color: var(--text-secondary);
}
.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}
.btn {
  padding: 0.6rem 2rem;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  border: none;
}
.cancel {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border);
}
.confirm {
  background: var(--accent);
  color: #fff;
}
.confirm:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
