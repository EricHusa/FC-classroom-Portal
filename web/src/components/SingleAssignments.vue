<template>
  <div>
    <b-table :fields="headers" :items="assignments">
      <template v-slot:cell(action)="data">
        <!-- `data.value` is the value after formatted by the Formatter -->
        <router-link to="/settings" tag="button">{{data.item.action}}</router-link>
      </template>
    </b-table>
  </div>
</template>

<script>
import api from "../api/index.js";
export default {
  data() {
    return {
      assignments: [
        {
          title: "Predict How Many Days",
          end_date: "03/25/2020",
          status: "incomplete",
          action: "view"
        },
        {
          title: "Smell the Flower",
          end_date: "03/05/2020",
          status: "complete",
          action: "view"
        }
      ],
      headers: [
        { key: "title", label: "Title" },
        { key: "end_date", label: "Due Date" },
        { key: "status", label: "Status" },
        { key: "action", label: "Action" }
      ]
    };
  },
  beforeMount() {
    api
      .getAssignments("single")
      .then(response => {
        this.assignments = response;
      })
      .catch(() => {
        alert("yikes");
      });
  },
  methods: {
    view: function(assignment) {
      this.$router.push({
        name: "viewAssignment",
        params: { id: assignment.id }
      });
    },
    refresh: function() {
      api
        .getAssignments("single")
        .then(response => {
          this.assignments = response;
        })
        .catch(() => {
          alert("yikes");
        });
    }
  }
};
</script>
