<template>
  <div>
    <b-overlay :show="deleted" rounded="sm">
      <b-jumbotron
        ><h2>{{ assignment.title }}</h2>
        <hr />
        <b-container fluid>
          <br />
          <p>{{assignment.description}}</p>
          <b-collapse :visible="response && response.length ">
          <b-row>
            <b-col sm="3">
              <label for="student-assignment-response-input"
                ><code>response</code
                >:</label
              >
            </b-col>
            <b-col sm="9">
              <b-form-input
                id="student-assignment-response-input"
                :type="assignment.type"
                :value="response.response"
                :placeholder="response.response"
                v-model="this.form.response"
              ></b-form-input>
            </b-col>
            <b-button @click="responseSubmitted" variant="success">Submit</b-button>
          </b-row>
            </b-collapse>
        </b-container>


        <b-collapse :visible="responseList.length">
          <b-container fluid>
            <b-row class="my-1" v-for="item in responseList" :key="item.key">
            <b-col sm="3">
              <label :for="`type-${item.assignment}`"
                ><code>{{ getStudentName(item.student) }}</code
                >:</label
              >
            </b-col>
            <b-col sm="9">
              <b-form-input
                :id="`type-${item.assignment}`"
                :value="item.response"
                disabled
              ></b-form-input>
            </b-col>
          </b-row>
          </b-container>
        </b-collapse>
      </b-jumbotron>
      <template v-slot:overlay>
        <div class="text-center">
          <b-icon icon="x-circle-fill" font-scale="3"></b-icon>
          <p id="cancel-label">Please select or create another assignment.</p>
        </div>
      </template>
    </b-overlay>
  </div>
</template>

<script>
import api from "../api/index.js";
export default {
  name: "AssignmentViewer",
  props: {
    assignment: Object,
    response: Object,
    responseList: Array,
  },
  data() {
    return {
      form: {
        response: null,
        submitted: null
      },
      deleted: false,
      students: []
    };
  },
  beforeMount() {
    this.students = api.getStudents()
  },
  methods: {
    responseSubmitted(){
      api.updateStudentAssignmentResponses(this.assignment.id, this.$store.currentUser.id, this.form)
    },
    getStudentName(studentId){
      if(studentId != null) {
        let student = api.getStudent(studentId)
        return student.username + ", " + student.fname + " " + student.lname
      }
      else{
        return ""
      }
    }
  }
};
</script>

<style scoped></style>
