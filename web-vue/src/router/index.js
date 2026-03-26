import { createRouter, createWebHistory } from "vue-router";
import AdminLayout from "../layouts/AdminLayout.vue";
import UserLayout from "../layouts/UserLayout.vue";

const routes = [
  {
    path: "/login",
    component: () => import("../views/Login.vue"),
    meta: { title: "用户登陆" },
  },
  {
    path: "/register",
    component: () => import("../views/Register.vue"),
    meta: { title: "用户注册" },
  },
  {
    path: "/admin-login",
    component: () => import("../views/AdminLogin.vue"),
    meta: { title: "管理员登陆" },
  },
  {
    path: "/",
    component: UserLayout,
    meta: { requiresAuth: true, requiresUser: true },
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

// 路由守卫
router.beforeEach((to, from, next) => {
  const currentUser = JSON.parse(localStorage.getItem("currentUser") || "null");

  if (to.meta.requiresAuth) {
    if (!currentUser) {
      // 未登陆，根据需要的角色重定向
      if (to.meta.requiresAdmin) {
        next("/admin-login");
      } else {
        next("/login");
      }
      return;
    }

    // 检查权限
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
