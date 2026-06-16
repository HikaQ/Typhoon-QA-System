import { createRouter, createWebHistory } from "vue-router";
import AdminLayout from "../layouts/AdminLayout.vue";
import UserLayout from "../layouts/UserLayout.vue";
import { getAuthToken, getCurrentUser } from "../utils/auth";

const routes = [
  {
    path: "/login",
    component: () => import("../views/Login.vue"),
    meta: { title: "用户登录" },
  },
  {
    path: "/register",
    component: () => import("../views/Register.vue"),
    meta: { title: "用户注册" },
  },
  {
    path: "/admin-login",
    component: () => import("../views/AdminLogin.vue"),
    meta: { title: "管理员登录" },
  },
  {
    path: "/",
    component: UserLayout,
    meta: { requiresAuth: true, requiresUser: true },
  },
  {
    path: "/profile",
    component: () => import("../views/Profile.vue"),
    meta: { requiresAuth: true, requiresUser: true, title: "个人中心" },
  },
  {
    path: "/admin",
    component: AdminLayout,
    redirect: "/admin/user",
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: "user", component: () => import("../views/User.vue") },
      { path: "log", component: () => import("../views/Log.vue") },
      { path: "setting", component: () => import("../views/Setting.vue") },
    ],
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/login",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const currentUser = getCurrentUser();
  const token = getAuthToken();

  if (to.meta.requiresAuth) {
    if (!currentUser || !token) {
      if (to.meta.requiresAdmin) {
        next("/admin-login");
      } else {
        next("/login");
      }
      return;
    }

    if (to.meta.requiresAdmin && currentUser.type !== "admin") {
      next("/admin-login");
      return;
    }

    if (to.meta.requiresUser && currentUser.type !== "user") {
      next("/login");
      return;
    }
  }

  next();
});

export default router;
