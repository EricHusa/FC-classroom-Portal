<template>
  <div class="center">
    <button><router-link to="/home">Home</router-link></button>
    <br />
    <b-row>
      <b-col cols="6" md="4"
        >Classes
        <b-list-group v-for="item in classes" :key="item.name">
          <b-list-group-item button @click="sendMessage">{{item.name}}</b-list-group-item>
        </b-list-group>
        <br />
        <b-button variant="success">Create a new class</b-button>
      </b-col>

      <b-col cols="12" md="8"
        >Students
        <StudentList
          v-bind:students="students"
          v-bind:headers="headers"
          v-bind:device="device"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import StudentList from "../components/StudentList.vue";
// import api from "../api/index.js";
export default {
  name: "School",
  components: { StudentList },
  data() {
    return {
      students: [
        {
          fname: "Jono",
          lname: "Joe",
          username: "JJ09",
          password: "Peaches"
        },
        {
          fname: "Will",
          lname: "Billy",
          username: "WB02",
          password: "Cake"
        }
      ],
      headers: [
        { key: "fname", label: "First Name" },
        { key: "lname", label: "Last Name" },
        { key: "username", label: "Username" },
        { key: "password", label: "Password" },
        { key: "action", label: "Action" }
      ],
      device: this.$store.state.device,
      classes: [{}]
    };
  },
  methods: {
      sendMessage() {
          this.school = '7762326'
      }
  },
  mounted () {
  // api.getClasses()
  //       .then(response => {
  //         this.classes = response })
  //       .catch(() => {
  //         this.classes = [{}]})

  // api.getSchool()
  //       .then(response => {
  //         this.school = response })
  //       .catch(() => {
  //         this.school = "446521"})
  }
};
</script>

<style>
.center {
  margin: auto;
  width: 60%;
  padding: 10px;
}
</style>
