<template>
  <div>
    <b-table :fields="headers" :items="assignments">
      <template v-slot:cell(frequency)="data">
        {{data.item.frequency}} days
      </template>
      <template v-slot:cell(action)="data">
        <!-- `data.value` is the value after formatted by the Formatter -->
        <router-link :to="`/view_assignment/${data.item.id}`" tag="button">{{setButton(data.item.status)}}</router-link>
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
          id: 31728637862,
          title: "Daily Check-in",
          frequency: "1",
          status: "incomplete"
        },
        {
          id: 31728637863,
          title: "Height Measurement",
          frequency: "2",
          status: "incomplete"
        },
        {
          id: 31728637864,
          title: "Color Observation",
          frequency: "7",
          status: "complete"
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
