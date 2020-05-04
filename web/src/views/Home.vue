<template>
  <div>
    <NavBar />
    <div>
      <b-overlay :show="loading" rounded="sm">
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
                        ><b-button @click="createExperiment()" variant="success"
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
                  v-bind:devices="devices"
                  @experimentsChanged="refreshExperimentList"
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
                    ><AssignmentCreator
                          @assignmentCreated="createAssignment"
                          v-bind:studentsList="studentCheckboxes"
                            v-bind:updating="false"
                  /></b-collapse>
                  <h3>Singular Assignments</h3>
                  <div>
                    <b-table :fields="assignmentHeaders" :items="formattedAssignments">
                      <!--                      <template v-slot:cell(action)="data">-->
                      <!--                        <b-icon-->
                      <!--                          :id="`comment-notification-${data.item.id}`"-->
                      <!--                          icon="exclamation-circle"-->
                      <!--                          font-scale="2"-->
                      <!--                          :hidden="role == 'teacher && responses[data.item.id].comments == null"-->
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
                          v-bind:studentsList="studentCheckboxes"
                            v-bind:currentValues="data.item"
                            v-bind:updating="true"
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
                    @assignmentDeleted="refreshAssignmentList"
                    @updateResponseList="setAssignment"
                  />
                </b-col>
              </b-row>
            </div>
          </b-tab>

          <b-tab title="Observations" :disabled="$store.state.currentExperiment==null">
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
                    <b-table :fields="observationHeaders" :items="formattedObservations">
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
                            v-bind:studentList="activeExperiment.students"
                          />
                        </b-card>
                      </template>
                    </b-table>
                  </div>
                </b-col>
                <b-col sm="6">
                  <ObservationViewer v-bind:observation="activeObservation"
                                     v-bind:responses="observationResponses"
                                     @observationDeleted="refreshObservations"
                                    @observationUpdated="refreshObservations"/>
                </b-col>
              </b-row>
            </div>
          </b-tab>

          <b-tab title="Data" :disabled="$store.state.currentExperiment==null">
            <div>
              <ChartViewer v-bind:dataName="'temperature'" v-bind:xDataUnit="'C'"/>
              <hr/>
              <ChartViewer v-bind:dataName="'humidity'" v-bind:xDataUnit="'%'"/>
            </div>
          </b-tab>

          <b-tab title="Images" :disabled="$store.state.currentExperiment==null">
            <div>
              <ImageViewer />
            </div>
          </b-tab>
        </b-tabs>
      </b-card>
        </b-overlay>
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
      observationResponses: [],
      responses: [],
      devices: [],
      assignmentHeaders: TableHeaders.assignments,
      observationHeaders: TableHeaders.observations,
      activeExperiment: {},
      activeAssignment: {},
      activeResponse: {},
      activeObservation: {},
      studentCheckboxes: [],
      formattedAssignments: [],
      formattedObservations: [],
      loading: false,
      experimentForm: {
        title: null,
        description: null,
        plant: null,
        start_date: null,
        student_ids: []
      }
    };
  },
  beforeMount() {
    this.loading = true;
    this.refreshStudents();
    this.refreshClasses();
    this.refreshDeviceList();
    this.refreshExperimentList();
    if (this.experiments.length > 0) {
      this.setExpi(this.experiments[0].id);
    } else {
      this.setExpi(null);
    }
    this.refreshAssignmentList();
    this.loading = false;
  },
  computed: {
    addColors() {
      let rows = this.assignments.map(item => {
        let tmp = item;
        if (this.$store.state.role === "student") {
          // let student_responses = this.refreshStudentAssignmentResponses();
          let res = this.responses[item.id];
          // alert("res is: ");
          // alert(JSON.stringify(res));
          res.submitted === null || res.submitted === undefined || res.submitted === "None"
            ? (tmp._rowVariant = "warning")
            : (tmp._rowVariant = "success");
        }
        let d = new Date(item.due_date.replace(/-/g, '/'));
        tmp.due_date = d.toDateString();
        return tmp;
      });
      return rows;
    },
    formatDates() {
      if (this.observations.length > 0) {
        let rows = this.observations.map(item => {
          let tmp = item;
          let d = new Date(item.updated);
          tmp.updated = d.toDateString();
          return tmp;
        });
        return rows;
      }
      else{
        return [];
      }
    },
    formatObservationDates() {
      let rows = this.observationResponses.map(item => {
        let tmp = item;
        if (item.submitted != null) {
          let d = new Date(item.submitted);
          tmp.submitted = d.toDateString();
        }
        return tmp;
      });
      return rows;
    }
  },
  methods: {
    async setExpi(id = null) {
      if(id===null){return;}
      this.activeExperiment = api.getExperiment(id);
      this.$store.state.currentExperiment = this.activeExperiment;
      for (let k in this.experimentForm) {
        this.experimentForm[k] = this.activeExperiment[k];
      }
      this.experimentForm.student_ids = api.getStudentIdList(this.activeExperiment.students);
      this.observations = await api.setLocalObservations().then(function(response) {
        return response;
      }).catch(function (error) {
        alert(error);
        return;
      });
      // this.refreshObservations();
      },

    createExperiment() {
      this.activeExperiment = { title: "New Experiment", device: this.devices[0], student_ids: [], students: [], start_date: api.getToday(new Date()) };
      this.$store.state.currentExperiment = null;
      for (let k in this.experimentForm) {
        this.experimentForm[k] = this.activeExperiment[k];
      }
    },
    async refreshExperimentList(newItem=null){
      this.experiments = await api.setLocalExperiments().then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      if(newItem !== null){
        this.setExpi(newItem);
      }
    },
    async refreshStudentAssignmentResponses(){
      this.responses = await api.setLocalStudentAssignmentResponses(this.$store.state.currentUser.id).catch(function (error) {
        alert(error);
      });
      this.formattedAssignments = this.addColors;
      // alert(JSON.stringify(this.responses));
      // return this.responses;
    },
    async refreshAssignmentList(){
      this.assignments = await api.setLocalAssignments().then(function(response) {
        return response;
      }).catch(function (error) {
        alert(error);
        return;
      });
      if (this.role == "student") {
        this.refreshStudentAssignmentResponses();
    }
      else {
        this.formattedAssignments = this.addColors;
      }
      this.activeAssignment = {};
    },
    async setAssignment(assignment) {
      this.activeAssignment = assignment;
      if (this.role == "student") {
        this.activeResponse = api.getStudentAssignmentResponse(
          assignment.id
        );
      } else {
        this.responses = await api.getTeacherAssignmentResponses(
          this.activeAssignment.id
        ).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
      });
      }
    },
    async createAssignment(values) {
      await api.createAssignment(values).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      this.assignments = await api.setLocalAssignments().then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
    },
    async createObservation(values) {
      await api.createObservation(values).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      this.refreshObservations();
    },
    async updateObservation(values) {
      this.activeObservation = await api.updateObservation(values.id, values).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      this.refreshObservations();


      //api.updateObservation(values.id, values);
    },
    // getObservationResponses(){
    //   return [];
    // },
    setObservation(obs) {
      this.activeObservation = obs;
      this.observationResponses = this.formatObservationDates;
    },
    async refreshObservations(){
      this.observations = await api.setLocalObservations().then(function(response) {
        return response;
      }).catch(function (error) {
        alert(error);
        return;
      });
      this.formattedObservations = this.formatDates;
    },

    async updateAssignment(values) {
      this.activeAssignment = await api.updateAssignment(values.id, values).then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
      this.assignments = await api.setLocalAssignments().then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
      });
    },
    async refreshClasses(){
      await api.setLocalClasses().then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
        return;
      });
    },
    async refreshStudents(){
      await api.setLocalStudents().then(function (response) {
          return response;
        }).catch(function (error) {
        alert(error);
      });
      this.studentCheckboxes = api.getStudentCheckboxes();
    },
    async refreshDeviceList(){
      this.devices = await api.setLocalDevices().then(function(response) {
        return response;
      }).catch(function (error) {
        alert(error);
        return;
      });
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
