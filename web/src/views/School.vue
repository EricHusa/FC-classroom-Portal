<template>
  <div class="center">
    <button><router-link to="/home">Home</router-link></button>
    <br />
    <b-row>
      <b-col cols="6" md="4"
        ><b-button class="m-1" variant="success" @click="addClass">Create a new class</b-button>
        <br />
        <b-list-group v-for="item in classes" :key="item.name">
          <b-list-group-item button @click="setClass(item.id)">{{
            item.name
          }}</b-list-group-item>
        </b-list-group>
        <br />
        Your class list
      </b-col>

      <b-col cols="12" md="8"
        >
        <StudentList
          v-bind:students="students"
          v-bind:headers="headers"
          v-bind:device="device"
          v-bind:currClass="currClass"
        />
      </b-col>
    </b-row>
  </div>
</template>

<script>
import StudentList from "../components/StudentList.vue";
// import getDevice from "../api";
import api from "../api/index.js";
export default {
  name: "School",
  components: { StudentList },
  data() {
    return {
      students: api.getStudents(this.$store.state.activeClass),
      headers: [
        { key: "fname", label: "First Name" },
        { key: "lname", label: "Last Name" },
        { key: "username", label: "Username" },
        { key: "password", label: "Password" },
        { key: "action", label: "Action" }
      ],
      device: this.$store.state.device,
      classes: [{}],
      currClass: "Select a class"
    };
  },
  methods: {
      config: function () {
        this.$router.push({name:"start_crop"})
      },
    addClass() {
      this.classes.push({
        name: "New Class",
        id: api.generateId(),
        students: []
      })
    },
    setClass(id) {
        this.students = api.getStudents(id)
        // let i;
        // for (i in students) {
        //   this.students.push(api.getUser(students[i]));
        // }
        this.$store.state.activeClass = id
        this.currClass = "Class: ".concat(id)
    }
  },
  mounted() {
    this.classes = api.getClasses()
    // if (this.$store.state.currClass != null){
    //   this.currClass = this.$store.state.currClass
    //   this.students = this.$store.state.currClass
    // }

    // this.$store.dispatch('listClasses')
    // getClasses()
    //       .then(response => {
    //         this.classes = response })
    //       .catch(() => {
    //         this.classes = [{}]})
    // getDevice()
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
