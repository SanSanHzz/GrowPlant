<template>
  <div class="plant-canvas">
    <svg viewBox="0 0 200 250" class="plant-svg">
      <!-- Pot -->
      <rect x="60" y="190" width="80" height="40" rx="6" fill="#8B5E3C" />
      <rect x="50" y="220" width="100" height="15" rx="4" fill="#6D4829" />

      <!-- Stage 1: Seed (sub 0-2 = bigger seed) -->
      <g v-if="stage >= 1">
        <ellipse
          cx="100" cy="185"
          :rx="10 + subStage * 3"
          :ry="8 + subStage * 2"
          fill="#5B8C3E"
        />
        <!-- tiny root visible at sub=2 -->
        <line v-if="subStage >= 2" x1="100" y1="190" x2="98" y2="198" stroke="#4A7A32" stroke-width="1.5" />
        <line v-if="subStage >= 2" x1="100" y1="190" x2="102" y2="198" stroke="#4A7A32" stroke-width="1.5" />
      </g>

      <!-- Stage 2: Sprout (sub 0-2: growing stem + leaves) -->
      <g v-if="stage >= 2">
        <line v-if="subStage >= 0"
          x1="100" y1="185"
          :x2="100" :y2="135 - subStage * 15"
          :stroke-width="3 + subStage"
          stroke="#5B8C3E" stroke-linecap="round" />
        <ellipse v-if="subStage >= 0"
          cx="100" :cy="130 - subStage * 15"
          :rx="10 + subStage * 3" :ry="5 + subStage * 2"
          fill="#7AB85E" />
        <ellipse v-if="subStage >= 1"
          cx="88" :cy="138 - subStage * 15"
          rx="8" ry="4" fill="#7AB85E" />
        <ellipse v-if="subStage >= 1"
          cx="112" :cy="138 - subStage * 15"
          rx="8" ry="4" fill="#7AB85E" />
        <ellipse v-if="subStage >= 2"
          cx="78" :cy="145 - subStage * 15"
          rx="6" ry="3" fill="#8CCC6E" />
        <ellipse v-if="subStage >= 2"
          cx="122" :cy="145 - subStage * 15"
          rx="6" ry="3" fill="#8CCC6E" />
      </g>

      <!-- Stage 3: Young (sub 0-2: thicker trunk, branches, denser foliage) -->
      <g v-if="stage >= 3">
        <line
          x1="100" y1="185"
          :x2="100" :y2="100 - subStage * 10"
          :stroke-width="5 + subStage"
          stroke="#4A7A32" stroke-linecap="round" />
        <line v-if="subStage >= 0"
          x1="100" :y1="130 - subStage * 5" x2="75" :y2="105 - subStage * 10"
          :stroke-width="3 + subStage * 0.5" stroke="#4A7A32" stroke-linecap="round" />
        <line v-if="subStage >= 0"
          x1="100" :y1="130 - subStage * 5" x2="125" :y2="105 - subStage * 10"
          :stroke-width="3 + subStage * 0.5" stroke="#4A7A32" stroke-linecap="round" />
        <!-- Extra branches at higher sub-stages -->
        <line v-if="subStage >= 1"
          x1="100" :y1="115 - subStage * 5" x2="82" y2="90"
          stroke-width="2.5" stroke="#4A7A32" stroke-linecap="round" />
        <line v-if="subStage >= 1"
          x1="100" :y1="115 - subStage * 5" x2="118" y2="90"
          stroke-width="2.5" stroke="#4A7A32" stroke-linecap="round" />
        <line v-if="subStage >= 2"
          x1="100" :y1="105" x2="70" y2="82"
          stroke-width="2" stroke="#3D6B28" stroke-linecap="round" />
        <line v-if="subStage >= 2"
          x1="100" :y1="105" x2="130" y2="82"
          stroke-width="2" stroke="#3D6B28" stroke-linecap="round" />
        <!-- Foliage -->
        <ellipse v-if="subStage >= 0"
          cx="100" :cy="95 - subStage * 10"
          :rx="16 + subStage * 4" :ry="9 + subStage * 2"
          fill="#5B8C3E" />
        <ellipse v-if="subStage >= 0"
          cx="72" :cy="100 - subStage * 8" rx="10" ry="6" fill="#5B8C3E" />
        <ellipse v-if="subStage >= 0"
          cx="128" :cy="100 - subStage * 8" rx="10" ry="6" fill="#5B8C3E" />
        <ellipse v-if="subStage >= 1"
          cx="80" :cy="88 - subStage * 5" rx="8" ry="5" fill="#6A994E" />
        <ellipse v-if="subStage >= 1"
          cx="120" :cy="88 - subStage * 5" rx="8" ry="5" fill="#6A994E" />
        <ellipse v-if="subStage >= 2"
          cx="68" cy="78" rx="6" ry="4" fill="#6A994E" />
        <ellipse v-if="subStage >= 2"
          cx="132" cy="78" rx="6" ry="4" fill="#6A994E" />
      </g>

      <!-- Stage 4: Mature (sub 0-2: full canopy, thicker trunk) -->
      <g v-if="stage >= 4">
        <line
          x1="100" y1="185"
          :x2="100" :y2="70 - subStage * 5"
          :stroke-width="6 + subStage"
          stroke="#3D6B28" stroke-linecap="round" />
        <line v-if="subStage >= 0"
          x1="100" :y1="100 - subStage * 5" x2="65" :y2="70 - subStage * 5"
          :stroke-width="4 + subStage * 0.3" stroke="#3D6B28" stroke-linecap="round" />
        <line v-if="subStage >= 0"
          x1="100" :y1="100 - subStage * 5" x2="135" :y2="70 - subStage * 5"
          :stroke-width="4 + subStage * 0.3" stroke="#3D6B28" stroke-linecap="round" />
        <line v-if="subStage >= 0"
          x1="100" :y1="85 - subStage * 3" x2="80" :y2="55 - subStage * 3"
          stroke-width="3" stroke="#3D6B28" stroke-linecap="round" />
        <line v-if="subStage >= 0"
          x1="100" :y1="85 - subStage * 3" x2="120" :y2="55 - subStage * 3"
          stroke-width="3" stroke="#3D6B28" stroke-linecap="round" />
        <line v-if="subStage >= 1"
          x1="100" :y1="75" x2="55" y2="58"
          stroke-width="2.5" stroke="#2E5B1E" stroke-linecap="round" />
        <line v-if="subStage >= 1"
          x1="100" :y1="75" x2="145" y2="58"
          stroke-width="2.5" stroke="#2E5B1E" stroke-linecap="round" />
        <line v-if="subStage >= 2"
          x1="100" :y1="68" x2="70" y2="45"
          stroke-width="2" stroke="#2E5B1E" stroke-linecap="round" />
        <line v-if="subStage >= 2"
          x1="100" :y1="68" x2="130" y2="45"
          stroke-width="2" stroke="#2E5B1E" stroke-linecap="round" />
        <!-- Dense canopy -->
        <ellipse v-if="subStage >= 0"
          cx="100" :cy="65 - subStage * 5"
          :rx="20 + subStage * 4" :ry="11 + subStage * 2"
          fill="#4A7A32" />
        <ellipse v-if="subStage >= 0"
          cx="60" :cy="65 - subStage * 4" :rx="12 + subStage * 2" :ry="7 + subStage" fill="#4A7A32" />
        <ellipse v-if="subStage >= 0"
          cx="140" :cy="65 - subStage * 4" :rx="12 + subStage * 2" :ry="7 + subStage" fill="#4A7A32" />
        <ellipse v-if="subStage >= 1"
          cx="78" :cy="50 - subStage * 2" rx="9" ry="5" fill="#5B8C3E" />
        <ellipse v-if="subStage >= 1"
          cx="122" :cy="50 - subStage * 2" rx="9" ry="5" fill="#5B8C3E" />
        <ellipse v-if="subStage >= 2"
          cx="65" cy="45" rx="7" ry="4" fill="#6A994E" />
        <ellipse v-if="subStage >= 2"
          cx="135" cy="45" rx="7" ry="4" fill="#6A994E" />
      </g>

      <!-- Stage 5: Bloomed (sub 0-2: more flowers, brighter colors) -->
      <g v-if="stage >= 5">
        <line
          x1="100" y1="185"
          :x2="100" :y2="40 - subStage * 3"
          :stroke-width="7 + subStage * 0.3"
          stroke="#2E5B1E" stroke-linecap="round" />
        <line x1="100" y1="80" x2="55" y2="55" stroke-width="4" stroke="#2E5B1E" stroke-linecap="round" />
        <line x1="100" y1="80" x2="145" y2="55" stroke-width="4" stroke="#2E5B1E" stroke-linecap="round" />
        <line x1="100" y1="65" x2="72" y2="40" stroke-width="3" stroke="#2E5B1E" stroke-linecap="round" />
        <line x1="100" y1="65" x2="128" y2="40" stroke-width="3" stroke="#2E5B1E" stroke-linecap="round" />
        <line x1="100" y1="55" x2="60" y2="32" stroke-width="2.5" stroke="#1B4D1B" stroke-linecap="round" />
        <line x1="100" y1="55" x2="140" y2="32" stroke-width="2.5" stroke="#1B4D1B" stroke-linecap="round" />
        <!-- Full canopy -->
        <ellipse cx="100" :cy="55 - subStage * 3" rx="24" ry="14" fill="#2E7D32" />
        <ellipse cx="55" :cy="55 - subStage * 2" rx="14" ry="8" fill="#2E7D32" />
        <ellipse cx="145" :cy="55 - subStage * 2" rx="14" ry="8" fill="#2E7D32" />
        <ellipse cx="75" :cy="42 - subStage * 2" rx="10" ry="6" fill="#388E3C" />
        <ellipse cx="125" :cy="42 - subStage * 2" rx="10" ry="6" fill="#388E3C" />
        <!-- Flowers (more at higher sub-stages) -->
        <circle cx="100" :cy="35 - subStage" r="5" fill="#FF6B6B" />
        <circle cx="85" :cy="40 - subStage" r="4" fill="#FF8E8E" />
        <circle cx="115" :cy="40 - subStage" r="4" fill="#FF8E8E" />
        <circle v-if="subStage >= 0" cx="70" cy="48" r="4" fill="#FF6B6B" />
        <circle v-if="subStage >= 0" cx="130" cy="48" r="4" fill="#FF6B6B" />
        <circle v-if="subStage >= 1" cx="60" cy="42" r="3" fill="#FFAA6B" />
        <circle v-if="subStage >= 1" cx="140" cy="42" r="3" fill="#FFAA6B" />
        <circle v-if="subStage >= 2" cx="80" cy="32" r="3.5" fill="#FFD54F" />
        <circle v-if="subStage >= 2" cx="120" cy="32" r="3.5" fill="#FFD54F" />
      </g>
    </svg>

    <!-- Max level badge -->
    <div v-if="maxStage" class="badge">🌼 MAX LEVEL</div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  stage: number;
  subStage: number;
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
