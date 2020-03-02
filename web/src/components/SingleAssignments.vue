<template>
  <div>
    <b-table :fields="headers" :items="assignments">
      <template v-slot:cell(action)="data">
        <!-- `data.value` is the value after formatted by the Formatter -->
        <router-link :to="`/view_assignment/${data.item.id}`" tag="button">{{setButton(data.item.status)}}</router-link>
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
          id: 63174627868,
          title: "Predict How Many Days",
          end_date: "03/25/2020",
          status: "incomplete"
        },
        {
          id: 63174627867,
          title: "Smell the Flower",
          end_date: "03/05/2020",
          status: "complete"
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
    },
    setButton: function(status){
      if(status == 'incomplete')
      {
        return "submit"
      }
      else{
        return "review"
      }
    }
  }
};
</script>
