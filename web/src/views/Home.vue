<template>
  <div>
    <NavBar />
    <div>
      <b-card no-body>
        <b-tabs card justified>
          <b-tab title="Experiment">
            <b-row>
              <b-col sm="6">
                <b-card-group deck>
                  <b-card-group v-for="item in experiments" :key="item.name">
                    <b-card
                      :border-variant="getVariant(item.id, 'border')"
                      :header-bg-variant="getVariant(item.id, 'header')"
                      :header="item.title"
                      header-border-variant="secondary"
                      style="max-width: 13rem; max-height: 14rem; min-width: 13rem; min-height: 14rem;"
                    >
                      <b-card-text>{{ item.description }}</b-card-text>
                      <b-form-radio-group buttons>
                        <b-form-radio
                          :id="`exp-select-${item.id}`"
                          :value="item.id"
                          button-variant="default"
                          size="lg"
                          :checked="item.id == activeExperiment.id"
                          style="vertical-align: sub;"
                        >
                          <b-button @click="setExpi(item.id)" variant="primary"
                            >Select experiment</b-button
                          ></b-form-radio
                        ></b-form-radio-group
                      >
                    </b-card>
                  </b-card-group>
                  <b-overlay :show="role == 'student'">
                    <b-card
                      border-variant="secondary"
                      bg-variant="success"
                      header="Create Experiment"
                      style="max-width: 13rem; max-height: 14rem; min-width: 13rem; min-height: 14rem;"
                      ><b-card-text
                        ><b-button @click="setExpi()" variant="success"
                          ><b-icon
                            icon="plus-square-fill"
                            font-scale="5"
                          ></b-icon></b-button></b-card-text
                    ></b-card>
                    <template v-slot:overlay>
                      <b-icon
                        id="experiment-blocker"
                        icon="x-circle-fill"
                        font-scale="2"
                      ></b-icon>
                      <b-popover
                        target="experiment-blocker"
                        placement="bottom"
                        triggers="hover focus"
                        content="Only teachers can create experiments right now"
                      ></b-popover>
                    </template>
                  </b-overlay>
                </b-card-group>
              </b-col>
              <b-col sm="6">
                <ExperimentViewer
                  v-bind:experiment="activeExperiment"
                  v-bind:form="experimentForm"
                />
              </b-col>
            </b-row>
          </b-tab>

          <b-tab title="Assignments">
            <div>
              <b-row>
                <b-col sm="6">
                  <b-button
                    v-b-toggle.assignment-creator
                    variant="success"
                    :hidden="role == 'student'"
                    >New Assignment</b-button
                  >
                  <b-collapse id="assignment-creator"
                    ><AssignmentCreator @assignmentCreated="createAssignment"
                  /></b-collapse>
                  <h3>Singular Assignments</h3>
                  <div>
                    <b-table :fields="assignmentHeaders" :items="addColors">
                      <!--                      <template v-slot:cell(action)="data">-->
                      <!--                        <b-icon-->
                      <!--                          :id="`comment-notification-${data.item.id}`"-->
                      <!--                          icon="exclamation-circle"-->
                      <!--                          font-scale="2"-->
                      <!--                          :hidden="responses[data.item.id].comments == null"-->
                      <!--                        ></b-icon>-->
                      <!--                        <b-popover-->
                      <!--                          :target="`comment-notification-${data.item.id}`"-->
                      <!--                          placement="bottom"-->
                      <!--                          triggers="hover focus"-->
                      <!--                          :content="responses[data.item.id].comments"-->
                      <!--                        ></b-popover>-->
                      <!--                      </template>-->
                      <template v-slot:cell(action)="row">
                        <b-button
                          :hidden="role == 'teacher'"
                          @click="setAssignment(row.item)"
                          >View</b-button
                        >
                        <b-button
                          :hidden="role == 'student'"
                          size="md"
                          @click="row.toggleDetails"
                          class="mr-2"
                          >Update</b-button
                        >
                        <b-button
                          :hidden="role == 'student'"
                          @click="setAssignment(row.item)"
                          >Results</b-button
                        >
                      </template>
                      <template v-slot:row-details="data">
                        <b-card>
                          <!--                          <b-card-text>{{data.item.id}}</b-card-text>-->
                          <AssignmentCreator
                            @assignmentCreated="updateAssignment"
                            v-bind:currentValues="data.item"
                          />
                        </b-card>
                      </template>
                    </b-table>
                  </div>
                </b-col>
                <b-col sm="6">
                  <AssignmentViewer
                    v-bind:assignment="activeAssignment"
                    v-bind:response="activeResponse"
                    v-bind:responseList="responses"
                  />
                </b-col>
              </b-row>
            </div>
          </b-tab>

          <b-tab title="Observations">
            <br />
            <div>
              <b-row>
                <b-col sm="6">
                  <b-button
                    v-b-toggle.observation-creator
                    variant="success"
                    :hidden="role == 'student'"
                    >New Observation</b-button
                  >
                  <b-collapse id="observation-creator"
                    ><ObservationCreator @observationCreated="createObservation"
                  /></b-collapse>
                  <h3>Experiment Observations</h3>
                  <div>
                    <b-table :fields="observationHeaders" :items="formatDates">
                      <template v-slot:cell(action)="row">
                        <b-button
                          :hidden="role == 'student'"
                          size="md"
                          @click="row.toggleDetails"
                          class="mr-2"
                          >Update</b-button
                        >
                        <b-button @click="setObservation(row.item)"
                          >View</b-button
                        >
                      </template>
                      <template v-slot:row-details="data">
                        <b-card>
                          <ObservationCreator
                            @observationCreated="updateObservation"
                            v-bind:currentValues="data.item"
                          />
                        </b-card>
                      </template>
                    </b-table>
                  </div>
                </b-col>
                <b-col sm="6">
                  <ObservationViewer v-bind:observation="activeObservation" />
                </b-col>
              </b-row>
            </div>
          </b-tab>

          <b-tab title="Data">
            <div>
              <ChartViewer v-bind:dataName="'temperature'" v-bind:xDataUnit="'C'"/>
              <hr/>
              <ChartViewer v-bind:dataName="'humidity'" v-bind:xDataUnit="'%'"/>
            </div>
          </b-tab>

          <b-tab title="Images">
            <div>
              <ImageViewer />
            </div>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import NavBar from "../components/NavBar";
import ImageViewer from "../components/ImageViewer";
import api from "../api/index.js";
import ExperimentViewer from "../components/ExperimentViewer";
import AssignmentCreator from "../components/AssignmentCreator";
import TableHeaders from "../constants/TableHeaders.ts";
import AssignmentViewer from "../components/AssignmentViewer";
import ObservationCreator from "../components/ObservationCreator";
import ObservationViewer from "../components/ObservationViewer";
import ChartViewer from "../components/ChartViewer";
export default {
  name: "HomePage",
  components: {
    NavBar,
    ImageViewer,
    ExperimentViewer,
    AssignmentCreator,
    AssignmentViewer,
    ObservationCreator,
    ObservationViewer,
    ChartViewer
  },
  data() {
    return {
      role: this.$store.state.role,
      experiments: [],
      assignments: [],
      observations: [],
      responses: [],
      assignmentHeaders: TableHeaders.assignments,
      observationHeaders: TableHeaders.observations,
      activeExperiment: {},
      activeAssignment: {},
      activeResponse: {},
      activeObservation: {},
      experimentForm: {
        title: null,
        description: null,
        plant: null,
        start_date: null
      }
    };
  },
  beforeMount() {
    this.experiments = api.getExperiments(
      this.$store.state.role,
      this.$store.state.currentUser.id
    );
    if (this.experiments.length > 0) {
      this.setExpi(this.experiments[0].id);
    } else {
      this.setExpi(null);
    }
    this.assignments = api.getAssignments(
      this.$store.state.role,
      this.$store.state.currentUser.id
    );
    if (this.role == "student") {
      this.responses = api.getStudentAssignmentResponses(
        this.$store.state.currentUser.id
      );
    }
    this.observations = api.getObservations();
  },
  computed: {
    addColors() {
      let rows = this.assignments.map(item => {
        let tmp = item;
        if (this.$store.state.role == "student") {
          let pos = this.responses
            .map(function(r) {
              return r.assignment;
            })
            .indexOf(item.id);
          this.responses[pos].submitted == null
            ? (tmp._rowVariant = "warning")
            : (tmp._rowVariant = "success");
        }
        let d = new Date(item.due_date);
        tmp.due_date = d.toDateString();
        return tmp;
      });
      return rows;
    },
    formatDates() {
      let rows = this.observations.map(item => {
        let tmp = item;
        let d = new Date(item.updated);
        tmp.updated = d.toDateString();
        return tmp;
      });
      return rows;
    }
  },
  methods: {
    setExpi(id = null) {
      this.activeExperiment = api.getExperiment(id);
      this.$store.state.currentExperiment = this.activeExperiment;
      for (let k in this.experimentForm) {
        this.experimentForm[k] = this.activeExperiment[k];
      }
      this.experiments = api.getExperiments(
        this.$store.state.role,
        this.$store.state.currentUser.id
      );
      this.observations = api.getObservations();
    },
    setAssignment(assignment) {
      this.activeAssignment = assignment;
      if (this.role == "student") {
        this.activeResponse = api.getStudentAssignmentResponse(
          assignment.id,
          this.$store.state.currentUser.id
        );
      } else {
        this.responses = api.getTeacherAssignmentResponses(
          this.activeAssignment.id
        );
      }
    },
    createAssignment(values) {
      api.createAssignment(values);
      this.assignments = api.getAssignments(
        this.$store.state.role,
        this.$store.state.currentUser.id
      );
    },
    createObservation(values) {
      api.createObservation(values);
    },
    updateObservation(values) {
      this.activeObservation = api.updateObservation(values.id, values);
    },
    setObservation(obs) {
      this.activeObservation = obs;
    },

    updateAssignment(values) {
      api.updateAssignment(values.id, values);
    },
    getVariant(id, type) {
      if (id == this.activeExperiment.id) {
        return "info";
      } else {
        if (type == "header") {
          return "light";
        } else {
          return "secondary";
        }
      }
    }
  }
};
</script>

<style>
form {
  margin-bottom: 5px;
  margin-top: 5px;
}
</style>
