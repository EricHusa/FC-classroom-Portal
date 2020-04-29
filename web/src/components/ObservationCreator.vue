<template>
  <div class="observation-creator-dropdown">
    <b-row></b-row>
    <b-col>
      <b-alert
        :show="updateAlert"
        dismissible
        fade
        variant="success"
        @dismissed="resetAlert"
      >
        Observation updated!
      </b-alert>
      <b-form class="my-1" @submit="onSubmit" @reset="onReset" v-if="show">
        <b-row v-for="item in options" :key="item.key">
          <b-col sm="3">
            <label
              :id="`observation-creation-${item.key}-label`"
              :label-for="`observation-creation-${item.key}-input`"
              >{{ item.label }}:</label
            ></b-col
          >
          <b-col sm="9"
            ><b-form-input
              :id="`observation-creation-${item.key}-input`"
              v-model="form[item.key]"
              :required="item.required"
              :type="item.type"
            ></b-form-input
          ></b-col>
        </b-row>

        <b-row class="my-1">
          <b-col sm="3">
            <label
              id="observation-creation-type-label"
              label-for="observation-creation-type-input"
              >Information type:</label
            ></b-col
          >
          <b-col sm="9"
            ><b-form-select
              id="observation-creation-type-input"
              v-model="form.type"
              :options="types"
              required
            ></b-form-select
          ></b-col>
        </b-row>

        <b-row class="my-1">
          <b-col sm="3">
            <label
              id="observation-creation-students-label"
              label-for="observation-creation-students-input"
              >Collaborators:</label
            ></b-col
          >
          <b-col sm="9"
            ><b-form-select
              id="observation-creation-students-input"
              v-model="form.collaborators"
              :options="studentsList"
              required
              multiple
              description="CTRL + click to select multiple students"
            ></b-form-select
          ></b-col>
        </b-row>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button
          type="reset"
          variant="danger"
          :disabled="currentValues !== undefined"
          >Clear</b-button
        >
      </b-form>
    </b-col>
    <hr />
  </div>
</template>

<script>
import api from "../api/index.js";
import CreatorOptions from "../constants/CreatorOptions.ts";
export default {
  name: "AssignmentCreator",
  props: {
    currentValues: {}
  },
  data() {
    return {
      createdAlert: 0,
      show: true,
      studentsList: [],
      updateAlert: 0,
      form: {
        id: null,
        title: null,
        description: null,
        type: [],
        updated: null,
        collaborators: []
      },
      options: CreatorOptions.observationOptions.options,
      types: CreatorOptions.observationOptions.types
    };
  },
  beforeMount: function() {
    this.studentsList = api.getStudentCheckboxes(this.$store.state.currentExperiment.id);
  },
  mounted() {
    if (this.currentValues !== undefined) {
      for (const [key] of Object.entries(this.form)) {
        this.form[key] = this.currentValues[key];
      }
    }
  },
  methods: {
    resetForm() {
      for (const [key] of Object.entries(this.form)) {
        if (key != "id") {
          this.form[key] = null;
        }
      }
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.updateAlert = 3;
      let copyForm = Object.assign({}, this.form);
      this.$emit("observationCreated", copyForm);
      if (this.currentValues == undefined) {
        this.onReset(evt);
      }
    },
    onReset(evt) {
      evt.preventDefault();
      this.resetForm();
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
    resetAlert() {
      this.updateAlert = 0;
    }
  }
};
</script>

<style scoped>
.assignment-creator-dropdown {
  background-color: #f2f2f2;
  margin: 0.25rem;
}
</style>
