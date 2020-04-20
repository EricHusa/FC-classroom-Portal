<template>
  <div>
      <b-alert :show="updateAlert" dismissible fade variant="success">
      Experiment updated
    </b-alert>
      <b-jumbotron ><h2>{{experiment.title}}</h2><hr>
      <b-container fluid>
    <br />
    <b-row class="my-1" v-for="item in fields" :key="item.key">
      <b-col sm="3">
        <label :for="`type-${item.name}`"
          ><code>{{ item.name }}</code
          >:</label
        >
      </b-col>
      <b-col sm="9">
        <b-form-input
          :id="`type-${item.type}`"
          :type="item.type"
          :value="experiment[item.key]"
          v-model="form[item.key]"
          :disabled="checkRole()"
        ></b-form-input>
      </b-col>
    </b-row>
  </b-container>
          <b-button
          @click="updateExperiment()"
          variant="success"
          >Update information</b-button
        >
      </b-jumbotron>
  </div>
</template>

<script>
import ExperimentData from "../constants/ExperimentData.ts";
import api from "../api/index.js";
export default {
  props: {
    experiment: Object,
      form: Object
  },
  data() {
    return {
    experimentInfo: { name: "You have no experiments" },
    updateAlert: 0,
    fields: ExperimentData.fields
  }},
  methods: {
      checkRole() {
      return this.$store.state.role == "student";
    },
      updateExperiment() {
      api.updateExperiment(this.experiment.id, this.form);
      this.experiment = api.getExperiment(this.experiment.id)
      this.updateAlert = 3;
    }
  },
  mounted() {
    this.form.description = this.experiment.description;
    this.form.plant = this.experiment.plant;
    this.form.start_date = this.experiment.start_date;
  }
};
</script>

<style scoped></style>
