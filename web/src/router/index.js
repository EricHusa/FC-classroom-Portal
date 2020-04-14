import Vue from "vue";
import VueRouter from "vue-router";
// import Router from 'vue-router'
import Home from "../views/Home.vue";
import Login from "../components/Login.vue";
import Settings from "../views/Settings.vue";
import store from "../store";
import Assignment from "../views/Assignment";
import School from "../views/School";

Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "login",
    component: Login
  },
  {
    path: "/",
    name: "home",
    component: Home,
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticatedTest) {
        next("/login");
      } else {
        next("/home");
      }
    }
  },
  {
    path: "/settings",
    name: "settings",
    component: Settings
  },
  {
    path: "/school",
    name: "school",
    component: School
  },
  {
    path: "/view_assignment/:id",
    name: "viewAssignment",
    component: Assignment
  },
  {
    path: "/home",
    name: "landing",
    component: Home
  }

  // {
  //   path: "/teacher",
  //   name: "teacher",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/Teacher.vue")
  // },
  // {
  //   path: "/student",
  //   name: "student",
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/Student.vue")
  // }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
