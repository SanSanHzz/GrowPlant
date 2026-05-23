<template>
  <div class="water-drop" :class="{ active: visible }">
    <svg width="20" height="30" viewBox="0 0 20 30">
      <ellipse cx="10" cy="20" rx="8" ry="10" fill="#4FC3F7" opacity="0.8" />
      <ellipse cx="10" cy="12" rx="5" ry="6" fill="#81D4FA" opacity="0.6" />
    </svg>
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
    }, 800);
  },
);

defineExpose({ reset: () => (visible.value = false) });
</script>

<style scoped>
.water-drop {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.2s, transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  pointer-events: none;
}
.water-drop.active {
  opacity: 1;
  transform: translateX(-50%) translateY(180px);
}
</style>
