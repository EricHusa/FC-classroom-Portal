<template>
  <div>
    <NavBar /><br>
    <b-row>
      <b-col sm="4"></b-col>
      <b-col sm="4">
    <b-card header-html="<h3><b>Login</b></h3>" no-body>
      <b-alert :show="errorAlert" dismissible fade variant="danger">
      {{this.errorMsg}}
    </b-alert>

        <b-tabs card justified>
          <b-tab title="Student">
            <b-row class="my-1" v-for="item in options" :key="item">
              <label :for="`student-login-form-${item.key}`" class="login-label">{{ item.label }}:</label>
                <b-form-input
                  :id="`student-login-form-${item.key}`"
                  v-model="forms.student[item.key]"
                  class="login-input"
                ></b-form-input>
            </b-row>
            <b-button variant="success" @click="login('student')">Login</b-button>
          </b-tab>

          <b-tab title="Teacher">
            <b-row class="my-1" v-for="item in options.slice(1)" :key="item">
              <label :for="`teacher-login-form-${item.key}`">{{ item.label }}:</label>
                <b-form-input
                  :id="`teacher-login-form-${item.key}`"
                  v-model="forms.teacher[item.key]"
                ></b-form-input>
            </b-row>
            <b-button variant="success" @click="login('teacher')">Login</b-button>
            <b-button variant="info" @click="register()">Register</b-button>
          </b-tab>
        </b-tabs>

    </b-card>
        </b-col>
      <b-col sm="4"></b-col>
      </b-row>
  </div>
</template>

<script>
import { EventBus } from "../utils";
import NavBar from "./NavBar";
import api from "../api/index.js";
export default {
  components: { NavBar },
  data() {
    return {
      email: "",
      password: "",
      errorMsg: "",
      forms: {
        student: {teacher: "", username: "", password: ""},
        teacher: {username: "", password: ""}
        },
      options: [{key: "teacher", label: "Teacher"}, {key: "username", label: "Username"},{key: "password", label: "Password"}],
      errorAlert: 0
    };
  },
  methods: {
    authenticate() {
      // this.$store.dispatch('login', { email: this.email, password: this.password })
      //   .then(() => this.$router.push('/'))
      this.$store
        .dispatch("device", "student")
        .then(() => this.$router.push("/"));
      this.$store.dispatch("dev", "student").then(() => this.$router.push("/"));

    },
    register() {
      alert(this.$route.query.teacher)
      //this.$store.dispatch("dev", "teacher").then(() => this.$router.push("/"));
      //    this.$store.dispatch('register', { email: this.email, password: this.password })
      //      .then(() => this.$router.push('/')).catch(e => {
      // alert(e);
    },
    login(role){
        try{
          this.$store.state.currentUser = api.login(role, this.forms[role])
        }catch(error){
          this.errorMsg = error;
          this.errorAlert = 5;
          return
        }
          this.$store.state.role = role
          this.$router.push("/")
    }

  },
  beforeMount() {
    this.forms.student.teacher = this.$route.query.teacher
    this.$store.state.role = "guest"
  },
  mounted() {
    this.$store.dispatch("device");
    this.$store.dispatch("dev", "guest");
    EventBus.$on("failedRegistering", msg => {
      this.errorMsg = msg;
    });
    EventBus.$on("failedAuthentication", msg => {
      this.errorMsg = msg;
    });
  },
  beforeDestroy() {
    EventBus.$off("failedRegistering");
    EventBus.$off("failedAuthentication");
  }
};
</script>

<style lang="scss">
.login-label{
  text-decoration: underline;
}

.login-input{
  margin-bottom:1rem;
}

.error-msg {
  color: red;
  font-weight: bold;
}
</style>
