<template>
  <div class="login-page">
    <div class="card" v-if="!checking">
      <h1 class="title">GrowPlant</h1>
      <p class="subtitle">Your GitHub contributions come to life</p>
      <LoginButton />
    </div>
    <div v-else class="loading">Authenticating...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import LoginButton from "@/components/auth/LoginButton.vue";
import { useUserStore } from "@/stores/userStore";

const router = useRouter();
const userStore = useUserStore();
const checking = ref(false);

onMounted(async () => {
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");
  if (token) {
    localStorage.setItem("session_token", token);
    window.history.replaceState({}, "", "/");
    checking.value = true;
    const authenticated = await userStore.fetchStatus();
    if (authenticated) {
      router.push("/select-plant");
    } else {
      checking.value = false;
    }
  }
});
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--bg-primary);
}
.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 3rem 4rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 12px;
}
.title {
  font-size: 2.5rem;
  font-weight: 700;
}
.subtitle {
  color: var(--text-secondary);
  font-size: 1.125rem;
}
.loading { color: var(--text-secondary); font-size: 1.25rem; }
</style>
