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
    <b-overlay :show="assignment.id===undefined" rounded="sm">
      <b-jumbotron
        ><h2>{{ assignment.title }}</h2>
        <code>{{assignment.type}}</code>
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
                  <b-form-textarea
                    id="student-assignment-response-input"
                    :type="assignment.type"
                    required
                    :disabled="unlocked != assignment.id"
                    :placeholder="response.response"
                    v-model="response.response"
                  ></b-form-textarea>
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
            </b-row><hr/>
            <b><u>Teacher's Comments:</u></b>
            <p>{{response.comments}}</p>
          </b-collapse>
        </b-container>


        <b-collapse :visible="role == 'teacher'">
          <b-container fluid>
            <b-form-group v-for="item in responseList" :key="item.key">
            <b-row class="my-1" >
              <b-col sm="3">
                <label :for="`response-${item.student.id}`"
                  ><b>{{ item.student.username }}</b
                  >:</label
                >
              </b-col>
              <b-col sm="8">
                <b-form-group
                  :label-for="`response-${item.student.id}`"
                  :description="`Submission: ${item.submitted == 'None' ? 'None' : new Date((item.submitted.split(' ')[0]).replace(/-/g, '/')).toDateString()}`">
                <b-form-textarea
                  :id="`response-${item.student.id}`"
                  :value="item.response"
                  disabled
                ></b-form-textarea></b-form-group>
              </b-col>
              <b-col sm="1"><b-button @click="selectResponse(item)">+</b-button></b-col>
            </b-row>
              <b-collapse :visible="commentingOn!==null && commentingOn===item.id" class="mt-2">
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
            <b-button variant="danger" @click="deleteAssignment" :hidden="assignment.id===undefined" style="float:left;">Delete assignment</b-button>
          </b-container>
        </b-collapse>
      </b-jumbotron>
      <template v-slot:overlay>
        <div class="text-center">
          <b-icon icon="x-circle-fill" font-scale="3"></b-icon>
          <p id="cancel-label">Please select or create an assignment.</p>
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
    async responseSubmitted(evt) {
      evt.preventDefault();
      if(this.assignment.type ==="number"){
        if(!/^\d+(\.\d+)?$/.test(this.response.response)){
          alert("You may only enter numbers for this response (such as 1.5), please try again");
          return;
        }
      }
      this.form.response = this.response.response;
      this.form.submitted = api.getToday(new Date());
      this.response = await api.updateStudentAssignmentResponse(
        this.assignment.id,
        this.response.id,
        this.form
      ).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      this.showSuccess = 3;
      this.alertMessage = "Assignment submitted!"
      this.unlocked = null;
      this.$emit("studentSubmission");
    },
    selectResponse(res){
      this.teacherComment = res.comments;
      this.commentingOn = res.id;
    },
    async addComment(res){
      this.commentingOn = await api.addCommentToAssignment(res.assignment.id, res.id, this.teacherComment).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      this.showSuccess = 3;
      this.alertMessage = "Comment updated";
      this.commentingOn = null;
      this.$emit("updateResponseList", this.assignment);
    },
    async deleteAssignment(){
      await api.deleteAssignment(this.assignment.id).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      this.deleted=true;
      this.$emit("assignmentDeleted")
    },
    resetAlert() {
      this.showSuccess = 0;
    },
    unlockAnswer(assignmentId) {
      this.unlocked = assignmentId;
    },
  }
};
</script>

<style scoped></style>
