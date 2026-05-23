<template>
  <div class="counter">
    <span class="icon">💧</span>
    <span class="value">{{ total }}</span>
    <span class="label">total drops</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{ total: number }>();
</script>

<style scoped>
.counter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem 1.5rem;
}
.icon { font-size: 1.5rem; }
.value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--accent);
}
.label {
  color: var(--text-secondary);
  font-size: 0.875rem;
}
</style>
