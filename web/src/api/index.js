/*
  This file is where we connect to the backend, primarily to get datbase data.
  The base URL is set at the top of the file and is the address the backend makes itself public to.
  There is also a set of local variables. We use these as a sort of cache so that some data is readily available
  without having to request it from the database again.
*/

import axios from "axios";
import store from "../store/index";
const API_URL = "http://127.0.0.1:5000/api";

//Local storage for speed
let students = [];
let classes = [];
let experiments = [];
let assignments = [];
let assignment_responses = {};
let observations = [];
let observation_responses = [];
let devices = [];

let sludev = "8a0118e3-a6bf-4ace-85c4-a7c824da3f0c";

axios.defaults.validateStatus = () => {

    return status <= 400;
};

export function authenticate(userData) {
  return axios.post(`${API_URL}/login/`, userData);
}

export function register(userData) {
  return axios.post(`${API_URL}/register/`, userData);
}

export default {
  login(role, userData) {
    if (role === "student") {
      return Promise.resolve(axios.post(`${API_URL}/auth/student/login`, userData)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                store.state.currentTeacher = response.data.teacher.id;
                return (response.data.student);
            }
        }))
    }

    if (role === "teacher") {
      return Promise.resolve(axios.post(`${API_URL}/auth/teacher/login`, userData)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                JSON.stringify(response.data);
                return (response.data.teacher);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
    }
  },

  /// MISC FUNCTIONS

  getToday: function(d) {
    let fullDate = new Date(d);
    let dd = String(fullDate.getDate()).padStart(2, "0");
    let mm = String(fullDate.getMonth() + 1).padStart(2, "0"); //January is 0!
    let yyyy = fullDate.getFullYear();
    fullDate = yyyy + "-" + mm + "-" + dd;
    return fullDate;
  },
  generateUsername() {
    let username = "";
    let characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    for (let i = 0; i < 4; i++) {
      username += characters.charAt(
        Math.floor(Math.random() * characters.length)
      );
    }
    return username;
  },
  getDataArrays(rawData, type) {
    let temp = { units: null, name: type, data: [] };
    for (let i in rawData) {
      let record = rawData[i];
      if (record.attribute === type) {
        temp.units = record.units;
        break;
      }
    }
    for (let i in rawData) {
      let record = rawData[i];
      if (record.attribute === type) {
        temp.data.push({ x: record.ts, y: record.value });
      }
    }
    return temp;
  },

  /// FUNCTIONS FOR EXTERNAL API
    async getEnvironmentData(type, startDate, endDate){
    let rawData = await Promise.resolve(axios.get(`${API_URL}/external/observations/${sludev}/${startDate}/${endDate}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.observations
            }
        }))
    .catch(function(error) {
        throw (error);
    });
    let dataArrays = this.getDataArrays(rawData, type);
    return dataArrays;
    },

  /// FUNCTIONS FOR CLASSES

  setLocalClasses: function() {
    return Promise.resolve(axios.get(`${API_URL}/course/teacher/${store.state.currentTeacher}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                classes = response.data.courses;
                return(classes);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },

  getClasses: function() {
    return classes;
  },
  getClass: function(classId) {
    return classes.find(c => c.id === classId);
  },
  addClass: function() {
    let tempClass = {
      name: "New Class",
      teacher_username: store.state.currentUser.username,
      students: []
    };

    return Promise.resolve(axios.post(`${API_URL}/course`, tempClass)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                classes.push(response.data.course);
                return (response.data.course);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  deleteClass: function(classId) {
    return Promise.resolve(axios.delete(`${API_URL}/course/${classId}/teacher/${store.state.currentTeacher}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.message);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  updateClass: function(course) {
    return Promise.resolve(axios.put(`${API_URL}/course/${course.id}/teacher/${store.state.currentTeacher}`, course)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.course);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  getClassCheckboxes(){
    let newList = [{text: "All Classes", value:null}];
    let modifiedClass = {};
    for (let i in classes) {
      let thisClass = classes[i];
      modifiedClass = {
        text: thisClass.name,
        value: thisClass.id
      };
      newList.push(modifiedClass);
    }
    return newList;
  },

  /// FUNCTIONS FOR STUDENTS

  setLocalStudents(){
    return Promise.resolve(axios.get(`${API_URL}/student/teacher/${store.state.currentTeacher}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                students = response.data.students;
                return response.data.students;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  getStudents(classId = null) {
    if (classId === null) {
      return students;
    } else {
      let currentClass = this.getClass(classId)
      return currentClass.students;
    }
  },
  getStudentCheckboxes(scope=null, scopeId=null) {
    let newList = [];
    let modifiedStudent = {};
    let currentScope;
    if(scope === "experiment") {
      let exp = experiments.find(c => c.id === scopeId);
      currentScope = exp.students;
    }
    else if(scope === "class"){
      let thisClass = classes.find(c => c.id === scopeId);
      currentScope = thisClass.students;
    }
    else{
      currentScope = students;
    }

    for (let i in currentScope) {
      let student = currentScope[i];
      modifiedStudent = {
        text: student.username + ", " + student.fname + " " + student.lname,
        value: student.id
      };
      newList.push(modifiedStudent);
    }
    return newList;
  },
  getStudent(studentId) {
    let student = students.find(c => c.id === studentId);
    if (!student) {
      alert("This account does not exist");
    } else {
      return student;
    }
  },
  createStudent(student) {
    student.teacher_username = store.state.currentUser.username;
    return Promise.resolve(axios.post(`${API_URL}/auth/register/student`, student)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                students.push(response.data.student);
                return response.data.student;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  updateStudent(studentId, values) {
    return Promise.resolve(axios.put(`${API_URL}/account/student/${studentId}`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.student);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },

  deleteStudent: function(studentId) {
    return Promise.resolve(axios.delete(`${API_URL}/student/${studentId}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.message);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  getStudentDisplayName(studentId) {
    if (store.state.role==="teacher") {
      return "teacher";
    }
    let student = this.getStudent(studentId);
    return student.username + ", " + student.fname + " " + student.lname;
  },
    getStudentIdList(studentList){
      let student_ids = [];
      let student;
      for(let i in studentList){
          student = studentList[i];
          student_ids.push(student.id);
      }
      return student_ids;
    },

  /// FUNCTIONS FOR EXPERIMENTS

  setLocalExperiments(){
    return Promise.resolve(axios.get(`${API_URL}/experiment/${store.state.role}/${store.state.currentUser.id}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                experiments = (response.data.experiments).map(item => {
                    let tmp = item;
                    tmp.start_date = ((item.start_date).split(' '))[0];
                    return tmp;
                });
                return experiments;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  getExperiments() {
    return experiments;
  },
  getExperiment: function(id) {
    for (let e in experiments) {
      let exp = experiments[e];
      if (exp.id === id) {
        return exp;
      }
    }
    return null;
  },
  createExperiment: function(values) {
    return Promise.resolve(axios.post(`${API_URL}/experiment/teacher/${store.state.currentTeacher}`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                experiments.unshift(response.data.experiment);
                return response.data.experiment;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  updateExperiment: function(experimentId, values) {
    return Promise.resolve(axios.put(`${API_URL}/experiment/${experimentId}/teacher/${store.state.currentTeacher}`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.experiment);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  deleteExperiment: function(experimentId) {
    return Promise.resolve(axios.delete(`${API_URL}/experiment/${experimentId}/teacher/${store.state.currentTeacher}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.message);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },

  /// FUNCTIONS FOR ASSIGNMENTS

    setLocalAssignments(){
    return Promise.resolve(axios.get(`${API_URL}/assignment/${store.state.role}/${store.state.currentUser.id}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                // alert(JSON.stringify(response.data))
                assignments = (response.data.assignments).map(item => {
                    let tmp = item;
                    tmp.due_date = ((item.due_date).split(' '))[0];
                    return tmp;
                });

                // assignments = response.data.assignments;
                return response.data.assignments;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  getAssignment(assignmentId) {
    for (let a in assignments) {
      let assign = assignments[a];
      if (assign.id === assignmentId) {
        return assign;
      }
    }
    return null;
  },
  async createAssignment(values) {
    let assignment = await Promise.resolve(axios.post(`${API_URL}/assignment/teacher/${store.state.currentTeacher}`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                assignments.unshift(response.data.assignment);
                return response.data.assignment;
            }
        }))
    .catch(function(error) {
        throw (error);
    });

    let resp_values;
    for (let index in values.student_ids){
        resp_values = {student_id: values.student_ids[index], response: ""};
        await this.createAssignmentResponse(assignment.id, resp_values);
    }

    return assignment;
  },
  updateAssignment(assignmentId, values) {
      return Promise.resolve(axios.put(`${API_URL}/assignment/${assignmentId}/teacher/${store.state.currentTeacher}`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.assignment);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  deleteAssignment(assignmentId){
    return Promise.resolve(axios.delete(`${API_URL}/assignment/${assignmentId}/teacher/${store.state.currentTeacher}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.message);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
    getApiStudentAssignmentResponse(assignmentId,studentId){
      return Promise.resolve(axios.get(`${API_URL}/assignment/${assignmentId}/response/student/${studentId}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.assignment_response;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
    },
  async setLocalStudentAssignmentResponses(studentId) {
    let assignment;
    let res;
    for (let i in assignments) {
        assignment = assignments[i];
        res = await this.getApiStudentAssignmentResponse(assignment.id,studentId).then(function(response) {
        return response;
      }).catch(function (error) {
        throw(error);
      });
        assignment_responses[assignment.id] = res;
    }
    return assignment_responses;
  },

  getTeacherAssignmentResponses(assignmentId) {
  return Promise.resolve(axios.get(`${API_URL}/assignment/${assignmentId}/response`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.assignment_response;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  getStudentAssignmentResponse(assignmentId) {
    return assignment_responses[assignmentId];
  },
  updateStudentAssignmentResponse(assignmentId, responseId, values) {
    return Promise.resolve(axios.put(`${API_URL}/assignment/${assignmentId}/response/${responseId}/student/${store.state.currentUser.id}`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.assignment_response);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
    createAssignmentResponse(assignmentId, values){
    return Promise.resolve(axios.post(`${API_URL}/assignment/${assignmentId}/response`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.assignment_response);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
    },
  addCommentToAssignment(assignmentId, responseId, value){
      return Promise.resolve(axios.put(`${API_URL}/assignment/${assignmentId}/response/${responseId}/teacher/${store.state.currentUser.id}`, {comments: value})
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.assignment_response.id);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },

  /// FUNCTIONS FOR OBSERVATIONS

    setLocalObservations(){
    return Promise.resolve(axios.get(`${API_URL}/observation/experiment/${store.state.currentExperiment.id}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                observations = response.data.observations;
                return response.data.observations;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  getObservation(observationId) {
      return Promise.resolve(axios.get(`${API_URL}/observation/${observationId}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.observation;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  updateObservation(observationId, values) {
      return Promise.resolve(axios.put(`${API_URL}/observation/${observationId}`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.observation;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  createObservation(values) {
    let obs = {};
    obs.experiment_id = store.state.currentExperiment.id;
    obs.title = values.title;
    obs.description = values.description;
    obs.type = values.type;
    obs.units = values.units;
    obs.student_ids = values.collaborators;

    let observation = Promise.resolve(axios.post(`${API_URL}/observation`, obs)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.observation;
            }
        }))
    .catch(function(error) {
        throw (error);
    });

    observations.unshift(observation);
    return observation;
  },
  deleteObservation(observationId) {
    return Promise.resolve(axios.delete(`${API_URL}/observation/${observationId}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.status;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
    getObservationResponses(observationId){
        return Promise.resolve(axios.get(`${API_URL}/observation/${observationId}/response`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.responses;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
    },
  addObservationResponse(observationId) {
    let res = {
      response: "",
      editable: true
    };

    let obsResponse =  Promise.resolve(axios.post(`${API_URL}/observation/${observationId}/response`, res)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.response;
            }
        }))
    .catch(function(error) {
        throw (error);
    });

    observation_responses.push(obsResponse);
    return obsResponse;
  },
  updateObservationResponse(observationId, responseNumber, studentId, value) {
    let obs = this.getObservation(observationId);
    let responseIndex = obs.responses
      .map(function(e) {
        return e.number;
      })
      .indexOf(responseNumber);
    let response = obs.responses[responseIndex];

    response.response = value;
    response.submitted = this.getToday(new Date());
    response.student = this.getStudentDisplayName(studentId);
    return obs;
  },
  updateObservationResponseLock(observationId, responseNumber) {
    let obs = this.getObservation(observationId);
    let responseIndex = obs.responses
      .map(function(e) {
        return e.number;
      })
      .indexOf(responseNumber);
    obs.responses[responseIndex].editable = !obs.responses[responseIndex]
      .editable;
    return obs;
  },
  deleteObservationResponse(observationId, responseId) {
    return Promise.resolve(axios.delete(`${API_URL}/observation/${observationId}/response/${responseId}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return response.data.message;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },

  /// FUNCTIONS FOR DEVICES

    setLocalDevices(){
      return Promise.resolve(axios.get(`${API_URL}/device/teacher/${store.state.currentTeacher}`)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                devices = response.data.devices;
                return response.data.devices;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
    },
  getDevices() {
    return devices;
  },
  updateDeviceName(deviceId, newName) {
    return Promise.resolve(axios.put(`${API_URL}/device/${deviceId}/teacher/${store.state.currentTeacher}`, {name: newName})
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.device);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  verifyDevice(deviceId) {
    if (deviceId==="bad",deviceId===""||deviceId===null||deviceId===undefined) {
        return false;
    }
    return true;
  },
  registerDevice(values) {
      return Promise.resolve(axios.post(`${API_URL}/device`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                let device = response.data.device
                delete device.teacher;
                devices.push(device);
                return device;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },

  /// FUNCTIONS FOR TEACHERS

    updateTeacher(values){
     return Promise.resolve(axios.put(`${API_URL}/account/teacher/${store.state.currentTeacher}`, values)
        .then(function(response) {
            if (response.data.status === "fail") {
                throw (response.data.message);
            } else {
                return (response.data.teacher);
            }
        }))
    .catch(function(error) {
        throw (error);
    });
},
  registerTeacher(values) {
    let deviceId = values.id;
    if (this.verifyDevice(deviceId)) {
      values.username = this.generateUsername();
      return Promise.resolve(axios.post(`${API_URL}/auth/register/teacher`, values)
          .then(function (response) {
            if (response.data.status === "fail") {
              throw(response.data.message);
            } else {
              return (response.data.teacher);
            }
          }))
          .catch(function (error) {
            throw(error);
          });
    }
    else{
      throw "invalid device ID";
    }
  }
};

export function newExperiment(exp, jwt) {
  return axios.post(`${API_URL}/experiments/`, exp, {
    headers: { Authorization: `Bearer: ${jwt}` }
  });
}
