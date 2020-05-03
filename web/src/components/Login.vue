<template>
  <div>
    <NavBar /><br />
    <b-row>
      <b-col sm="4"></b-col>
      <b-col sm="4">
        <b-card header-html="<h3><b>Login</b></h3>" no-body>
          <b-alert :show="errorAlert" dismissible fade variant="danger" @dismissed="resetAlert">
            {{ this.errorMsg }}
          </b-alert>

          <b-tabs card justified>
            <b-tab title="Student">
              <b-row class="my-1" v-for="item in options" :key="item.key">
                <label
                  :for="`student-login-form-${item.key}`"
                  class="login-label"
                  >{{ item.label }}:</label
                >
                <b-form-input
                  :id="`student-login-form-${item.key}`"
                  v-model="forms.student[item.key]"
                  required
                  class="login-input"
                ></b-form-input>
              </b-row>
              <b-button variant="success" @click="login('student')"
                >Login</b-button
              >
            </b-tab>

            <b-tab title="Teacher">
              <b-row
                class="my-1"
                v-for="item in options"
                :key="item.key"
              >
                <label :for="`teacher-login-form-${item.key}`"
                  >{{ item.label }}:</label
                >
                <b-form-input
                  :id="`teacher-login-form-${item.key}`"
                  v-model="forms.teacher[item.key]"
                  required
                  class="login-input"
                ></b-form-input>
              </b-row>
              <b-button variant="success" @click="login('teacher')"
                >Login</b-button
              >
              <b-button variant="info" v-b-toggle.register-teacher>Register</b-button>
              <b-collapse id="register-teacher">
                <b-form @submit="register">
                <b-row v-for="item in registerOptions" :key="item.key">
                  <b-col sm="4">
                    <label>{{item.label}}: </label>
                  </b-col>
                  <b-col sm="8">
                    <b-input
                      v-model="forms.register[item.key]"
                      :type="item.type"
                      :required="item.required"
                      ></b-input><br/>
                  </b-col>
                </b-row>
                  <b-button variant="success" type="submit">Create Account</b-button>
                </b-form>
              </b-collapse>
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
import LoginOptions from "../constants/LoginOptions.ts";
export default {
  components: { NavBar },
  data() {
    return {
      email: "",
      password: "",
      errorMsg: "",
      forms: {
        student: { username: "", password: "" },
        teacher: { username: "", password: "" },
        register: {id: "", fname: "", lname: "", password: "", repeatPassword: ""}
      },
      options: LoginOptions.login,
      registerOptions: LoginOptions.register,
      errorAlert: 0
    };
  },
  methods: {
    // authenticate() {
    //   // this.$store.dispatch('login', { email: this.email, password: this.password })
    //   //   .then(() => this.$router.push('/'))
    //   this.$store
    //     .dispatch("device", "student")
    //     .then(() => this.$router.push("/"));
    //   this.$store.dispatch("dev", "student").then(() => this.$router.push("/"));
    // },
    getUsername(){

    },
    async register(evt) {
      // alert(this.$route.query.teacher);
      //this.$store.dispatch("dev", "teacher").then(() => this.$router.push("/"));
      //    this.$store.dispatch('register', { email: this.email, password: this.password })
      //      .then(() => this.$router.push('/')).catch(e => {
      // alert(e);
      evt.preventDefault();
      let teacher;
      try {
        this.checkNewPassword();
        teacher = await api.registerTeacher(this.forms.register).then(function (response) {
          return response;
        })
      }
      catch (error) {
        this.errorMsg = error;
        this.errorAlert = 5;
        return;
      }
        await api.registerDevice({ id: this.forms.register.id, name: this.forms.register.id, teacher_id: teacher.id}).catch(function (error) {
        alert(error);
        return;
      });
        this.forms.teacher.username = teacher.username;
        this.forms.teacher.password = this.forms.register.password;
        alert("Your username is " + teacher.username + ". Please write it down now and then log in")
    },
    async login(role) {
      try {
        let user = await api.login(role, this.forms[role]).then(function(response) {
        return response;
      });
        this.$store.state.currentUser = user;
        if(role==="teacher"){
          this.$store.state.currentTeacher = user.id;
      }
        // else{
        //   this.$store.state.currentTeacher = user.teacher.id;
        // }
        this.$store.state.role = role;
        this.$router.push("/");
      } catch (error) {
        this.errorMsg = error;
        this.errorAlert = 5;
        return;
      }
    },
    checkNewPassword(){
      if(this.forms.register.password !== this.forms.register.repeatPassword){
        throw "Passwords must match"
      }
    },
    resetAlert(){
      this.errorAlert = 0;
    }
  },
  beforeMount() {
    this.forms.student.teacher = this.$route.query.teacher;
    this.$store.state.role = "guest";
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
#teacher-login-form-password {
  type: "password";
}

.login-label {
  text-decoration: underline;
}

.login-input {
  margin-bottom: 1rem;
}

.btn {
  margin-right: 0.25rem;
  margin-left: 0.25rem;
}

.error-msg {
  color: red;
  font-weight: bold;
}
</style>
