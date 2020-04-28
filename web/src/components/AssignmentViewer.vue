<template>
  <div>
    <b-alert
      :show="showSuccess"
      dismissible
      fade
      variant="success"
      @dismissed="resetAlert"
    >
      {{alertMessage}}
    </b-alert>
    <b-overlay :show="deleted" rounded="sm">
      <b-jumbotron
        ><h2>{{ assignment.title }}</h2>
        <hr />
        <b-container fluid>
          <br />
          <p>{{ assignment.description }}</p>
          <b-collapse
            :visible="role == 'student' && Object.keys(assignment).length !== 0"
          >
            <b-row>
              <b-col sm="3">
                <label for="student-assignment-response-input"
                  ><b>response</b>:</label
                >
              </b-col>
              <b-col sm="9">
                <b-form @submit="responseSubmitted">
                  <b-form-input
                    id="student-assignment-response-input"
                    :type="assignment.type"
                    required
                    :disabled="unlocked != assignment.id"
                    :placeholder="response.response"
                    v-model="response.response"
                  ></b-form-input>
                  <b-button
                    type="submit"
                    variant="success"
                    style="margin: 1rem;"
                    >Submit</b-button
                  >
                  <b-button
                    @click="unlockAnswer(assignment.id)"
                    variant="danger"
                    style="margin: 1rem;"
                    >Change Answer</b-button
                  >
                </b-form>
              </b-col>
            </b-row>
          </b-collapse>
        </b-container>

        <b-collapse :visible="role == 'teacher'">
          <b-container fluid>
            <b-form-group v-for="item in responseList" :key="item.key">
            <b-row class="my-1" >
              <b-col sm="3">
                <label :for="`response-${item.student}`"
                  ><b>{{ getStudentName(item.student) }}</b
                  >:</label
                >
              </b-col>
              <b-col sm="8">
                <b-form-input
                  :id="`response-${item.student}`"
                  :value="item.response"
                  disabled
                ></b-form-input>
              </b-col>
              <b-col sm="1"><b-button @click="selectResponse(item)">+</b-button></b-col>
            </b-row>
              <b-collapse :visible="commentingOn!==null && commentingOn.student===item.student" class="mt-2">
            <b-row class="my-1">
              <b-col sm="3">
                <b-button variant="success" @click="addComment(item)">Set Comment</b-button>
              </b-col>
                <b-col sm="8">
                <b-input v-model="teacherComment"></b-input>
              </b-col>
            </b-row>
                </b-collapse>
              </b-form-group>
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
    responseList: Array
  },
  data() {
    return {
      form: {
        response: "",
        submitted: null
      },
      deleted: false,
      students: [],
      role: null,
      unlocked: null,
      teacherComment: null,
      commentingOn: null,
      showSuccess: 0,
      alertMessage: ""
    };
  },
  beforeMount() {
    this.students = api.getStudents();
    this.role = this.$store.state.role;
  },
  methods: {
    responseSubmitted(evt) {
      evt.preventDefault();
      this.form.response = this.response.response;
      this.form.submitted = api.getToday(new Date());
      api.updateStudentAssignmentResponse(
        this.assignment.id,
        this.$store.state.currentUser.id,
        this.form
      );
      this.showSuccess = 3;
      this.alertMessage = "Assignment submitted!"
      this.unlocked = null;
    },
    selectResponse(res){
      this.teacherComment = res.comments;
      this.commentingOn = (this.responseList.filter(response => response.student === res.student))[0];
    },
    addComment(res){
      this.commentingOn = api.addCommentToAssignment(res.assignment, res.student, this.teacherComment);
      this.showSuccess = 3;
      this.alertMessage = "Comment updated";
      this.commentingOn = null;
    },
    resetAlert() {
      this.showSuccess = 0;
    },
    unlockAnswer(assignmentId) {
      this.unlocked = assignmentId;
    },
    getStudentName(studentId) {
      if (studentId != null) {
        let student = api.getStudent(studentId);
        return student.username + ", " + student.fname + " " + student.lname;
      } else {
        return "";
      }
    }
  }
};
</script>

<style scoped></style>
