<template>
  <div class="plant-canvas">
    <svg viewBox="0 0 200 250" class="plant-svg">
      <!-- Pot -->
      <rect x="60" y="190" width="80" height="40" rx="6" fill="#8B5E3C" />
      <rect x="50" y="220" width="100" height="15" rx="4" fill="#6D4829" />

      <!-- Stage-based rendering -->
      <!-- Seed (stage 1) -->
      <ellipse v-if="stage >= 1" cx="100" cy="185" rx="10" ry="8" fill="#5B8C3E" />

      <!-- Sprout (stage 2) -->
      <line v-if="stage >= 2" x1="100" y1="185" x2="100" y2="135" stroke="#5B8C3E" stroke-width="4" stroke-linecap="round" />
      <ellipse v-if="stage >= 2" cx="100" cy="130" rx="12" ry="6" fill="#7AB85E" />
      <ellipse v-if="stage >= 2" cx="88" cy="138" rx="8" ry="4" fill="#7AB85E" />
      <ellipse v-if="stage >= 2" cx="112" cy="138" rx="8" ry="4" fill="#7AB85E" />

      <!-- Young (stage 3) -->
      <line v-if="stage >= 3" x1="100" y1="185" x2="100" y2="100" stroke="#4A7A32" stroke-width="5" stroke-linecap="round" />
      <line v-if="stage >= 3" x1="100" y1="130" x2="75" y2="105" stroke="#4A7A32" stroke-width="3" stroke-linecap="round" />
      <line v-if="stage >= 3" x1="100" y1="130" x2="125" y2="105" stroke="#4A7A32" stroke-width="3" stroke-linecap="round" />
      <ellipse v-if="stage >= 3" cx="100" cy="95" rx="18" ry="10" fill="#5B8C3E" />
      <ellipse v-if="stage >= 3" cx="72" cy="100" rx="12" ry="7" fill="#5B8C3E" />
      <ellipse v-if="stage >= 3" cx="128" cy="100" rx="12" ry="7" fill="#5B8C3E" />

      <!-- Mature (stage 4) -->
      <line v-if="stage >= 4" x1="100" y1="185" x2="100" y2="70" stroke="#3D6B28" stroke-width="6" stroke-linecap="round" />
      <line v-if="stage >= 4" x1="100" y1="100" x2="65" y2="70" stroke="#3D6B28" stroke-width="4" stroke-linecap="round" />
      <line v-if="stage >= 4" x1="100" y1="100" x2="135" y2="70" stroke="#3D6B28" stroke-width="4" stroke-linecap="round" />
      <line v-if="stage >= 4" x1="100" y1="85" x2="80" y2="55" stroke="#3D6B28" stroke-width="3" stroke-linecap="round" />
      <line v-if="stage >= 4" x1="100" y1="85" x2="120" y2="55" stroke="#3D6B28" stroke-width="3" stroke-linecap="round" />
      <ellipse v-if="stage >= 4" cx="100" cy="65" rx="22" ry="12" fill="#4A7A32" />
      <ellipse v-if="stage >= 4" cx="60" cy="65" rx="14" ry="8" fill="#4A7A32" />
      <ellipse v-if="stage >= 4" cx="140" cy="65" rx="14" ry="8" fill="#4A7A32" />
      <ellipse v-if="stage >= 4" cx="78" cy="50" rx="10" ry="6" fill="#5B8C3E" />
      <ellipse v-if="stage >= 4" cx="122" cy="50" rx="10" ry="6" fill="#5B8C3E" />

      <!-- Bloomed (stage 5) -->
      <circle v-if="stage >= 5" cx="100" cy="38" r="6" fill="#FF6B6B" />
      <circle v-if="stage >= 5" cx="85" cy="45" r="5" fill="#FF8E8E" />
      <circle v-if="stage >= 5" cx="115" cy="45" r="5" fill="#FF8E8E" />
      <circle v-if="stage >= 5" cx="70" cy="52" r="4" fill="#FF6B6B" />
      <circle v-if="stage >= 5" cx="130" cy="52" r="4" fill="#FF6B6B" />
    </svg>

    <!-- Max level badge -->
    <div v-if="maxStage" class="badge">🌼 MAX LEVEL</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  stage: number;
  maxStage?: boolean;
}>();
</script>

<style scoped>
.plant-canvas {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.plant-svg {
  width: 200px;
  height: 250px;
}
.badge {
  margin-top: 0.5rem;
  background: linear-gradient(135deg, #f5af19, #f12711);
  color: #fff;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
}
</style>
