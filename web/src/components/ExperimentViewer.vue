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
    <b-overlay :show="Object.keys(experiment).length === 0||experiment.id===deleted" rounded="sm">
      <b-jumbotron
        ><h2>{{ experiment.title }}</h2>
        <hr />
        <b-container fluid>
          <br />
          <b-row class="my-1" v-for="item in fields" :key="item.key">
            <b-col sm="3">
              <label :for="`type-${item.name}`"
                ><b>{{ item.name }}</b
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
                trim
                :disabled="checkRole()"
              ></b-form-input>
            </b-col>
          </b-row>

          <b-row class="my-1">
          <b-col sm="3">
            <label><b>Device</b>:</label>
          </b-col>
          <b-col sm="9">
            <b-form-select
              v-model="experiment.device.id"
              :options="formatDevices"
              :disabled="checkRole()"
              id="inline-form-input-system"
            ></b-form-select>
          </b-col>
        </b-row>

        <b-row class="my-1">
          <b-col sm="3">
            <label><b>Students</b>:</label>
          </b-col>
          <b-col sm="3">
            <b-dropdown
              text="Class"
              menu-class="w-100"
              variant="light"
              style="width: 100%; margin: auto;"
              :disabled="checkRole()"
            >
              <b-dropdown-form>
                <b-form-radio-group
                  v-model="currentClassScope"
                  :options="getClassCheckboxes()"
                  name="flavour-2a"
                  stacked
                ></b-form-radio-group>
              </b-dropdown-form>
            </b-dropdown><br/>
          </b-col>
          <b-col sm="6">
            <b-dropdown
              text="Select students"
              menu-class="w-100"
              variant="light"
              style="width: 100%; margin: auto;"
              :disabled="checkRole()"
            >
              <b-dropdown-form>
                <b-form-checkbox-group
                  v-model="form.student_ids"
                  :options="getStudentCheckboxes()"
                  name="flavour-2a"
                  stacked
                ></b-form-checkbox-group>
              </b-dropdown-form>
            </b-dropdown><br/>
          </b-col>
        </b-row>
          </b-container>

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
        </b-collapse>
        <b-collapse
          id="experiment-create-section"
          :visible="!checkRole() && !experiment.id"
        >
          <b-button
            @click="createExperiment"
            variant="success"
            style="float: right;"
            >Add experiment</b-button
          >
        </b-collapse>
      </b-jumbotron>
      <template v-slot:overlay>
        <div class="text-center">
          <b-icon icon="x-circle-fill" font-scale="3"></b-icon>
          <p id="cancel-label">Please select or create an experiment.</p>
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
    form: Object,
    devices: Array
  },
  data() {
    return {
      currentClassScope: null,
      updateAlert: 0,
      updateAction: "",
      deleted: null,
      selectedStudents: [], //delete?
      fields: TableHeaders.experiments
    };
  },
  computed: {
    formatDevices() {
      let rows = this.devices.map(item => {
        let tmp = {};
        tmp.text = item.name;
        tmp.value = item.id;
        return tmp;
      });
      return rows;
    }
  },
  methods: {
    checkRole() {
      return this.$store.state.role == "student";
    },
    async deleteExperiment() {
      if (confirm("Are you sure you want to delete this experiment?")) {
        await api.deleteExperiment(this.experiment.id).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
        //this.experiment = { title: "Deleted", deleted: true };
        this.deleted = this.experiment.id
        this.$store.state.currentExperiment = null;
        this.updateAction = "deleted";
        this.updateAlert = 3;
        this.$emit("experimentsChanged");
      }
    },
    addFormValues(form){
      let updateValues = form;
      if(this.experiment===undefined){
        updateValues.student_ids = [];
      }
      // else {
      //   updateValues.student_ids = this.experiment.students;
      // }
      // alert(JSON.stringify(this.experiment));
      updateValues.device_id = this.experiment.device.id;
      return updateValues
    },
    async createExperiment() {
      let updateValues = this.addFormValues(this.form);
      if(updateValues.title.length <=0 || updateValues.device_id === null){
        alert("New experiments must have at least a name and device assigned")
        return;
      }
      this.experiment = await api.createExperiment(updateValues).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      this.updateAction = "created";
      this.updateAlert = 3;
      this.$emit("experimentsChanged", this.experiment.id);
    },
    async updateExperiment() {
      let updateValues = this.addFormValues(this.form);
      this.experiment = await api.updateExperiment(this.experiment.id, updateValues).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      // this.experiment = api.getExperiment(this.experiment.id);
      this.updateAction = "updated";
      this.updateAlert = 3;
      this.$emit("experimentsChanged");
    },
    getStudentCheckboxes() {
      if(this.currentClassScope === null) {
        return api.getStudentCheckboxes();
      }
      else{
        return api.getStudentCheckboxes("class",this.currentClassScope);
      }
    },
    getClassCheckboxes(){
      return api.getClassCheckboxes();
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
