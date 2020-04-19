<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  /*padding-top: 10px;*/
  /*padding-bottom: 5px;*/
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-image: linear-gradient(
    to bottom left,
    #344675,
    #263148,
    #344675
  ) !important;
  text-align: center;
}

#nav a {
  font-weight: bold;
  color: white;
  text-align: center;
}

#nav li a {
  color: #007bff;
}

/*#nav a.router-link-exact-active {*/
/*  color: #42b983;*/
/*}*/
</style>

<script>
import NavOptions from "./constants/NavOptions.ts";
export default {
  data() {
    return {
      options: NavOptions[this.$store.state.role],
      roley: this.$store.state.role
    };
  },
  mounted: function() {
    //this.options = NavOptions[this.$store.state.role];
  }
};
</script>
