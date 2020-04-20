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
                      :header="item.name"
                      header-border-variant="secondary"
                      style="max-width: 20rem; max-height: 20rem;"
                    >
                      <b-card-text>{{ item.description }}</b-card-text>
                      <b-form-radio-group buttons>
                        <b-form-radio
                          :id="`exp-select-${item.id}`"
                          :value=item.id
                          disabled
                          button-variant="default"
                          size="lg"
                          :checked="item.id == activeExperiment.id"
                          ><b-button @click="setExpi(item.id)" variant="primary">Select experiment</b-button></b-form-radio
                        ></b-form-radio-group
                      >
                    </b-card>
                  </b-card-group>
                </b-card-group>
              </b-col>
              <b-col sm="6">
                <ExperimentViewer v-bind:experiment="activeExperiment"/>
              </b-col>
            </b-row>
          </b-tab>
          <b-tab title="Assignments">
            <br />
            <div style="width: 100%; overflow: hidden;">
              <div style="width: 48%; float: left;">
                <h3>Singular Observation</h3>
                <SingleAssignments />
              </div>
              <!-- <Single_Assignments />-->
              <div style="width: 48%; float: right;">
                <h3>Repeating Observations</h3>
                <RepeatAssignments />
              </div>
              <!-- <Repeat_Assignments />-->
            </div>
            <Assignments />
          </b-tab>
          <b-tab title="Data">
            <b-card-text>Tab contents 3</b-card-text>
          </b-tab>
          <b-tab title="Images" :disabled="false">
            <div>
              <ImageViewer
              />
            </div>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
import SingleAssignments from "../components/SingleAssignments.vue";
import RepeatAssignments from "../components/RepeatAssignments";
// import Experiments from "../components/Experiments";
import NavBar from "../components/NavBar";
import ImageViewer from "../components/ImageViewer";
import api from "../api/index.js";
import ExperimentViewer from "../components/ExperimentViewer";
export default {
  name: "HomePage",
  components: {
    SingleAssignments,
    RepeatAssignments,
    NavBar,
    ImageViewer,
    ExperimentViewer
  },
  data() {
    return {
      experiments: [],
      activeExperiment: { name: "You have no experiments" }
    };
  },
  beforeMount() {
    this.experiments = api.getExperiments(
      this.$store.state.role,
      this.$store.state.currentUser
    );
    if(this.experiments.length > 0) {
      this.setExpi(this.experiments[0].id)
    }
  },
    methods: {
      setExpi(id) {
          this.activeExperiment = api.getExperiment(id)
          this.$store.state.currentExperiment = this.activeExperiment
      },
      getVariant(id, type){
        if(id==this.activeExperiment.id){
          return "success"
        }
        else{
          if(type=="header") {
            return "light"
          }
          else{
            return "secondary"
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
