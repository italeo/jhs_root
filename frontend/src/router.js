import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./views/Home.vue"; // Make sure this path is correct

const routes = [
  {
    path: "/",
    name: "HomePage",
    component: HomePage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes, // Ensure `routes` is used here
});

export default router;
