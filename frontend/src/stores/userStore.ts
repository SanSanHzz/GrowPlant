import { defineStore } from "pinia";
import { ref } from "vue";
import {
  getAuthStatus,
  logout as apiLogout,
  type User,
} from "@/services/authService";

export const useUserStore = defineStore("user", () => {
  const user = ref<User | null>(null);
  const loading = ref(true);

  async function fetchStatus() {
    loading.value = true;
    const status = await getAuthStatus();
    user.value = status.user;
    loading.value = false;
    return status.authenticated;
  }

  async function logout() {
    await apiLogout();
    user.value = null;
  }

  return { user, loading, fetchStatus, logout };
});
