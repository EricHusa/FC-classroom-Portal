<template>
  <div>
      <b-jumbotron ><h2>{{experiment.name}}</h2><hr></b-jumbotron>
  </div>
</template>

<script>
export default {
  props: {
    experiment: Object
  },
  data() {
    return {
    experimentInfo: { name: "You have no experiments" },
  }},
  methods: {
  }
};
</script>

<style scoped></style>
