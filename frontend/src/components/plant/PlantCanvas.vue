<template>
  <div class="plant-canvas">
    <svg viewBox="0 0 200 250" class="plant-svg">
      <!-- Pot -->
      <rect x="60" y="190" width="80" height="40" rx="6" fill="#8B5E3C" />
      <rect x="50" y="220" width="100" height="15" rx="4" fill="#6D4829" />

      <!-- Stage 1: Seed (continuous growth from 0 to 5 drops) -->
      <g v-if="stage >= 1">
        <ellipse
          cx="100" cy="185"
          :rx="10 + s * 5"
          :ry="8 + s * 3"
          :fill="'#5B8C3E'"
        />
        <!-- root grows in -->
        <line v-if="s > 0.2" x1="100" y1="190" x2="98" y2="198" :stroke-width="0.5 + s" stroke="#4A7A32" :opacity="s" />
        <line v-if="s > 0.2" x1="100" y1="190" x2="102" y2="198" :stroke-width="0.5 + s" stroke="#4A7A32" :opacity="s" />
      </g>

      <!-- Stage 2: Sprout (stem grows, leaves appear/expan) -->
      <g v-if="stage >= 2">
        <line
          x1="100" y1="185"
          :x2="100" :y2="185 - s * 60"
          :stroke-width="3 + s * 2"
          :stroke="color('#5B8C3E', 1)"
          stroke-linecap="round" />
        <!-- center leaf -->
        <ellipse
          :cx="100" :cy="185 - s * 60"
          :rx="10 + s * 6" :ry="5 + s * 3"
          :fill="color('#7AB85E', 1)" />
        <!-- side leaves appear at s > 0.3 -->
        <ellipse v-if="s > 0.3"
          cx="88" :cy="185 - s * 55"
          :rx="8 + s * 3" :ry="4 + s * 1.5"
          :fill="color('#7AB85E', 2)" :opacity="Math.min(1, s * 1.5)" />
        <ellipse v-if="s > 0.3"
          cx="112" :cy="185 - s * 55"
          :rx="8 + s * 3" :ry="4 + s * 1.5"
          :fill="color('#7AB85E', 2)" :opacity="Math.min(1, s * 1.5)" />
        <!-- tiny lower leaves at s > 0.6 -->
        <ellipse v-if="s > 0.6"
          cx="78" :cy="170 - s * 30"
          :rx="5 + s * 3" :ry="2.5 + s * 1.5"
          :fill="color('#8CCC6E', 2)" :opacity="(s - 0.6) * 2.5" />
        <ellipse v-if="s > 0.6"
          cx="122" :cy="170 - s * 30"
          :rx="5 + s * 3" :ry="2.5 + s * 1.5"
          :fill="color('#8CCC6E', 2)" :opacity="(s - 0.6) * 2.5" />
      </g>

      <!-- Stage 3: Young (trunk thickens, canopy expands) -->
      <g v-if="stage >= 3">
        <!-- Main trunk -->
        <line x1="100" y1="185" :x2="100" :y2="100 - s * 30"
          :stroke-width="5 + s * 3" stroke="#4A7A32" stroke-linecap="round" />
        <!-- Branches -->
        <line x1="100" :y1="130 - s * 15" x2="75" :y2="105 - s * 25"
          :stroke-width="3 + s * 2" stroke="#4A7A32" stroke-linecap="round" />
        <line x1="100" :y1="130 - s * 15" x2="125" :y2="105 - s * 25"
          :stroke-width="3 + s * 2" stroke="#4A7A32" stroke-linecap="round" />
        <!-- Secondary branches appear at s > 0.4 -->
        <line v-if="s > 0.4" x1="100" :y1="115 - s * 10" x2="82" y2="90"
          :stroke-width="2 + s" stroke="#4A7A32" stroke-linecap="round" :opacity="(s - 0.4) * 1.7" />
        <line v-if="s > 0.4" x1="100" :y1="115 - s * 10" x2="118" y2="90"
          :stroke-width="2 + s" stroke="#4A7A32" stroke-linecap="round" :opacity="(s - 0.4) * 1.7" />
        <!-- Foliage - grows continuously -->
        <ellipse cx="100" :cy="95 - s * 30"
          :rx="16 + s * 8" :ry="9 + s * 4"
          :fill="color('#5B8C3E', 2)" />
        <ellipse cx="72" :cy="100 - s * 20"
          :rx="10 + s * 5" :ry="6 + s * 3"
          :fill="color('#5B8C3E', 1)" />
        <ellipse cx="128" :cy="100 - s * 20"
          :rx="10 + s * 5" :ry="6 + s * 3"
          :fill="color('#5B8C3E', 1)" />
        <!-- More leaves at s > 0.5 -->
        <ellipse v-if="s > 0.5"
          cx="80" :cy="88 - s * 15"
          :rx="6 + s * 4" :ry="4 + s * 2"
          :fill="color('#6A994E', 2)" :opacity="(s - 0.5) * 2" />
        <ellipse v-if="s > 0.5"
          cx="120" :cy="88 - s * 15"
          :rx="6 + s * 4" :ry="4 + s * 2"
          :fill="color('#6A994E', 2)" :opacity="(s - 0.5) * 2" />
      </g>

      <!-- Stage 4: Mature (full canopy, thicker) -->
      <g v-if="stage >= 4">
        <line x1="100" y1="185" :x2="100" :y2="70 - s * 20"
          :stroke-width="6 + s * 3" stroke="#3D6B28" stroke-linecap="round" />
        <line x1="100" :y1="100 - s * 15" x2="65" :y2="70 - s * 20"
          :stroke-width="4 + s * 2" stroke="#3D6B28" stroke-linecap="round" />
        <line x1="100" :y1="100 - s * 15" x2="135" :y2="70 - s * 20"
          :stroke-width="4 + s * 2" stroke="#3D6B28" stroke-linecap="round" />
        <line x1="100" :y1="85 - s * 10" x2="80" :y2="55 - s * 15"
          :stroke-width="3 + s" stroke="#3D6B28" stroke-linecap="round" />
        <line x1="100" :y1="85 - s * 10" x2="120" :y2="55 - s * 15"
          :stroke-width="3 + s" stroke="#3D6B28" stroke-linecap="round" />
        <line v-if="s > 0.4" x1="100" y1="75" x2="55" y2="58"
          :stroke-width="2 + s" stroke="#2E5B1E" stroke-linecap="round" :opacity="(s - 0.4) * 1.7" />
        <line v-if="s > 0.4" x1="100" y1="75" x2="145" y2="58"
          :stroke-width="2 + s" stroke="#2E5B1E" stroke-linecap="round" :opacity="(s - 0.4) * 1.7" />
        <!-- Canopy -->
        <ellipse cx="100" :cy="65 - s * 15"
          :rx="20 + s * 6" :ry="11 + s * 3"
          :fill="color('#4A7A32', 3)" />
        <ellipse cx="60" :cy="65 - s * 10"
          :rx="12 + s * 4" :ry="7 + s * 2"
          :fill="color('#4A7A32', 2)" />
        <ellipse cx="140" :cy="65 - s * 10"
          :rx="12 + s * 4" :ry="7 + s * 2"
          :fill="color('#4A7A32', 2)" />
        <ellipse v-if="s > 0.5"
          cx="78" :cy="50 - s * 8"
          :rx="7 + s * 3" :ry="4 + s * 1.5"
          :fill="color('#5B8C3E', 1)" :opacity="(s - 0.5) * 2" />
        <ellipse v-if="s > 0.5"
          cx="122" :cy="50 - s * 8"
          :rx="7 + s * 3" :ry="4 + s * 1.5"
          :fill="color('#5B8C3E', 1)" :opacity="(s - 0.5) * 2" />
      </g>

      <!-- Stage 5: Bloomed (max canopy + more flowers) -->
      <g v-if="stage >= 5">
        <line x1="100" y1="185" :x2="100" :y2="40 - s * 10"
          :stroke-width="7 + s * 1.5" stroke="#2E5B1E" stroke-linecap="round" />
        <line x1="100" y1="80" x2="55" y2="55" stroke-width="4" stroke="#2E5B1E" stroke-linecap="round" />
        <line x1="100" y1="80" x2="145" y2="55" stroke-width="4" stroke="#2E5B1E" stroke-linecap="round" />
        <line x1="100" y1="65" x2="72" y2="40" stroke-width="3" stroke="#2E5B1E" stroke-linecap="round" />
        <line x1="100" y1="65" x2="128" y2="40" stroke-width="3" stroke="#2E5B1E" stroke-linecap="round" />
        <!-- Full canopy -->
        <ellipse cx="100" :cy="55 - s * 10" :rx="24 + s * 3" :ry="14 + s * 2" fill="#2E7D32" />
        <ellipse cx="55" :cy="55 - s * 5" rx="14" ry="8" fill="#388E3C" />
        <ellipse cx="145" :cy="55 - s * 5" rx="14" ry="8" fill="#388E3C" />
        <ellipse cx="75" :cy="42 - s * 5" rx="10" ry="6" fill="#388E3C" />
        <ellipse cx="125" :cy="42 - s * 5" rx="10" ry="6" fill="#388E3C" />
        <!-- Flowers: more blooms as s increases -->
        <circle cx="100" :cy="35 - s * 3" :r="5 + s * 0.5" fill="#FF6B6B" />
        <circle cx="85" :cy="40 - s * 2" :r="4 + s * 0.3" fill="#FF8E8E" />
        <circle cx="115" :cy="40 - s * 2" :r="4 + s * 0.3" fill="#FF8E8E" />
        <circle cx="70" cy="48" :r="3 + s * 0.5" fill="#FF6B6B" :opacity="0.3 + s * 0.35" />
        <circle cx="130" cy="48" :r="3 + s * 0.5" fill="#FF6B6B" :opacity="0.3 + s * 0.35" />
        <!-- New flowers appear at s > 0.5 -->
        <circle v-if="s > 0.5" cx="60" cy="42" :r="2 + s * 0.5" fill="#FFAA6B" :opacity="(s - 0.5) * 2" />
        <circle v-if="s > 0.5" cx="140" cy="42" :r="2 + s * 0.5" fill="#FFAA6B" :opacity="(s - 0.5) * 2" />
        <circle v-if="s > 0.7" cx="80" cy="32" :r="2.5 + s * 0.3" fill="#FFD54F" :opacity="(s - 0.7) * 3.3" />
        <circle v-if="s > 0.7" cx="120" cy="32" :r="2.5 + s * 0.3" fill="#FFD54F" :opacity="(s - 0.7) * 3.3" />
      </g>
    </svg>

    <div v-if="maxStage" class="badge">🌼 MAX LEVEL</div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  stage: number;
  subStage: number;
  maxStage?: boolean;
}>();

const s = computed(() => props.subStage);

function color(hex: string, _variant: number): string {
  return hex;
}
</script>

<script lang="ts">
export default {
  inheritAttrs: false,
};
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
  transition: all 0.5s ease;
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
