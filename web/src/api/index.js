import axios from "axios";
// import ErrorMessages from "../constants/ErrorMessages.ts";
import store from "../store/index";
import SampleClimate from "../constants/SampleClimate.ts";
import SampleClimateData from "../constants/SampleClimateData.ts";
// const API_URL = process.env.API_URL;
const API_URL = "http://127.0.0.1:5000/api";

//Local storage for speed
let students = [];
let classes = [];
let experiments = [];
let assignments = [];
let assignment_responses = {};
let observations = [];
let devices = [];

//sample database data
// let students = [
//   {
//     fname: "Jon",
//     lname: "Joe",
//     username: "JJ09",
//     password: "Peaches",
//     id: 1,
//     teacher: "a"
//   },
//   {
//     fname: "Will",
//     lname: "Billy",
//     username: "WB02",
//     password: "Cake",
//     id: 2,
//     teacher: "a"
//   },
//   {
//     fname: "Drew",
//     lname: "Blue",
//     username: "DB12",
//     password: "Orange",
//     id: 3,
//     teacher: "a"
//   },
//   {
//     fname: "Bob",
//     lname: "Cob",
//     username: "b",
//     password: "c",
//     id: 4,
//     teacher: "a"
//   }
// ];

// let experiments = [
//   {
//     title: "Example Experiment",
//     description: "This is a sample experiment",
//     plant: "basil",
//     start_date: "2020-03-15",
//     teacher: "a",
//     students: [1, 4],
//     id: 38782347,
//     device: "8a0118e3-a6bf-4ace-85c4-a7c824da3f0c"
//   },
//   {
//     title: "Another",
//     description: "Another example experiment",
//     plant: "tomato",
//     start_date: "2020-03-18",
//     teacher: "a",
//     students: [1, 2, 3],
//     id: 16847325,
//     device: "8a0118e3-a6bf-4ace-85c4-a7c824da3f0c"
//   }
// ];

// let assignments = [
//   {
//     id: 35688201,
//     teacher: "a",
//     experiment: 38782347,
//     title: "Predict How Many Days",
//     description: "Predict how many days it takes the plant to grow 1 inch",
//     type: "number",
//     due_date: "2020-05-05",
//     assignees: [2, 4]
//   },
//   {
//     id: 25674621,
//     teacher: "a",
//     experiment: 38782347,
//     title: "Give yourself a team role",
//     description: "Tell me what your role on the team is",
//     type: "text",
//     due_date: "2020-05-04",
//     assignees: [1, 2, 3, 4]
//   }
// ];

// let assignment_responses = [
//   {
//     assignment: 25674621,
//     student: 1,
//     response: "I want team Leader",
//     submitted: "2020-05-03",
//     comments: "Congratulations, you will be the team's Leader"
//   },
//   {
//     assignment: 25674621,
//     student: 2,
//     response: "Gardener",
//     submitted: "2020-05-03",
//     comments: "Congratulations, you will be the team's Gardener"
//   },
//   {
//     assignment: 25674621,
//     student: 3,
//     response: "Can I be the Record Keeper",
//     submitted: "2020-05-04",
//     comments: "Congratulations, you will be the team's Record Keeper"
//   },
//   {
//     assignment: 25674621,
//     student: 4,
//     response: "I want to be the team Researcher",
//     submitted: "2020-05-04",
//     comments: "Congratulations, you will be the team's Researcher"
//   },
//   {
//     assignment: 35688201,
//     student: 2,
//     response: null,
//     submitted: "",
//     comments: null
//   },
//   {
//     assignment: 35688201,
//     student: 4,
//     response: null,
//     submitted: "",
//     comments: null
//   }
// ];

// let observations = [
//   {
//     id: 12835739,
//     title: "Height Measurement",
//     description:
//       "Take your ruler and measure the height of the plant in centimeters",
//     experiment: 38782347,
//     type: "number",
//     units: "centimeters",
//     updated: "2020-05-01",
//     collaborators: [1, 2, 4],
//     responses: [
//       {
//         number: 1,
//         response: "3",
//         submitted: "2020-05-02",
//         student: 4,
//         editable: true
//       },
//       {
//         number: 2,
//         response: "3.1",
//         submitted: "2020-05-03",
//         student: 1,
//         editable: true
//       }
//     ]
//   }
// ];

// let teachers = [{ fname: "Mr", lname: "Teacher", password: "a", id: "a" }];
//
// let studentIdCounter = students.length;

// let devices = [
//   {
//     name: "SLUdev1",
//     fopd_id: "8a0118e3-a6bf-4ace-85c4-a7c824da3f0c",
//     teacher: "a"
//   }
// ];

// let classes = [
//   {
//     name: "Class 1",
//     id: 23213931,
//     students: [1, 2]
//   },
//   {
//     name: "Class 2",
//     id: 63526050,
//     students: [3, 4]
//   }
// ];

export function authenticate(userData) {
  return axios.post(`${API_URL}/login/`, userData);
}

export function register(userData) {
  return axios.post(`${API_URL}/register/`, userData);
}

// export function getDevice() {
//   return "1199802";
// }

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
    .catch(function(error) {
        throw (error);
    });
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



      // let r = axios.get(`${API_URL}/teacher/${userData.id}`);
      // axios.get(`${API_URL}/teacher/${userData.id}`)
      // .then(function (response) {
      //   if(response.data.status==="fail"){
      //     throw(response.data.message);
      //   }
      //   else{
      //     return(response.data);
      //   }
      // })
      // .catch(function (error) {
      //   throw(error);
      // });

      // for (let i in teachers) {
      //   let user = teachers[i];
      //   if (user.id === userData.username) {
      //     if (user.password === userData.password) {
      //       return user;
      //     } else {
      //       throw ErrorMessages.incorrectCredentials;
      //     }
      //   }
      // }
      // throw ErrorMessages.incorrectCredentials;
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

    // let index = classes
    //   .map(function(e) {
    //     return e.id;
    //   })
    //   .indexOf(classId);
    // classes.splice(index, 1);
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

    // let index = classes
    //   .map(function(e) {
    //     return e.id;
    //   })
    //   .indexOf(classId);
    // classes[index].name = val;
  },
  // async addStudent(studentUsername, course) {
  //   course.students.push(studentUsername);
  //   let c = await this.updateClass(course, course.name).then(function(response) {
  //       return response;
  //     });
  //
  //   // let currentClass = classes.find(c => c.id === classId);
  //   // currentClass.students.push(studentId);
  // },
  // removeStudentFromClass(classId, studentId){
  //   let index = classes
  //     .map(function(e) {
  //       return e.id;
  //     })
  //     .indexOf(classId);
  //   let studentIndex = classes[index].students.indexOf(studentId);
  //   classes[index].students.splice(studentIndex, 1);
  // },
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
      currentScope = students.filter(element => exp.students.includes(element.id));
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

    // for (let index in students) {
    //   if (students[index].username === student.username) {
    //     throw "That username already exists";
    //   }
    // }
    // if (student.username) studentIdCounter += 1;
    // student.id = studentIdCounter;
    // students.push(student);
    // return student;
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

    // for (let index in students) {
    //   if (students[index].username === values.username && students[index].id !== studentId) {
    //     throw "That username already exists";
    //   }
    // }
    //
    // let index = students
    //   .map(function(e) {
    //     return e.id;
    //   })
    //   .indexOf(studentId);
    //
    // let student = students[index];
    // student.fname = values.fname;
    // student.lname = values.lname;
    // student.username = values.username;
    // student.password = values.password;
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

    // //Delete student from student list
    // let index = students
    //   .map(function(e) {
    //     return e.id;
    //   })
    //   .indexOf(studentId);
    // students.splice(index, 1);
    // //Remove student from their classes
    // for (let i in classes) {
    //   let c = classes[i];
    //   if (c.students.includes(studentId)) {
    //     c.students.splice(c.students.indexOf(studentId), 1);
    //   }
    // }
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
    // let today = this.getToday(new Date());
    // return { title: "New Experiment", start_date: today };
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
    // let newExperiment = {};
    // for (let v in values) {
    //   newExperiment[v] = values[v];
    // }
    // newExperiment.teacher = teacher;
    // newExperiment.id = this.generateId();
    //
    // experiments.push(newExperiment);
    // return newExperiment;
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
  // changeExperimentInvolvement: function(expId, studentId) {
  //   let index = experiments
  //     .map(function(e) {
  //       return e.id;
  //     })
  //     .indexOf(expId);
  //
  //   let exp = experiments[index];
  //   if (exp.students.includes(studentId)) {
  //     exp.students.splice(exp.students.indexOf(studentId), 1);
  //   } else {
  //     exp.students.push(studentId);
  //   }
  // },
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
                assignments = response.data.assignments;
                return response.data.assignments;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },
  getAssignments() {
    return assignments;
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
  createAssignment(values) {
    return Promise.resolve(axios.post(`${API_URL}/assignment/teacher/${store.state.currentTeacher}`, values)
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

    // assignments.push(values);
    // for(let i in values.assignees) {
    //   this.addAssignmentResponse(values.id,values.assignees[i])
    // }
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

    // for (let a in assignments) {
    //   let assignment = assignments[a];
    //   if (assignment.id === assignmentId) {
    //     assignment.title = values.title;
    //     assignment.description = values.description;
    //     assignment.due_date = values.due_date;
    //     assignment.assignees = values.assignees;

        // let currentResponses = this.getTeacherAssignmentResponses(
        //   assignment.id
        // );
        // let assigneesList = assignment.assignees;
        // for (let index in assigneesList) {
        //   if (!currentResponses.find(o => o.student === assigneesList[index])) {
        //     this.addAssignmentResponse(assignment.id, assigneesList[index]);
        //   }
        // }
    //   }
    // }
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
    getAssignmentAssignees(){

    },
  // addAssignmentResponse(assignmentId, studentId) {
  //   let newResponse = {
  //     assignment: assignmentId,
  //     student: studentId,
  //     response: null,
  //     submitted: "",
  //     comments: null
  //   };
  //   assignment_responses.push(newResponse);
  // },
    getApiStudentAssignmentResponse(assignmentId,studentId){
      return Promise.resolve(axios.get(`${API_URL}/assignment/${assignmentId}/student/${studentId}`)
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
getStudentAssignmentResponses(){
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

    // let studentResponses = [];
    // for (let i in assignment_responses) {
    //   let thisAssignment = assignment_responses[i];
    //   if (thisAssignment.assignment === assignmentId) {
    //     studentResponses.push(thisAssignment);
    //   }
    // }
    // return studentResponses;
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
  addCommentToAssignment(assignmentId, responseId, value){
      return Promise.resolve(axios.put(`${API_URL}/assignment/${assignmentId}/response/${responseId}/student/${store.state.currentUser.id}`, {comments: value})
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
                assignments = response.data.assignments;
                return response.data.assignments;
            }
        }))
    .catch(function(error) {
        throw (error);
    });
  },

  getObservations(experiment) {
      if(experiment==null||experiment==undefined||experiment=={}) {
          return [];
      }
    let obsList = [];
    for (let i in observations) {
      let obs = observations[i];
      if (obs.experiment === experiment.id) {
        obsList.unshift(obs);
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
  getDevice(deviceId){
    let index = devices
      .map(function(e) {
        return e.fopd_id;
      })
      .indexOf(deviceId);
    return devices[index]
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
  // updateDeviceOwner(deviceId, teacherId) {
  //   let device = this.getDevice(deviceId)
  //   device.name = teacherId;
  // },
  //
  getClimate() {
    return SampleClimate.climate_file.phases;
  },
  verifyDevice(deviceId) {
    if (deviceId==="bad",deviceId===""||deviceId===null||deviceId===undefined) {
        return false;
    }
    return true;
  },
  registerDevice(values) {
      values.teacher_id = store.state.currentTeacher;
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

  // getTeacherInfo() {
  //   return Promise.resolve(axios.get(`${API_URL}/teacher/${store.state.currentTeacher}/`)
  //       .then(function(response) {
  //           if (response.data.status === "fail") {
  //               throw (response.data.message);
  //           } else {
  //               return response.data.teacher;
  //           }
  //       }))
  //   .catch(function(error) {
  //       throw (error);
  //   });
  // },
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
  // updateTeacherName(values) {
  //   let teacher = this.getTeacherInfo();
  //   teacher.fname = values.fname;
  //   teachers.lname = values.lname;
  // },
  // changeTeacherPassword(oldPass, newPass) {
  //   let teacher = this.getTeacherInfo();
  //   if (teacher.password !== oldPass) {
  //     throw "Password incorrect";
  //   } else {
  //     teacher.password = newPass;
  //     store.state.currentUser = {
  //       fname: teacher.fname,
  //       lname: teacher.lname,
  //       id: teacher.id
  //     };
  //   }
  // },
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

// export function getRepeatAssignments() {
//   return axios.get(`${API_URL}/repeatAssignments/`);
// }

export function newExperiment(exp, jwt) {
  return axios.post(`${API_URL}/experiments/`, exp, {
    headers: { Authorization: `Bearer: ${jwt}` }
  });
}
