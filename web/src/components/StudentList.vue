<template>
  <div>
    <b-table
      :fields="headers"
      :items="students"
      :striped="true"
      :bordered="true"
    >
      <template v-slot:cell(action)="data">
        <b-button :hidden="false" :to="`/student/${data.item.id}`">Update</b-button>
      </template>
    </b-table>
  </div>
</template>

<script>
export default {
  props: {
    students: Array,
    headers: Array,
    classView: Boolean
  },
  data() {
    return {
    };
  },
  methods: {
  }
};
</script>

<style scoped></style>
