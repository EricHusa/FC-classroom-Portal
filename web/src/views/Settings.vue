<template>
  <div>
    <NavBar />
    <div class="center">
      <ScopeSelector />
      <br />
      <button><router-link to="/">Home</router-link></button>
    </div>
  </div>
</template>

<script>
import ScopeSelector from "../components/ScopeSelector";
import NavBar from "../components/NavBar";
export default {
  name: "Settings",
  components: { ScopeSelector, NavBar }
};
</script>

<style>
.center {
  margin: auto;
  width: 60%;
  padding: 10px;
}
</style>
