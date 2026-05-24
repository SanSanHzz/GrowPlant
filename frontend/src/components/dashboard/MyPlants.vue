<template>
  <div class="my-plants">
    <div class="header">
      <h3>My Plants ({{ plants.length }})</h3>
      <button class="add-btn" @click="$emit('add')">+ New Plant</button>
    </div>
    <div class="list">
      <div
        v-for="p in plants"
        :key="p.id"
        class="plant-card"
        :class="{ active: p.is_active }"
        @click="switchTo(p)"
      >
        <span class="emoji">{{ emoji(p.plant_type) }}</span>
        <div class="info">
          <input
            v-if="editing === p.id"
            class="rename-input"
            v-model="editName"
            @blur="saveRename(p)"
            @keyup.enter="saveRename(p)"
            @keyup.escape="editing = ''"
            @click.stop
            ref="editInput"
          />
          <span v-else class="name">{{ p.name || p.plant_type }}</span>
          <span class="stage">{{ p.current_stage_name }}</span>
        </div>
        <span class="drops">{{ p.total_drops }} 💧</span>
        <span v-if="p.is_active" class="badge">Active</span>
        <div class="actions" @click.stop>
          <button class="icon-btn" title="Rename" @click="startRename(p)">
            ✏️
          </button>
          <button class="icon-btn" title="Delete" @click="confirmDelete(p)">
            🗑️
          </button>
        </div>
      </div>
      <div v-if="plants.length === 0" class="empty">No plants yet</div>
    </div>

    <!-- Delete confirmation modal -->
    <Teleport to="body">
      <div v-if="deleting" class="modal-overlay" @click.self="deleting = null">
        <div class="modal">
          <h3>Delete plant?</h3>
          <p>
            This will permanently delete
            <strong>{{ deleting.name || deleting.plant_type }}</strong>
            and all its drops. This cannot be undone.
          </p>
          <div class="modal-actions">
            <button class="btn cancel" @click="deleting = null">Cancel</button>
            <button class="btn danger" @click="doDelete">Delete</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import type { Plant } from "@/types/plant";
import { renamePlant, deletePlant } from "@/services/plantService";

defineProps<{ plants: Plant[] }>();
const emit = defineEmits<{
  add: [];
  switch: [id: string];
  refresh: [];
}>();

const editing = ref("");
const editName = ref("");
const deleting = ref<Plant | null>(null);

function emoji(type: string) {
  const map: Record<string, string> = {
    cactus: "🌵",
    bonsai: "🌳",
    cannabis: "🌿",
    fruit: "🍓",
  };
  return map[type] || "🌱";
}

function switchTo(p: Plant) {
  if (!p.is_active) emit("switch", p.id);
}

function startRename(p: Plant) {
  editing.value = p.id;
  editName.value = p.name || p.plant_type;
  setTimeout(() => {
    const el = document.querySelector<HTMLInputElement>(".rename-input");
    el?.focus();
  }, 50);
}

async function saveRename(p: Plant) {
  if (!editName.value.trim()) return;
  await renamePlant(p.id, editName.value.trim());
  editing.value = "";
  emit("refresh");
}

function confirmDelete(p: Plant) {
  deleting.value = p;
}

async function doDelete() {
  if (!deleting.value) return;
  await deletePlant(deleting.value.id);
  deleting.value = null;
  emit("refresh");
}
</script>

<style scoped>
.my-plants { margin-top: 2rem; }
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}
.add-btn {
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
  padding: 0.4rem 1rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}
.add-btn:hover { background: var(--accent); color: #fff; }
.list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.plant-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.2s;
}
.plant-card:hover { border-color: var(--accent); }
.plant-card.active {
  border-color: var(--accent);
  background: color-mix(in srgb, var(--accent) 8%, var(--bg-card));
}
.emoji { font-size: 1.5rem; flex-shrink: 0; }
.info { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.name { font-weight: 600; text-transform: capitalize; }
.stage {
  font-size: 0.8rem;
  color: var(--text-secondary);
  text-transform: capitalize;
}
.rename-input {
  font: inherit;
  font-weight: 600;
  background: var(--bg-primary);
  border: 1px solid var(--accent);
  border-radius: 4px;
  padding: 0.15rem 0.4rem;
  color: var(--text-primary);
  outline: none;
  width: 100%;
}
.drops { font-size: 0.9rem; color: var(--accent); font-weight: 600; white-space: nowrap; }
.badge {
  font-size: 0.7rem;
  background: var(--accent);
  color: #fff;
  padding: 0.15rem 0.5rem;
  border-radius: 10px;
  font-weight: 700;
  flex-shrink: 0;
}
.actions {
  display: flex;
  gap: 0.25rem;
  flex-shrink: 0;
  opacity: 0;
  transition: opacity 0.15s;
}
.plant-card:hover .actions { opacity: 1; }
.icon-btn {
  background: transparent;
  border: none;
  font-size: 1rem;
  padding: 0.2rem;
  cursor: pointer;
  border-radius: 4px;
  line-height: 1;
}
.icon-btn:hover { background: var(--border); }
.empty { text-align: center; padding: 1.5rem; color: var(--text-secondary); }

/* Modal */
.modal-overlay {
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
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
}
.modal h3 { margin-bottom: 0.75rem; }
.modal p { color: var(--text-secondary); margin-bottom: 1.5rem; line-height: 1.5; }
.modal-actions { display: flex; gap: 1rem; justify-content: center; }
.btn {
  padding: 0.6rem 2rem;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
}
.cancel { background: transparent; color: var(--text-secondary); border: 1px solid var(--border); }
.danger { background: var(--danger); color: #fff; }
.danger:hover { opacity: 0.9; }
</style>
