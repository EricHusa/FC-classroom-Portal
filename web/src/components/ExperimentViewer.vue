<template>
  <div>
    <b-alert
      :show="updateAlert"
      dismissible
      fade
      variant="success"
      @dismissed="resetAlert"
    >
      Experiment {{ updateAction }}
    </b-alert>
    <b-overlay :show="experiment.id===deleted" rounded="sm">
      <b-jumbotron
        ><h2>{{ experiment.title }}</h2>
        <hr />
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
                :placeholder="experiment[item.key]"
                v-model="form[item.key]"
                :disabled="checkRole()"
              ></b-form-input>
            </b-col>
          </b-row>
        </b-container>
        <b-row class="my-1">
          <b-col sm="3">
            <label><code>Students</code>:</label>
          </b-col>
          <b-col sm="9">
            <b-dropdown
              text="Select students"
              menu-class="w-100"
              variant="light"
              style="width: 95%; margin: auto;"
              :disabled="checkRole()"
              block
            >
              <b-dropdown-form>
                <b-form-checkbox-group
                  v-model="experiment.students"
                  :options="getStudentCheckboxes()"
                  name="flavour-2a"
                  stacked
                ></b-form-checkbox-group>
              </b-dropdown-form>
            </b-dropdown>
          </b-col>
        </b-row>
        <b-collapse
          id="experiment-update-section"
          :visible="!checkRole() && experiment.id"
        >
          <b-row>
            <b-col sm="3">
              <b-button @click="deleteExperiment()" variant="danger"
                >Delete</b-button
              ></b-col
            >
            <b-col sm="9"
              ><b-button @click="updateExperiment()" variant="warning"
                >Update info</b-button
              ></b-col
            >
          </b-row>
          <b-collapse id="add-students-to-experiment">
            <div style="text-align: center;">
              <b-form-group style="text-align: left; display: inline-block">
                <b-form-checkbox-group
                  v-model="selectedStudents"
                  :options="getStudentCheckboxes()"
                  name="flavour-2a"
                  stacked
                ></b-form-checkbox-group>
              </b-form-group>
            </div>
          </b-collapse>
        </b-collapse>
        <b-collapse
          id="experiment-create-section"
          :visible="!checkRole() && !experiment.id"
        >
          <b-button
            @click="createExperiment()"
            variant="success"
            style="float: right;"
            >Add experiment</b-button
          >
        </b-collapse>
      </b-jumbotron>
      <template v-slot:overlay>
        <div class="text-center">
          <b-icon icon="x-circle-fill" font-scale="3"></b-icon>
          <p id="cancel-label">Please select or create another experiment.</p>
        </div>
      </template>
    </b-overlay>
  </div>
</template>

<script>
import TableHeaders from "../constants/TableHeaders.ts";
import api from "../api/index.js";
export default {
  props: {
    experiment: Object,
    form: Object
  },
  data() {
    return {
      updateAlert: 0,
      deleteAlert: 0,
      updateAction: "",
      deleted: null,
      selectedStudents: [1],
      fields: TableHeaders.experiments
    };
  },
  methods: {
    checkRole() {
      return this.$store.state.role == "student";
    },
    deleteExperiment() {
      if (confirm("Are you sure you want to delete this experiment?")) {
        api.deleteExperiment(this.experiment.id);
        //this.experiment = { title: "Deleted", deleted: true };
        this.deleted = this.experiment.id
        this.$store.state.currentExperiment = null;
        this.updateAction = "deleted";
        this.updateAlert = 3;
        this.$emit("experimentsChanged");
      }
    },
    createExperiment() {
      this.experiment = api.createExperiment(
        this.form,
        this.$store.state.currentUser.id
      );
      this.updateAction = "created";
      this.updateAlert = 3;
      this.$emit("experimentsChanged", this.experiment.id);
    },
    updateExperiment() {
      let updateValues = this.form;
      updateValues.students = this.experiment.students;
      api.updateExperiment(this.experiment.id, updateValues);
      this.experiment = api.getExperiment(this.experiment.id);
      this.updateAction = "updated";
      this.updateAlert = 3;
    },
    getStudentCheckboxes() {
      return api.getStudentCheckboxes();
    },
    inExperiment(studentId) {
      if (this.experiment.students.includes(studentId)) {
        return "success";
      } else {
        return "default";
      }
    },
    changeInvolvement(studentId) {
      api.changeExperimentInvolvement(this.experiment.id, studentId);
      this.$refs.dropdown.show(true);
    },
    resetAlert() {
      this.updateAlert = 0;
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
