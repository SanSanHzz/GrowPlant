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

router.beforeEach(async (to, _from, next) => {
  if (to.meta.requiresAuth) {
    const store = useUserStore();
    const authenticated = await store.fetchStatus();
    if (!authenticated) {
      return next({ name: "login" });
    }
  }
  next();
});

export default router;
