/*
  This file handles routing to different web pages, along with verifying auth for pages if needed.
  Pages are made up of components from the views folder.
*/

import Vue from "vue";
import VueRouter from "vue-router";
// import Router from 'vue-router'
import Home from "../views/Home.vue";
import Login from "../components/Login.vue";
import Settings from "../views/Settings.vue";
import store from "../store";
// import Assignment from "../views/Assignment";
import School from "../views/School";
import Student from "../views/Student";

Vue.use(VueRouter);

const routes = [
  {
    path: "/login/",
    name: "login",
    component: Login
  },
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/settings",
    name: "settings",
    component: Settings,
    beforeEnter(to, from, next) {
      if (store.getters.teacherStatus) {
        next();
      } else {
        next("/");
      }
    }
  },
  {
    path: "/school",
    name: "school",
    component: School,
    beforeEnter(to, from, next) {
      if (store.getters.teacherStatus) {
        next();
      } else {
        next("/");
      }
    }
  },
  {
    path: "/student/:id",
    name: "viewAccount",
    component: Student,
    beforeEnter(to, from, next) {
      if (store.getters.teacherStatus) {
        next();
      } else {
        next("/");
      }
    }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  {
    if (!store.getters.isAuthenticatedTest && to.fullPath !== "/login") {
      next("/login");
    } else {
      next();
    }
  }
});

export default router;
