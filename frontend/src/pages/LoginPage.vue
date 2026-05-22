<template>
  <div class="login-page">
    <div class="card">
      <h1 class="title">GrowPlant</h1>
      <p class="subtitle">Your GitHub contributions come to life</p>
      <LoginButton />
    </div>
  </div>
</template>

<script setup lang="ts">
import LoginButton from "@/components/auth/LoginButton.vue";
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
</style>
