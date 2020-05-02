<template>
  <div>
    <b-table
      :fields="headers"
      :items="students"
      :striped="true"
      :bordered="true"
    >
      <template v-slot:cell(action)="data">
        <b-button :hidden="classView" :to="`/student/${data.item.id}`">Update</b-button>
<!--        <b-button :hidden="!classView" @click="removeStudent(data.item.id)">Remove</b-button>-->
<!--        <router-link :to="`/student/${props.item.id}`" tag="button"-->
<!--          >Update</router-link-->
<!--        >-->
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
    // removeStudent(studentId){
    //   this.$emit("studentRemoved", studentId);
    // }
  }
};
</script>

<style scoped></style>
