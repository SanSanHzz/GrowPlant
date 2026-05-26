<template>
  <div v-if="active" class="rain-overlay">
    <div class="cloud"></div>
    <div class="drops">
      <span v-for="i in 12" :key="i" class="drop" :style="dropStyle(i)"></span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted } from "vue";

const props = defineProps<{ trigger: number }>();
const emit = defineEmits<{ done: [] }>();

const active = ref(false);
let timeout: ReturnType<typeof setTimeout> | null = null;

function dropStyle(i: number) {
  return {
    left: `${8 + (i * 8) % 90}%`,
    animationDelay: `${i * 0.4}s`,
    animationDuration: `${1.5 + (i % 3) * 0.5}s`,
  };
}

watch(
  () => props.trigger,
  (val) => {
    if (val === 0) return;
    if (timeout) clearTimeout(timeout);
    active.value = true;
    timeout = setTimeout(() => {
      active.value = false;
      emit("done");
    }, 300000);
  },
);

onUnmounted(() => {
  if (timeout) clearTimeout(timeout);
});
</script>

<style scoped>
.rain-overlay {
  position: absolute;
  top: -20px;
  left: -10px;
  width: calc(100% + 20px);
  height: 220px;
  overflow: hidden;
  pointer-events: none;
  z-index: 5;
}
.cloud {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 30px;
  background: radial-gradient(ellipse, rgba(100,181,246,0.5) 0%, transparent 70%);
  border-radius: 50%;
  animation: cloud-pulse 2s ease-in-out infinite;
}
.drops {
  position: absolute;
  top: 10px;
  left: 0;
  width: 100%;
  height: 200px;
}
.drop {
  position: absolute;
  top: 0;
  width: 8px;
  height: 14px;
  background: radial-gradient(ellipse at center, #64B5F6 0%, #2196F3 100%);
  border-radius: 50% 50% 50% 50% / 40% 40% 60% 60%;
  animation: fall linear infinite;
  opacity: 0;
}
@keyframes fall {
  0%   { opacity: 0; transform: translateY(0); }
  5%   { opacity: 0.8; }
  90%  { opacity: 0.3; }
  100% { opacity: 0; transform: translateY(200px); }
}
@keyframes cloud-pulse {
  0%, 100% { transform: translateX(-50%) scale(1); }
  50% { transform: translateX(-50%) scale(1.15); }
}
</style>
