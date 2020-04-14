<template>
  <div> {{ device }}
    <b-table
      :fields="headers"
      :items="students"
      :striped="true"
      :bordered="true"
    >
      <template v-slot:cell(action)="props">
        <!-- `data.value` is the value after formatted by the Formatter -->
        <router-link
          :to="`/device/${device}/account/${props.item.username}`"
          tag="button"
          >Update</router-link
        >
      </template>
    </b-table>
  </div>
</template>

<script>
export default {
  name: "StudentList",
  props: {
    device: String,
    students: Array,
    headers: Array
  }
};
</script>

<style scoped>
/*/school/{{ school }}/account/{{ students.username }}*/
</style>
