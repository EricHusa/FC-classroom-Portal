<template>
  <div>
    <h3><u>Phases</u></h3>
    <b-table :fields="climateHeaders" :items="phases">
      <template v-slot:cell(action)="row">
        <b-button size="md" @click="row.toggleDetails" class="mr-2"
          >Expand</b-button
        >
      </template>
      <template v-slot:row-details="data">
        <b-card>
          <b-row>
            <h3>Air Temperature</h3>
            <b />
            <b-table
              :fields="airTempHeaders"
              :items="getStepData(data.item.name, 'air_temperature')"
              bordered
            ></b-table
            ><br />
          </b-row>
          <b-row>
            <h3>Light Intensity</h3>
            <b />
            <b-table
              :fields="lightIntensityHeaders"
              :items="getStepData(data.item.name, 'light_intensity')"
              bordered
            ></b-table
            ><br />
          </b-row>
          <b-row>
            <h3>Air Flush</h3>
            <b />
            <b-table
              :fields="airFlushHeaders"
              :items="getStepData(data.item.name, 'air_flush')"
              bordered
            ></b-table
            ><br />
          </b-row>
        </b-card>
      </template>
    </b-table>
  </div>
</template>

<script>
import TableHeaders from "../constants/TableHeaders.ts";
import SampleClimate from "../constants/SampleClimate.ts";
export default {
  name: "DeviceViewer",
  data() {
    return {
      climateHeaders: TableHeaders.climate,
      airTempHeaders: TableHeaders.air_temp,
      lightIntensityHeaders: TableHeaders.light_intensity,
      airFlushHeaders: TableHeaders.air_flush,
      phases: SampleClimate.climate_file.phases
    };
  },
  methods: {
    getStepData(phaseName, stepName) {
      let index = this.phases
        .map(function(e) {
          return e.name;
        })
        .indexOf(phaseName);
      let phase = this.phases[index];
      return phase.step[stepName];
    }
  }
};
</script>

<style scoped></style>
