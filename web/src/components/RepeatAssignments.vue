<template>
  <div>
    <b-table :fields="headers" :items="assignments">
      <template v-slot:cell(frequency)="data">
        {{data.item.frequency}} days
      </template>
      <template v-slot:cell(action)="data">
        <!-- `data.value` is the value after formatted by the Formatter -->
        <router-link to="/settings" tag="button">{{data.item.action}}</router-link>
      </template>
    </b-table>
  </div>
</template>

<script>
import api from "../api/index";
export default {
  data() {
    return {
      assignments: [
        {
          title: "Daily Check-in",
          frequency: "1",
          status: "incomplete",
          action: "submit"
        },
        {
          title: "Height Measurement",
          frequency: "2",
          status: "incomplete",
          action: "submit"
        },
        {
          title: "Color Observation",
          frequency: "7",
          status: "complete",
          action: "view"
        }
      ],
      headers: [
        { key: "title", label: "Title" },
        { key: "frequency", label: "Frequency" },
        { key: "status", label: "Status" },
        { key: "action", label: "Action" }
      ]
    }
  },
  methods: {
    view: function(assignment) {
      this.$router.push({
        name: "viewAssignment",
        params: { id: assignment.id }
      });
    }
  },
  mounted() {
    api
      .getAssignments("repeat")
      .then(response => {
        this.assignments = response;
      })
      .catch(() => {
        this.assignments = [{}];
      });
  }
};
</script>
