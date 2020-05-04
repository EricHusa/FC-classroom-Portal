<template>
  <div>
    <b-alert
      :show="observationUpdated"
      dismissible
      fade
      variant="success"
      @dismissed="resetAlert"
    >
      Observation report updated!
    </b-alert>
    <b-alert
      :show="observationError"
      dismissible
      fade
      variant="danger"
      @dismissed="resetAlert"
    >
      {{ errMsg }}
    </b-alert>
    <b-overlay :show="observation.id === undefined || deleted === observation.id" rounded="sm">
    <b-jumbotron
      ><h2>{{ observation.title }}</h2>
      <code>{{ observation.units }}</code>
      <hr />
      <div id="observation-graph"></div>
      <div>
        <p>{{ observation.description }}</p>
        <b-row>
          <b-button
            @click="addObservation"
            variant="info"
            :hidden="role == 'student' || deleted === observation.id"
            >New Report Row</b-button
          >
        </b-row>
        <h3>Observations Records</h3>
        <div>
          <b-table :fields="observationHeaders" :items="responses">
            <template v-slot:cell(response)="data">
              <b-form-input
                :id="`observation-response-input-${data.item.id}`"
                :type="observation.type"
                :disabled="unlocked != data.item.id || !data.item.editable"
                step="0.01"
                min="0.00"
                v-model="response.response"
              ></b-form-input>
            </template>
            <template v-slot:cell(action)="row">
              <b-button
                :hidden="role=='teacher' || deleted === observation.id"
                @click="unlocked = row.item.id"
                >Change</b-button
              >
              <b-button
                :hidden="role == 'student' || deleted === observation.id"
                size="md"
                @click="row.toggleDetails"
                class="mr-2"
                >Manage</b-button
              >
              <b-button
                @click="updateObservation(row.item.id, row.item.response)"
                variant="success"
                :hidden="deleted === observation.id"
                >Update</b-button
              >
            </template>
            <template v-slot:row-details="data">
              <b-row>
                <b-button
                  variant="danger"
                  @click="deleteReport(data.item.id)"
                  :hidden="deleted === observation.id"
                  >Delete report</b-button
                >
                <b-button
                  variant="light"
                  @click="unlockResponse(data.item.id)"
                  :hidden="deleted === observation.id"
                  >Change</b-button
                >
                <b-button
                  variant="warning"
                  @click="changeEditPermission(data.item.id)"
                  :hidden="deleted === observation.id"
                  >Lock / Unlock</b-button
                >
              </b-row>
            </template>
          </b-table>
        </div>
        <b-row>
          <b-button
            @click="deleteObservation"
            variant="danger"
            :hidden="role == 'student' || deleted === observation.id"
            >Delete Observation</b-button
          >
        </b-row>
      </div>
    </b-jumbotron>
      <template v-slot:overlay>
        <div class="text-center">
          <b-icon icon="x-circle-fill" font-scale="3"></b-icon>
          <p id="cancel-label">Please select or create another observation.</p>
        </div>
      </template>
    </b-overlay>
  </div>
</template>

<script>
import TableHeaders from "../constants/TableHeaders.ts";
import api from "../api/index.js";
export default {
  name: "ObservationViewer",
  props: {
    observation: Object,
    responses: Array
  },
  data() {
    return {
      observationHeaders: TableHeaders.observationResponse,
      // responses: [],
      unlocked: null,
      observationUpdated: 0,
      observationError: 0,
      reportInputs: {},
      role: null,
      deleted: false,
      errMsg: ""
    };
  },
  mounted() {
    // if (this.observation !== undefined) {
      // for (let r in this.observation.responses) {
      //   let resp = this.observation.responses[r];
      //   this.reportInputs[resp.number] = resp.response;
      // }
      // this.responses = this.observation.responses;
    // }
    this.role = this.$store.state.role;
  },
  // computed: {
  //   formatObservationDates() {
  //     let rows = this.observation.responses.map(item => {
  //       let tmp = item;
  //       if (item.submitted != null) {
  //         let d = new Date(item.submitted);
  //         tmp.submitted = d.toDateString();
  //       }
  //       return tmp;
  //     });
  //     return rows;
  //   }
  // },
  methods: {
    async updateObservation(responseId, responseVal) {
      if (this.observation.type == "number") {
        responseVal = parseFloat(responseVal);
        if (isNaN(responseVal)) {
          this.errMsg = "Your response must be a number";
          this.observationError = 3;
          return;
        }
        responseVal = responseVal.toFixed(2);
      }
      await api.updateObservationResponse(
        this.observation.id,
        responseId,
        this.$store.state.currentUser.id,
        responseVal
      ).then(function(response) {
        return response;
      }).catch(function (error) {
        alert(error);
        return;
      });
      this.$emit("observationUpdated");
      this.unlocked = null;
      this.observationUpdated = 3;
    },
    async addObservation() {
      await api.addObservationResponse(this.observation.id).then(function(response) {
        return response;
      }).catch(function (error) {
        alert(error);
        return;
      });
      this.$emit("observationUpdated");
    },
    async deleteObservation() {
      if (
        confirm("Are you sure you want to permanently delete this observation?")
      ) {
        this.deleted = this.observation.id;
        await api.deleteObservation(this.observation.id).then(function(response) {
        return response;
      }).catch(function (error) {
        alert(error);
        return;
      });
        this.$emit("observationDeleted")
      }
    },
    resetAlert() {
      this.observationUpdated = 0;
      this.observationError = 0;
    },
    getIndex(responseNumber) {
      let index = this.observation.responses
        .map(function(e) {
          return e.number;
        })
        .indexOf(responseNumber);
      return index;
    },
    unlockResponse(responseNumber) {
      this.unlocked = responseNumber;
    },
    changeEditPermission(responseNumber) {
      api.updateObservationResponseLock(this.observation.id, responseNumber);
    },
    deleteReport(responseNumber) {
      if (confirm("Are you sure you want to delete this report?")) {
        this.observation = api.deleteObservationResponse(
          this.observation.id,
          responseNumber
        );
      }
    }
  }
};
</script>

<style scoped></style>
