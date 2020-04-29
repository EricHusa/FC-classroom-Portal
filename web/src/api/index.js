import axios from "axios";
import ErrorMessages from "../constants/ErrorMessages.ts";
import store from "../store/index";
import SampleClimate from "../constants/SampleClimate.ts";
import SampleClimateData from "../constants/SampleClimateData.ts";
const API_URL = process.env.API_URL;

//sample database data
let students = [
  {
    fname: "Jon",
    lname: "Joe",
    username: "JJ09",
    password: "Peaches",
    id: 1,
    teacher: "a"
  },
  {
    fname: "Will",
    lname: "Billy",
    username: "WB02",
    password: "Cake",
    id: 2,
    teacher: "a"
  },
  {
    fname: "Drew",
    lname: "Blue",
    username: "DB12",
    password: "Orange",
    id: 3,
    teacher: "a"
  },
  {
    fname: "Bob",
    lname: "Cob",
    username: "b",
    password: "c",
    id: 4,
    teacher: "a"
  }
];

let experiments = [
  {
    title: "Example Experiment",
    description: "This is a sample experiment",
    plant: "basil",
    start_date: "2020-03-15",
    teacher: "a",
    students: [1, 4],
    id: 38782347,
    device: "8a0118e3-a6bf-4ace-85c4-a7c824da3f0c"
  },
  {
    title: "Another",
    description: "Another example experiment",
    plant: "tomato",
    start_date: "2020-03-18",
    teacher: "a",
    students: [1, 2, 3],
    id: 16847325,
    device: "8a0118e3-a6bf-4ace-85c4-a7c824da3f0c"
  }
];

let assignments = [
  {
    id: 35688201,
    teacher: "a",
    experiment: 38782347,
    title: "Predict How Many Days",
    description: "Predict how many days it takes the plant to grow 1 inch",
    type: "number",
    due_date: "2020-05-05",
    assignees: [2, 4]
  },
  {
    id: 25674621,
    teacher: "a",
    experiment: 38782347,
    title: "Give yourself a team role",
    description: "Tell me what your role on the team is",
    type: "text",
    due_date: "2020-05-04",
    assignees: [1, 2, 3, 4]
  }
];

let assignment_responses = [
  {
    assignment: 25674621,
    student: 1,
    response: "I want team Leader",
    submitted: "2020-05-03",
    comments: "Congratulations, you will be the team's Leader"
  },
  {
    assignment: 25674621,
    student: 2,
    response: "Gardener",
    submitted: "2020-05-03",
    comments: "Congratulations, you will be the team's Gardener"
  },
  {
    assignment: 25674621,
    student: 3,
    response: "Can I be the Record Keeper",
    submitted: "2020-05-04",
    comments: "Congratulations, you will be the team's Record Keeper"
  },
  {
    assignment: 25674621,
    student: 4,
    response: "I want to be the team Researcher",
    submitted: "2020-05-04",
    comments: "Congratulations, you will be the team's Researcher"
  },
  {
    assignment: 35688201,
    student: 2,
    response: null,
    submitted: "",
    comments: null
  },
  {
    assignment: 35688201,
    student: 4,
    response: null,
    submitted: "",
    comments: null
  }
];

let observations = [
  {
    id: 12835739,
    title: "Height Measurement",
    description:
      "Take your ruler and measure the height of the plant in centimeters",
    experiment: 38782347,
    type: "number",
    units: "centimeters",
    updated: "2020-05-01",
    collaborators: [1, 2, 4],
    responses: [
      {
        number: 1,
        response: "3",
        submitted: "2020-05-02",
        student: 4,
        editable: true
      },
      {
        number: 2,
        response: "3.1",
        submitted: "2020-05-03",
        student: 1,
        editable: true
      }
    ]
  }
];

let teachers = [{ fname: "Mr", lname: "Teacher", password: "a", id: "a" }];

let studentIdCounter = students.length;

let devices = [
  {
    name: "SLUdev1",
    fopd_id: "8a0118e3-a6bf-4ace-85c4-a7c824da3f0c",
    teacher: "a"
  }
];

let classes = [
  {
    name: "Class 1",
    id: 23213931,
    students: [1, 2]
  },
  {
    name: "Class 2",
    id: 63526050,
    students: [3, 4]
  }
];

export function authenticate(userData) {
  return axios.post(`${API_URL}/login/`, userData);
}

export function register(userData) {
  return axios.post(`${API_URL}/register/`, userData);
}

// export function getExperiments() {
//   return axios.get(`${API_URL}/experiments/`);
// }

// export function getExperiment(experimentId) {
//   return axios.get(`${API_URL}/experiments/${experimentId}/`);
// }

export function getDevice() {
  return "1199802";
}

export default {
  login(role, userData) {
    if (role === "student") {
      for (let i in students) {
        let user = students[i];
        if (user.username === userData.username) {
          if (
            user.password === userData.password &&
            user.teacher === userData.teacher
          ) {
            return user;
          }
        }
      }
      throw ErrorMessages.incorrectCredentials;
    }

    if (role === "teacher") {
      for (let i in teachers) {
        let user = teachers[i];
        if (user.id === userData.username) {
          if (user.password === userData.password) {
            return user;
          } else {
            throw ErrorMessages.incorrectCredentials;
          }
        }
      }
      throw ErrorMessages.incorrectCredentials;
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
  generateId: function() {
    let str = Math.floor(Math.random() * 100000000 + 9999999).toString();
    return parseInt(str.substring(0, 8));
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
  getDataArrays(type) {
    let data = SampleClimateData.data;
    let temp = { units: null, name: type, data: [] };
    for (let i in data) {
      let record = data[i];
      if (record.attribute === type) {
        temp.units = record.units;
        break;
      }
    }
    for (let i in data) {
      let record = data[i];
      if (record.attribute === type) {
        temp.data.push({ x: record.ts, y: record.value });
      }
    }
    return temp;
  },
  pullCSV(start, end){
    alert("https://fop1.urbanspacefarms.com:5000/api/get_data_json/" + store.state.currentExperiment.device + "/" + start + "/" +end);
  },

  /// FUNCTIONS FOR CLASSES

  getClasses: function() {
    return classes;
  },
  getClass: function(classId) {
    return classes.find(c => c.id === classId);
  },
  addClass: function() {
    classes.push({
      name: "Class".concat(" ", (classes.length + 1).toString()),
      id: this.generateId(),
      students: []
    });
  },
  deleteClass: function(classId) {
    let index = classes
      .map(function(e) {
        return e.id;
      })
      .indexOf(classId);
    classes.splice(index, 1);
  },
  updateClass: function(classId, val) {
    let index = classes
      .map(function(e) {
        return e.id;
      })
      .indexOf(classId);
    classes[index].name = val;
  },
  removeStudentFromClass(classId, studentId){
    let index = classes
      .map(function(e) {
        return e.id;
      })
      .indexOf(classId);
    let studentIndex = classes[index].students.indexOf(studentId);
    classes[index].students.splice(studentIndex, 1);
  },

  /// FUNCTIONS FOR STUDENTS

  getStudents: function(classId = null) {
    if (classId === null) {
      return students;
    } else {
      let currentClass = classes.find(c => c.id === classId);
      let studentIds = currentClass.students;
      let classStudents = [];
      studentIds.forEach(function(id) {
        classStudents.push(students.find(s => s.id === id));
      });
      return classStudents;
    }
  },
  getStudentCheckboxes: function(experimentId=null) {
    let newList = [];
    let modifiedStudent = {};
    let currentScope;
    if(experimentId !== null) {
      let exp = experiments.find(c => c.id === experimentId);
      currentScope = students.filter(element => exp.students.includes(element.id));
    }
    else{
      currentScope = students;
    }

    for (let i in currentScope) {
      let student = students[i];
      modifiedStudent = {
        text: student.username + ", " + student.fname + " " + student.lname,
        value: student.id
      };
      newList.push(modifiedStudent);
    }
    return newList;
  },
  getStudent: function(studentId) {
    let student = students.find(c => c.id === studentId);
    if (!student) {
      alert("This account does not exist");
    } else {
      return student;
    }
  },
  createStudent: function(student) {
    for (let index in students) {
      if (students[index].username === student.username) {
        throw "That username already exists";
      }
    }
    if (student.username) studentIdCounter += 1;
    student.id = studentIdCounter;
    students.push(student);
    return student;
  },
  addStudent: function(studentId, classId) {
    let currentClass = classes.find(c => c.id === classId);
    currentClass.students.push(studentId);
  },
  updateStudent: function(studentId, values) {
    for (let index in students) {
      if (students[index].username === values.username && students[index].id !== studentId) {
        throw "That username already exists";
      }
    }

    let index = students
      .map(function(e) {
        return e.id;
      })
      .indexOf(studentId);

    let student = students[index];
    student.fname = values.fname;
    student.lname = values.lname;
    student.username = values.username;
    student.password = values.password;
  },

  deleteStudent: function(studentId) {
    //Delete student from student list
    let index = students
      .map(function(e) {
        return e.id;
      })
      .indexOf(studentId);
    students.splice(index, 1);
    //Remove student from their classes
    for (let i in classes) {
      let c = classes[i];
      if (c.students.includes(studentId)) {
        c.students.splice(c.students.indexOf(studentId), 1);
      }
    }
  },
  getStudentDisplayName(studentId) {
    if (typeof studentId === "string") {
      return "teacher";
    }
    let student = this.getStudent(studentId);
    return student.username + ", " + student.fname + " " + student.lname;
  },

  /// FUNCTIONS FOR EXPERIMENTS

  getExperiments: function(role, userId) {
    let expList = [];
    if (role === "teacher") {
      for (let e in experiments) {
        let exp = experiments[e];
        if (exp.teacher === userId) {
          expList.push(exp);
        }
      }
    } else if (role === "student") {
      for (let e in experiments) {
        let exp = experiments[e];
        if (exp.students.includes(userId)) {
          expList.push(exp);
        }
      }
    }
    return expList;
  },
  getExperiment: function(id) {
    for (let e in experiments) {
      let exp = experiments[e];
      if (exp.id === id) {
        return exp;
      }
    }
    // let today = this.getToday(new Date());
    // return { title: "New Experiment", start_date: today };
    return null;
  },
  createExperiment: function(values, teacher) {
    let newExperiment = {};
    for (let v in values) {
      newExperiment[v] = values[v];
    }
    newExperiment.teacher = teacher;
    newExperiment.id = this.generateId();

    experiments.push(newExperiment);
    return newExperiment;
  },
  updateExperiment: function(id, values) {
    for (let e in experiments) {
      let exp = experiments[e];
      if (exp.id === id) {
        for (let k in values) {
          exp[k] = values[k];
        }
        break;
      }
    }
  },
  changeExperimentInvolvement: function(expId, studentId) {
    let index = experiments
      .map(function(e) {
        return e.id;
      })
      .indexOf(expId);

    let exp = experiments[index];
    if (exp.students.includes(studentId)) {
      exp.students.splice(exp.students.indexOf(studentId), 1);
    } else {
      exp.students.push(studentId);
    }
  },
  deleteExperiment: function(experimentId) {
    let index = experiments
      .map(function(e) {
        return e.id;
      })
      .indexOf(experimentId);
    experiments.splice(index, 1);
  },

  /// FUNCTIONS FOR ASSIGNMENTS

  getAssignments(role, userId) {
    let assignmentList = [];
    if (role === "teacher") {
      for (let a in assignments) {
        let assignment = assignments[a];
        if (assignment.teacher === userId) {
          assignmentList.push(assignment);
        }
      }
    } else if (role === "student") {
      for (let a in assignments) {
        let assignment = assignments[a];
        if (assignment.assignees.includes(userId)) {
          assignmentList.push(assignment);
        }
      }
    }
    return assignmentList;
  },
  createAssignment(values) {
    values.teacher = store.state.currentUser.id;
    values.id = this.generateId();
    assignments.push(values);
    for(let i in values.assignees) {
      this.addAssignmentResponse(values.id,values.assignees[i])
    }
  },
  updateAssignment(assignmentId, values) {
    for (let a in assignments) {
      let assignment = assignments[a];
      if (assignment.id === assignmentId) {
        assignment.title = values.title;
        assignment.description = values.description;
        assignment.due_date = values.due_date;
        assignment.assignees = values.assignees;

        let currentResponses = this.getTeacherAssignmentResponses(
          assignment.id
        );
        let assigneesList = assignment.assignees;
        for (let index in assigneesList) {
          if (!currentResponses.find(o => o.student === assigneesList[index])) {
            this.addAssignmentResponse(assignment.id, assigneesList[index]);
          }
        }
      }
    }
  },
  deleteAssignment(assignmentId){
    let index = assignments
      .map(function(e) {
        return e.id;
      })
      .indexOf(assignmentId);
    assignments.splice(index, 1);
  },
  addAssignmentResponse(assignmentId, studentId) {
    let newResponse = {
      assignment: assignmentId,
      student: studentId,
      response: null,
      submitted: "",
      comments: null
    };
    assignment_responses.push(newResponse);
  },
  getStudentAssignmentResponses(studentId) {
    let studentResponses = [];
    for (let i in assignment_responses) {
      if (assignment_responses[i].student === studentId) {
        studentResponses.push(assignment_responses[i]);
      }
    }
    return studentResponses;
  },
  getTeacherAssignmentResponses(assignmentId) {
    let studentResponses = [];
    for (let i in assignment_responses) {
      let thisAssignment = assignment_responses[i];
      if (thisAssignment.assignment === assignmentId) {
        studentResponses.push(thisAssignment);
      }
    }
    return studentResponses;
  },
  getStudentAssignmentResponse(assignmentId, studentId) {
    for (let i in assignment_responses) {
      let thisAssignment = assignment_responses[i];
      if (
        thisAssignment.student === studentId &&
        thisAssignment.assignment === assignmentId
      ) {
        return thisAssignment;
      }
    }
    return null;
  },
  updateStudentAssignmentResponse(assignmentId, studentId, values) {
    for (let i in assignment_responses) {
      let thisAssignment = assignment_responses[i];
      if (
        thisAssignment.student === studentId &&
        thisAssignment.assignment === assignmentId
      ) {
        thisAssignment.response = values.response;
        thisAssignment.submitted = values.submitted;
        break;
      }
    }
  },
  addCommentToAssignment(assignmentId, studentId, value){
      let response = this.getStudentAssignmentResponse(assignmentId, studentId);
      response.comments = value;
      return response;
  },

  /// FUNCTIONS FOR OBSERVATIONS

  getObservations() {
    let experiment = store.state.currentExperiment.id;
    let obsList = [];
    for (let i in observations) {
      let obs = observations[i];
      if (obs.experiment === experiment) {
        obsList.push(obs);
      }
    }
    return obsList;
  },
  getObservation(observationId) {
    let obsList = this.getObservations();
    let index = obsList
      .map(function(e) {
        return e.id;
      })
      .indexOf(observationId);
    return observations[index];
  },
  updateObservation(observationId, values) {
    let obs = this.getObservation(observationId);
    obs.title = values.title;
    obs.description = values.description;
    obs.collaborators = values.collaborators;
    obs.updated = values.updated;
    return obs;
  },
  createObservation(values) {
    let obs = {};
    obs.id = this.generateId();
    obs.experiment = store.state.currentExperiment.id;
    obs.title = values.title;
    obs.description = values.description;
    obs.type = values.type;
    obs.collaborators = values.collaborators;
    obs.updated = this.getToday(new Date());
    obs.responses = [];

    observations.unshift(obs);
    return obs;
  },
  deleteObservation(observationId) {
    let obsList = this.getObservations();
    let index = obsList
      .map(function(e) {
        return e.id;
      })
      .indexOf(observationId);
    observations.splice(index, 1);
  },
  addObservationResponse(observationId) {
    let obs = this.getObservation(observationId);
    obs.responses.push({
      response: null,
      submitted: null,
      student: null,
      editable: true,
      number: obs.responses.length + 1
    });
    return obs;
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
  deleteObservationResponse(observationId, responseNumber) {
    let obs = this.getObservation(observationId);
    let responseIndex = obs.responses
      .map(function(e) {
        return e.number;
      })
      .indexOf(responseNumber);
    obs.responses.splice(responseIndex, 1);

    obs.responses.map(item => {
      if (item.number > responseNumber) {
        item.number -= 1;
      }
    });

    return obs;
  },

  /// FUNCTIONS FOR DEVICES

  getDevices() {
    return devices.filter(element => element.teacher === store.state.currentTeacher);
  },
  getDevice(deviceId){
    let index = devices
      .map(function(e) {
        return e.fopd_id;
      })
      .indexOf(deviceId);
    return devices[index]
  },
  updateDeviceName(deviceId, newName) {
    let device = this.getDevice(deviceId)
    device.name = newName;
  },
  updateDeviceOwner(deviceId, teacherId) {
    let device = this.getDevice(deviceId)
    device.name = teacherId;
  },

  getClimate() {
    return SampleClimate.climate_file.phases;
  },
  verifyDevice(deviceId) {
    for (let d in devices) {
      let device = devices[d]
      if (device.fopd_id === deviceId && device.teacher !== "") {
        return false;
      }
    }
    return true;
  },
  registerDevice(values, teacher) {
      devices.push({
        name: values.name,
        fopd_id: values.fopd_id,
        teacher: teacher
      });
  },

  /// FUNCTIONS FOR TEACHERS

  getTeacherInfo() {
    let index = teachers
      .map(function(e) {
        return e.id;
      })
      .indexOf(store.state.currentTeacher);
    return teachers[index];
  },
  updateTeacherName(values) {
    let teacher = this.getTeacherInfo();
    teacher.fname = values.fname;
    teachers.lname = values.lname;
  },
  changeTeacherPassword(oldPass, newPass) {
    let teacher = this.getTeacherInfo();
    if (teacher.password !== oldPass) {
      throw "Password incorrect";
    } else {
      teacher.password = newPass;
      store.state.currentUser = {
        fname: teacher.fname,
        lname: teacher.lname,
        id: teacher.id
      };
    }
  },
  registerTeacher(values) {
    let deviceId = values.fopd_id
    if (this.verifyDevice(deviceId)) {
      let newTeacher = {
        fname: values.fname,
        lname: values.lname,
        password: values.password,
        id: this.generateUsername()
      };
      teachers.push(newTeacher);
      this.registerDevice({ fopd_id: deviceId, name: deviceId }, newTeacher.id)
      return newTeacher.id
    } else {
      throw "invalid device ID";
    }
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
