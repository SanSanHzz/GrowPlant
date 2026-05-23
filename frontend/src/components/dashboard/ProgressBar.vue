<template>
  <div class="progress-section">
    <div class="header">
      <span>{{ stageName }}</span>
      <span class="pct">{{ pct }}%</span>
    </div>
    <div class="track">
      <div class="fill" :style="{ width: pct + '%' }"></div>
    </div>
    <div class="footer">
      <span>{{ dropsInStage }} drops in this stage</span>
      <span v-if="!maxStage">{{ dropsToNext }} to next stage</span>
      <span v-else class="max">MAX LEVEL</span>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  stageName: string;
  pct: number;
  dropsInStage: number;
  dropsToNext: number;
  maxStage: boolean;
}>();
</script>

<style scoped>
.progress-section {
  width: 100%;
}
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-weight: 600;
  text-transform: capitalize;
}
.pct { color: var(--accent); }
.track {
  height: 8px;
  background: var(--border);
  border-radius: 4px;
  overflow: hidden;
}
.fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-hover));
  border-radius: 4px;
  transition: width 0.5s ease;
}
.footer {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
}
.max { color: var(--warning); font-weight: 700; }
</style>
