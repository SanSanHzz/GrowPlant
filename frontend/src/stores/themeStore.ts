import { defineStore } from "pinia";
import { ref, watch } from "vue";

export const useThemeStore = defineStore("theme", () => {
  const saved = localStorage.getItem("theme");
  const isDark = ref(saved !== "light");

  function apply() {
    document.documentElement.setAttribute(
      "data-theme",
      isDark.value ? "dark" : "light",
    );
  }

  function toggle() {
    isDark.value = !isDark.value;
    localStorage.setItem("theme", isDark.value ? "dark" : "light");
    apply();
  }

  watch(isDark, apply, { immediate: true });

  return { isDark, toggle };
});
