<template>
  <div class="assignment-creator-dropdown">
    <b-row></b-row>
    <b-col>
      <b-alert :show="createdAlert" dismissible fade variant="success">
        Assignment created!
      </b-alert>
      <b-form class="my-1" @submit="onSubmit" @reset="onReset" v-if="show">
        <b-row v-for="item in options" :key="item.key">
          <b-col sm="3">
            <label
              :id="`assignment-creation-${item.key}-label`"
              :label-for="`assignment-creation-${item.key}-input`"
              >{{ item.label }}:</label
            ></b-col
          >
          <b-col sm="9"
            ><b-form-input
              :id="`assignment-creation-${item.key}-input`"
              v-model="form[item.key]"
              :required="item.required"
              :type="item.type"
            ></b-form-input
          ></b-col>
        </b-row>

        <b-row class="my-1">
          <b-col sm="3">
            <label
              id="assignment-creation-type-label"
              label-for="assignment-creation-type-input"
              >Information type:</label
            ></b-col
          >
          <b-col sm="9"
            ><b-form-select
              id="assignment-creation-type-input"
              v-model="form.type"
              :options="types"
              required
            ></b-form-select
          ></b-col>
        </b-row>

        <b-row class="my-1">
          <b-col sm="3">
            <label
              id="assignment-creation-students-label"
              label-for="assignment-creation-students-input"
              >Assigned students:</label
            ></b-col
          >
          <b-col sm="9"
            ><b-form-select
              id="assignment-creation-students-input"
              v-model="form.assignees"
              :options="studentsList"
              required
              multiple
              description="CTRL + click to select multiple students"
            ></b-form-select
          ></b-col>
        </b-row>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Clear</b-button>
      </b-form>
    </b-col>
    <hr />
  </div>
</template>

<script>
import api from "../api/index.js";
export default {
  name: "AssignmentCreator",
  props: {
    students: Array,
    currentValues: {}
  },
  data() {
    return {
      createdAlert: 0,
      show: true,
      studentsList: [],
      form: {
        id: null,
        title: null,
        description: null,
        type: [],
        due_date: null,
        assignees: []
      },
      options: [
        { key: "title", label: "Title", required: true, type: "text" },
        {
          key: "description",
          label: "Description",
          required: false,
          type: "text"
        },
        { key: "due_date", label: "Due Date", required: true, type: "date" }
      ],
      types: [
        { text: "Written response", value: "text" },
        { text: "Numerical response", value: "number" }
      ]
    };
  },
  beforeMount: function() {
    this.studentsList = api.getStudentCheckboxes();
  },
  mounted() {
    if (this.currentValues !== undefined) {
      for (const [key] of Object.entries(this.form)) {
        this.form[key] = this.currentValues[key];
      }
      this.form.due_date = api.getToday(this.form.due_date);
    }
  },
  methods: {
    resetForm() {
      this.form.title = null;
      this.form.description = null;
      this.form.type = null;
      this.form.due_date = null;
      this.form.assignees = null;
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.updateAlert = 3;
      let copyForm = Object.assign({}, this.form);
      this.$emit("assignmentCreated", copyForm);
      this.onReset(evt);
    },
    onReset(evt) {
      evt.preventDefault();
      this.resetForm();
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
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
