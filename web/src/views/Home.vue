<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <LoginMessage msg="Login" />
  </div>
</template>

<script>
// @ is an alias to /src
import LoginMessage from "@/components/Login.vue";

export default {
  name: "home",
  components: {
    LoginMessage
  }
};
</script>
