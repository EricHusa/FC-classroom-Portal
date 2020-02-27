<template>
  <div class="center">
    <ScopeSelector />
    <br />
    <button><router-link to="/home">Home</router-link></button>
  </div>
</template>

<script>
import ScopeSelector from "../components/ScopeSelector";
export default {
  name: "Settings",
  components: { ScopeSelector }
};
</script>

<style>
.center {
  margin: auto;
  width: 60%;
  padding: 10px;
}
</style>
