import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "@/stores/userStore";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "login",
      component: () => import("@/pages/LoginPage.vue"),
    },
    {
      path: "/select-plant",
      name: "plant-select",
      component: () => import("@/pages/PlantSelectPage.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: () => import("@/pages/DashboardPage.vue"),
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach(async (to) => {
  const token = localStorage.getItem("session_token");
  const store = useUserStore();

  if (to.meta.requiresAuth) {
    if (!token) return { name: "login" };
    const ok = await store.fetchStatus();
    if (!ok) {
      localStorage.removeItem("session_token");
      return { name: "login" };
    }
    return;
  }

  if (to.name === "login" && token) {
    const ok = await store.fetchStatus();
    if (ok) return { name: "dashboard" };
  }
});

export default router;
