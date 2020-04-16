<template>
  <div>
    <!--      <b-overlay :show="true" rounded="sm" variant="danger">-->
    <b-table
      :fields="headers"
      :items="students"
      :striped="true"
      :bordered="true"
    >
      <template v-slot:cell(action)="props">
        <router-link :to="`/student/${props.item.id}`" tag="button"
          >Update</router-link
        >
      </template>
    </b-table>
  </div>
</template>

<script>
// import api from "../api/index.js";
export default {
  props: {
    currClass: Number,
    students: Array,
    headers: Array
  },
  data() {
    return {
      form: {
        fname: null,
        lname: null,
        username: "",
        password: ""
      },
      selectedStudents: [],
      className: ""
    };
  },
  methods: {}
};
</script>

<style scoped></style>
