import axios from "axios";
import ErrorMessages from "../constants/ErrorMessages.ts";
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
    title: "Example",
    description: "This is a sample experiment",
    plant: "basil",
    start_date: "2020-03-15",
    teacher: "a",
    students: [1, 4],
    id: 38782347
  },
  {
    title: "Another",
    description: "Another example experiment",
    plant: "tomato",
    start_date: "2020-03-18",
    teacher: "a",
    students: [1, 2, 3],
    id: 16847325
  }
];

let teachers = [{ fname: "Mr", lname: "Teacher", password: "a", id: "a" }];

let studentIdCounter = students.length;

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
    if (role == "student") {
      for (let i in students) {
        let user = students[i];
        if (user.username == userData.username) {
          if (
            user.password == userData.password &&
            user.teacher == userData.teacher
          ) {
            return user;
          }
        }
      }
      throw ErrorMessages.incorrectCredentials;
    }

    if (role == "teacher") {
      for (let i in teachers) {
        let user = teachers[i];
        if (user.id == userData.username) {
          if (user.password == userData.password) {
            return user;
          } else {
            throw ErrorMessages.incorrectCredentials;
          }
        }
      }
      throw ErrorMessages.incorrectCredentials;
    }
  },
  getToday: function() {
    let today = new Date();
    let dd = String(today.getDate()).padStart(2, "0");
    let mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
    let yyyy = today.getFullYear();
    today = yyyy + "-" + mm + "-" + dd;
    return today;
  },
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
  generateId: function() {
    let str = Math.floor(Math.random() * 100000000 + 9999999).toString();
    return parseInt(str.substring(0, 8));
  },
  getStudents: function(classId = null) {
    if (classId == null) {
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
  getStudentCheckboxes: function(scopeId = null) {
    if (scopeId != null) {
      let newList = [];
      let modifiedStudent = {};
      // let currentScope
      // if(type == "experiment") {
      //   currentScope = experiments.find(c => c.id === scopeId);
      // }
      // else {
      //   currentScope = classes.find(c => c.id === scopeId);
      // }
      for (let i in students) {
        let student = students[i];
        modifiedStudent = {
          text: student.username + ", " + student.fname + " " + student.lname,
          value: student.id
        };
        newList.push(modifiedStudent);
      }
      return newList;
    }
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
      if (students[index].username == student.username) {
        throw "That username already exists";
      }
    }
    alert("does not end btw");
    if (student.username) studentIdCounter += 1;
    student.id = studentIdCounter;
    students.push(student);
    // this.$store.state.studentList = this.getStudents()
    return student;
  },
  addStudent: function(studentId, classId) {
    let currentClass = classes.find(c => c.id === classId);
    currentClass.students.push(studentId);
  },
  updateStudent: function(studentId, values) {
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

    this.$store.state.studentList = this.getStudents();
  },

  getExperiments: function(role, id) {
    let expList = [];
    if (role == "teacher") {
      for (let e in experiments) {
        let exp = experiments[e];
        if (exp.teacher == id) {
          expList.push(exp);
        }
      }
    } else if (role == "student") {
      for (let e in experiments) {
        let exp = experiments[e];
        if (exp.students.includes(id)) {
          expList.push(exp);
        }
      }
    }
    return expList;
  },
  getExperiment: function(id) {
    for (let e in experiments) {
      let exp = experiments[e];
      if (exp.id == id) {
        return exp;
      }
    }
    let today = this.getToday();
    return { title: "New Experiment", start_date: today };
  },
  createExperiment: function(values, teacher) {
    let newExperiment = {};
    for (let v in values) {
      newExperiment[v] = values[v];
    }
    newExperiment.teacher = teacher;
    newExperiment.students = [];
    newExperiment.id = this.generateId();

    experiments.push(newExperiment);
    return newExperiment;
  },
  updateExperiment: function(id, values) {
    for (let e in experiments) {
      let exp = experiments[e];
      if (exp.id == id) {
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
