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

export default {
  getClasses: function () {
      return [
        {
          name: "Class 1",
          id: "232139",
          students: ['JJ9','WB2','WT23','BB10','CK30']
        },
        {
          name: "Class 2",
          id: "635260",
          students: ['DB12','NB5','AD28','JB1']
        }
      ]
    },
  getSchool: function () {
      return "1199802"
    },
  getAssignments(frequency) {
    let repeating = {
      assignments: [
        {
          id: "1",
          experiment: "ex1",
          student: "12635",
          name: "Height Measurement",
          end_date: "05/25/2020",
          date_recorded: "",
          frequency: "7",
          type: "int",
          description: "Please record the height of the plant",
          observation: "",
          notes: ""
        },
        {
          id: "2",
          experiment: "ex1",
          student: "12635",
          name: "Color Observation",
          end_date: "05/25/2020",
          date_recorded: "",
          frequency: "14",
          type: "str",
          description: "Please record the color of the plant",
          observation: "",
          notes: ""
        }
      ]
    };

    const singular = [
      { title: "Smell the Flower", end_date: "03/05/2020", status: "complete" }
    ];

    if (frequency == "single") {
      return singular;
    } else if (frequency == "repeat") {
      return JSON.parse(repeating);
    } else return {};
    //return axios.get(`${API_URL}/assignments/`);
  }
};

export function getRepeatAssignments() {
  return axios.get(`${API_URL}/repeatAssignments/`);
}

export function newExperiment(exp, jwt) {
  return axios.post(`${API_URL}/experiments/`, exp, {
    headers: { Authorization: `Bearer: ${jwt}` }
  });
}
