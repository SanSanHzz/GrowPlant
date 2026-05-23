import { createRouter, createWebHistory } from "vue-router";

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
    },
    {
      path: "/dashboard",
      name: "dashboard",
      component: () => import("@/pages/DashboardPage.vue"),
    },
  ],
});

export default router;
