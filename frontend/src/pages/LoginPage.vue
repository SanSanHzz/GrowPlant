<template>
  <div class="login-page">
    <div class="card" v-if="!checking">
      <h1 class="title">GrowPlant</h1>
      <p class="subtitle">Your GitHub contributions come to life</p>
      <p v-if="error" class="error">{{ error }}</p>
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
const error = ref("");

onMounted(async () => {
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");

  const errMsg = params.get("error");
  if (errMsg) {
    error.value = decodeURIComponent(errMsg.replace(/\+/g, " "));
    window.history.replaceState({}, "", "/");
  }

  if (token) {
    localStorage.setItem("session_token", token);
    checking.value = true;
    window.location.href = "/select-plant";
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
  max-width: 480px;
}
.title {
  font-size: 2.5rem;
  font-weight: 700;
}
.subtitle {
  color: var(--text-secondary);
  font-size: 1.125rem;
}
.error {
  color: var(--danger);
  font-size: 0.875rem;
  text-align: center;
  word-break: break-word;
}
.loading { color: var(--text-secondary); font-size: 1.25rem; }
</style>
