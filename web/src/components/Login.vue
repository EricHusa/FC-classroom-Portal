<template>
  <div>
    <section class="hero is-primary">
      <div class="hero-body">
        <div class="container has-text-centered">
          <h2 class="title">Login</h2>
          <p class="subtitle error-msg">{{ errorMsg }}</p>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <div class="field">
          <label class="label  is-large" for="email">Username:</label>
          <div class="control">
            <input
              type="email"
              class="input is-large"
              id="email"
              v-model="email"
            />
          </div>
        </div>
        <div class="field">
          <label class="label  is-large" for="password">Password:</label>
          <div class="control">
            <input
              type="password"
              class="input is-large"
              id="password"
              v-model="password"
            />
          </div>
        </div>
        <br />
        <div class="control">
          <button class="button is-large is-primary" @click="authenticate">
            Student
          </button>
          <button class="button is-large is-success" @click="register">
            Teacher
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { EventBus } from "../utils";
export default {
  data() {
    return {
      email: "",
      password: "",
      errorMsg: ""
    };
  },
  methods: {
    authenticate() {
      // this.$store.dispatch('login', { email: this.email, password: this.password })
      //   .then(() => this.$router.push('/'))
      this.$store.dispatch("device", "913")
      this.$store.dispatch("dev", "student").then(() => this.$router.push("/"));

      //alert('Hello ')
    },
    register() {
      this.$store.dispatch("dev", "teacher").then(() => this.$router.push("/"));
      //    this.$store.dispatch('register', { email: this.email, password: this.password })
      //      .then(() => this.$router.push('/')).catch(e => {
      // alert(e);
    }
  },
  mounted() {
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
.error-msg {
  color: red;
  font-weight: bold;
}
</style>
