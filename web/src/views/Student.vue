<template>
  <b-container fluid>
    <NavBar />
    <b-alert :show="updateAlert" dismissible fade variant="success">
      Student account updated
    </b-alert>
    <b-alert :show="deleteAlert" dismissible fade variant="success">
      Student account deleted
    </b-alert>
    <br />
    <b-row
      ><b-button variant="secondary" to="/school" style="margin-left: 2rem;"
        >Back</b-button
      ></b-row
    >
    <b-row class="my-1" v-for="item in headers" :key="item">
      <b-col sm="3">
        <label :for="`form-${item.label}`">{{ item.label }}:</label>
      </b-col>
      <b-col sm="9">
        <b-form-input
          :id="`form-${item.label}`"
          :placeholder="student[item.key]"
          v-model="form[item.key]"
        ></b-form-input>
      </b-col>
    </b-row>
    <b-row>
      <b-col sm="3"></b-col>
      <b-col sm="9">
        <b-button
          style="float: left;"
          type="submit"
          @click="updateStudent()"
          variant="success"
          >Update information</b-button
        >
        <b-button
          style="float: right;"
          variant="danger"
          @click="deleteStudent()"
          >Delete student</b-button
        >
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import api from "../api/index.js";
import NavBar from "../components/NavBar";
export default {
  components: { NavBar },
  data() {
    return {
      student: {},
      updateAlert: 0,
      deleteAlert: 0,
      form: {
        fname: null,
        lname: null,
        username: "",
        password: ""
      },
      headers: [
        { key: "fname", label: "First Name", sortable: true },
        { key: "lname", label: "Last Name", sortable: true },
        { key: "username", label: "Username", sortable: true },
        { key: "password", label: "Password" }
      ]
    };
  },
  methods: {
    async updateStudent() {
      try {
        this.student = await api.updateStudent(this.student.id, this.form).then(function (response) {
          return response;
        });
        await api.setLocalStudents().then(function (response) {
          return response;
        });
      }
      catch(e){
        alert(e);
        return
      }
      this.updateAlert = 3;
    },
    async deleteStudent() {
      try{
      if (confirm("Are you sure you want to delete this student account?")) {
        await api.deleteStudent(this.student.id).then(function (response) {
          return response;
        });
        await api.setLocalStudents().then(function (response) {
          return response;
        });
        }
      catch(e){
        alert(e);
        return
      }
        // this.deleteAlert = 3
        this.$router.push("/school");
      }
    }
  },
  beforeMount: function() {
    this.studentId = parseInt(this.$route.params.id);
  },
  mounted() {
    this.student = api.getStudent(this.studentId);
    this.form.fname = this.student.fname;
    this.form.lname = this.student.lname;
    this.form.username = this.student.username;
    this.form.password = this.student.password;
  }
};
</script>
