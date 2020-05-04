import Vue from "vue";
import Vuex from "vuex";

import { newExperiment, authenticate, register } from "../api";
import { EventBus } from "../utils/index.js";

Vue.use(Vuex);

const state = {
  // single source of data
  jwt: "",
  currentExperiment: null, //Set when clicked on
  currentTeacher: null, //Set on login
  role: "guest", //Set on login
  currentUser: null //Set on login
};

const actions = {
  // asynchronous operations
  login(context, userData) {
    context.commit("setUserData", { userData });
    return authenticate(userData)
      .then(response => context.commit("setJwtToken", { jwt: response.data }))
      .catch(error => {
        EventBus.emit("failedAuthentication", error);
      });
  },
  register(context, userData) {
    context.commit("setUserData", { userData });
    return register(userData)
      .then(context.dispatch("login", userData))
      .catch(error => {
        //console.log("Error Registering: ", error);
        EventBus.emit("failedRegistering: ", error);
      });
  },
  createExperiment(context, survey) {
    return newExperiment(survey, context.state.jwt.token);
  },
  dev(context, value) {
    context.commit("setRole", value);
    context.commit("setUser");
  },
  device() {
  }
};

const mutations = {
  // isolated data mutations
  setUserData(state, payload) {
    state.userData = payload.userData;
  },
  setJwtToken(state, payload) {
    localStorage.token = payload.jwt.token;
    state.jwt = payload.jwt;
  },
  setRole(state, payload) {
    state.role = payload;
  },
  setUser(state) {
    state.currentUser = 34589798;
  }
};

const getters = {
  // reusable data accessors
  isAuthenticatedTest(state) {
    if (state.role !== "guest") {
      return true;
    } else {
      return false;
    }
  },
  teacherStatus(state) {
    return state.role === "teacher";
  }
};

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
});

export default store;
