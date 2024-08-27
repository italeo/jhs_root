import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./views/Home.vue";
import DataPage from "./views/DataPage.vue"; // Assuming it's in the views folder
import GraphPage from "./views/GraphPage.vue"; // New GraphPage

const routes = [
  {
    path: "/",
    name: "HomePage",
    component: HomePage,
  },
  {
    path: "/data",
    name: "DataPage",
    component: DataPage,
  },
  {
    path: "/graphs",
    name: "GraphPage",
    component: GraphPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
