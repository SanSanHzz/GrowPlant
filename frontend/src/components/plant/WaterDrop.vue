<template>
  <div class="rain-container">
    <div v-for="d in drops" :key="d.key" class="drop" :style="d.style">
      <svg width="8" height="14" viewBox="0 0 8 14">
        <ellipse cx="4" cy="10" rx="3.5" ry="5" fill="#4FC3F7" opacity="0.8" />
        <ellipse cx="4" cy="6" rx="2.5" ry="3.5" fill="#81D4FA" opacity="0.6" />
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted } from "vue";

const props = defineProps<{ trigger: number }>();
const emit = defineEmits<{ done: [] }>();

interface DropData {
  key: number;
  style: Record<string, string>;
}

const drops = ref<DropData[]>([]);
let interval: ReturnType<typeof setInterval> | null = null;

function createDrop(): DropData {
  const id = Date.now() + Math.random();
  const left = Math.random() * 80 + 10; // 10% to 90%
  const delay = Math.random() * 0.5;
  return {
    key: id,
    style: {
      left: `${left}%`,
      animation: `rainfall ${2 + Math.random() * 2}s linear infinite`,
      animationDelay: `${delay}s`,
      opacity: "0",
    },
  };
}

function startRain() {
  const count = 30;
  drops.value = Array.from({ length: count }, () => createDrop());

  interval = setInterval(() => {
    drops.value = drops.value.map(() => createDrop());
  }, 3000);
}

function stopRain() {
  if (interval) {
    clearInterval(interval);
    interval = null;
  }
  drops.value = [];
  emit("done");
}

watch(
  () => props.trigger,
  (val) => {
    if (val === 0) return;
    startRain();
    setTimeout(() => {
      stopRain();
    }, 60000);
  },
);

onUnmounted(() => {
  stopRain();
});
</script>

<style scoped>
.rain-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 180px;
  overflow: hidden;
  pointer-events: none;
  z-index: 5;
}
.drop {
  position: absolute;
  top: -20px;
}

@keyframes rainfall {
  0% {
    opacity: 0;
    transform: translateY(0);
  }
  10% {
    opacity: 0.85;
  }
  90% {
    opacity: 0.3;
  }
  100% {
    opacity: 0;
    transform: translateY(200px);
  }
}
</style>
