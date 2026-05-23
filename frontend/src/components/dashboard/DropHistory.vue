<template>
  <div class="history">
    <h3>Recent drops</h3>
    <div v-if="drops.length === 0" class="empty">No drops yet — start committing!</div>
    <div v-for="d in drops" :key="d.id" class="entry">
      <span class="type-icon">{{ icon(d.event_type) }}</span>
      <div class="info">
        <span class="repo">{{ d.source_repo }}</span>
        <span class="date">{{ formatDate(d.committed_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DropItem } from "@/types/plant";

defineProps<{ drops: DropItem[] }>();

function icon(type: string) {
  return type === "pull_request_merge" ? "🔀" : "💻";
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
</script>

<style scoped>
.history { width: 100%; }
.history h3 { margin-bottom: 1rem; }
.empty { color: var(--text-secondary); text-align: center; padding: 2rem; }
.entry {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border);
}
.entry:last-child { border-bottom: none; }
.type-icon { font-size: 1.25rem; }
.info {
  display: flex;
  flex-direction: column;
}
.repo { font-weight: 500; }
.date { font-size: 0.8rem; color: var(--text-secondary); }
</style>
