<template>
  <div class="transition-overlay" :class="{ active: visible }">
    <div class="glow"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{ trigger: number }>();
const emit = defineEmits<{ done: [] }>();
const visible = ref(false);
let timeout: ReturnType<typeof setTimeout> | null = null;

watch(
  () => props.trigger,
  (val) => {
    if (val === 0) return;
    visible.value = true;
    timeout = setTimeout(() => {
      visible.value = false;
      emit("done");
    }, 1200);
  },
);
</script>

<style scoped>
.transition-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
}
.transition-overlay.active {
  opacity: 1;
}
.glow {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(46, 160, 67, 0.6), transparent);
  animation: pulse 1.2s ease-out;
}
@keyframes pulse {
  0% { transform: scale(0.5); opacity: 1; }
  100% { transform: scale(2); opacity: 0; }
}
</style>
