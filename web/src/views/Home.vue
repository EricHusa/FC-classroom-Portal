<template>
  <div>
    <div>
      <b-card no-body>
        <b-tabs card justified>
          <b-tab title="Experiment" active>
            <b-card-text>Tab contents 1</b-card-text>
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
          <b-tab title="Images">
            <div>
              <b-card-text>Image things will go here</b-card-text>
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
export default {
  name: "Single_Assignments",
  components: { SingleAssignments, RepeatAssignments }
};
</script>

<style>
form {
  margin-bottom: 5px;
  margin-top: 5px;
}
</style>
