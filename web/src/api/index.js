import axios from "axios";

const API_URL = process.env.API_URL;

export function authenticate(userData) {
  return axios.post(`${API_URL}/login/`, userData);
}

export function register(userData) {
  return axios.post(`${API_URL}/register/`, userData);
}

export function getExperiments() {
  return axios.get(`${API_URL}/experiments/`);
}

export function getExperiment(experimentId) {
  return axios.get(`${API_URL}/experiments/${experimentId}/`);
}

export function newExperiment(exp, jwt) {
  return axios.post(`${API_URL}/experiments/`, exp, {
    headers: { Authorization: `Bearer: ${jwt}` }
  });
}
