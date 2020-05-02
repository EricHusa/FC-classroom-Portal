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
    path: "/view_assignment/:id",
    name: "viewAssignment",
    component: Assignment,
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticatedTest) {
        next("/login");
      } else {
        next();
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
