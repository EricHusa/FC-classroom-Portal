<template>
  <div class="center">
    <button><router-link to="/home">Home</router-link></button>
    <br />
    <b-row>
      <b-col cols="6" md="4"
        ><b-button class="m-1" variant="success" @click="addClass">Create a new class</b-button>
        <br />
        <b-list-group v-for="item in classes" :key="item.name">
          <b-list-group-item button @click="setClass(item.id)" :active="item.id==currClass">{{
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
      currClass: this.$store.state.activeClass
    };
  },
  methods: {
      config: function () {
        this.$router.push({name:"start_crop"})
      },
    addClass() {
       api.addClass()
       this.classes = api.getClasses()
    },
    setClass(id) {
        this.students = api.getStudents(id)
        this.$store.state.activeClass = id
        this.currClass = id
    }
  },
  mounted() {
    this.classes = api.getClasses()
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
