import Vue from "vue";
import Vuex from "vuex";

// imports of AJAX functions will go here
import {
  getExperiment,
  getExperiments,
  getDevice,
  newExperiment,
  authenticate,
  register
} from "../api";
import { isValidJwt, EventBus } from "../utils/index.js";

Vue.use(Vuex);

const state = {
  // single source of data
  jwt: "",
  experiments: [],
  currentExperiment: {},
  role: "guest",
  device: "8a0118e3-a6bf-4ace-85c4-a7c824da3f0c",
  activeClass: null,
  studentList: [],
  currentUser: null
};

const actions = {
  // asynchronous operations
  loadExperiments(context) {
    return getExperiments().then(response => {
      context.commit("setExperiments", { experiments: response.data });
    });
  },
  loadExperiment(context, { id }) {
    return getExperiment(id).then(response => {
      context.commit("setExperiment", { experiment: response.data });
    });
  },
  login(context, userData) {
    context.commit("setUserData", { userData });
    return authenticate(userData)
      .then(response => context.commit("setJwtToken", { jwt: response.data }))
      .catch(error => {
        //console.log("Error Authenticating: ", error);
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
    return getDevice().then(response => {
      state.device = response;
    });
  },
  clearState() {}
};

const mutations = {
  // isolated data mutations
  setExperiments(state, payload) {
    state.experiments = payload.experiments;
  },
  setExperiment(state, payload) {
    state.currentExperiment = payload.experiment;
  },
  setUserData(state, payload) {
    //console.log("setUserData payload = ", payload);
    state.userData = payload.userData;
  },
  setJwtToken(state, payload) {
    //console.log("setJwtToken payload = ", payload);
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
  isAuthenticated(state) {
    return isValidJwt(state.jwt.token);
  },
  isAuthenticatedTest(state) {
    if (state.role != "guest") {
      return true;
    } else {
      return false;
    }
  },
  teacherStatus(state) {
    return state.role == "teacher";
  },
  getRole(state) {
    return state.role;
  }
};

// export default new Vuex.Store({
//   state,
//   mutations,
//   actions,
//   modules //getters
// });

const store = new Vuex.Store({
  state,
  actions,
  mutations,
  getters
});

export default store;
