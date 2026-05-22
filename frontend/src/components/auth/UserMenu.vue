<template>
  <div v-if="user" class="user-menu">
    <img :src="user.avatar_url || ''" :alt="user.username" class="avatar" />
    <span class="username">{{ user.display_name || user.username }}</span>
    <button class="logout-btn" @click="$emit('logout')">Logout</button>
  </div>
</template>

<script setup lang="ts">
import type { User } from "@/services/authService";

defineProps<{ user: User | null }>();
defineEmits<{ logout: [] }>();
</script>

<style scoped>
.user-menu {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 1rem;
}
.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}
.username {
  font-weight: 500;
}
.logout-btn {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid var(--border);
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
}
.logout-btn:hover {
  color: var(--danger);
  border-color: var(--danger);
}
</style>
