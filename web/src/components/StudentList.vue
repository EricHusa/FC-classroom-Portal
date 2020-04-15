<template>
  <div>
      <b-form inline>
        <label class="sr-only" for="inline-form-class-name">Name</label>
        <b-input v-model="className"
         trim
          id="inline-form-class-name"
          class="mb-2 mr-sm-2 mb-sm-0"
          :placeholder="getClassName(currClass)"
        ></b-input>
        <b-button variant="warning" @click="updateClassName(currClass, className)" >Rename class</b-button>
      </b-form>
      <!--      <b-overlay :show="true" rounded="sm" variant="danger">-->
        <b-table
          :fields="headers"
          :items="students"
          :striped="true"
          :bordered="true"
        >
          <template v-slot:cell(action)="props">
            <router-link
              :to="`/device/${device}/account/${props.item.username}`"
              tag="button"
              >Update</router-link
            >
          </template>
        </b-table>
    <!--      </b-overlay>-->
<!--      <div >{{ currClass }}</div>-->
      <div><div><b-button style="float: left;" v-b-toggle.add-student class="m-1" variant="primary" :disabled="this.$store.state.activeClass == null">Add students</b-button>
      <b-button style="float: right;" variant="danger" @click="deleteClass(currClass)" :disabled="this.$store.state.activeClass == null">Delete class</b-button></div>
          <b-collapse id="add-student">
          <b-form @submit="onSubmit">

            <b-input size="sm" style="margin-bottom: 1%;"
              id="form-first-name"
              v-model="form.fname"
              trim
              placeholder="First Name"
            ></b-input>

              <b-input size="sm" style="margin-bottom: 1%;"
              id="form-last-name"
              v-model="form.lname"
              trim
              placeholder="Last Name"
            ></b-input>

              <b-input size="sm" style="margin-bottom: 1%;"
              id="form-username"
              v-model="form.username"
              required
              trim
              placeholder="Username"
            ></b-input>

              <b-input size="sm" style="margin-bottom: 1%;"
              id="form-password"
              v-model="form.password"
              required
              trim
              placeholder="Password"
            ></b-input>

            <b-button type="submit" variant="success" :disabled="this.$store.state.activeClass == null">Add</b-button>
          </b-form>
      </b-collapse></div>
  </div>
</template>

<script>
import api from "../api/index.js";
export default {
  name: "StudentList",
  props: {
    device: String,
    currClass: Number,
    students: Array,
    headers: Array
  },
  data() {
      return {
          form: {
              fname: null,
              lname: null,
              username: '',
              password: ''
          },
          className: ''
      }
  },
    methods: {
      validate() {
        return this.form.fname.indexOf(" ") === -1 &&
                this.form.lname.indexOf(" ") === -1 &&
                this.form.username.indexOf(" ") === -1 &&
                this.form.password.indexOf(" ") === -1
      },
       getClassName(id){
          return api.getClass(id).name
       },
       updateClassName(id, name){
          if(name.length > 0){
              api.updateClass(id, name)
          }
          this.className = ''
       },
        onSubmit(evt) {
            evt.preventDefault()
            if (!this.validate()) {
                alert('spaces are not allowed in input')
            } else {
                api.addStudent(JSON.parse(JSON.stringify(this.form)), this.$store.state.activeClass)
                this.students.push(JSON.parse(JSON.stringify(this.form)))
                this.form.fname = null
                this.form.lname = null
                this.form.username = ''
                this.form.password = ''
                this.show = false
                this.$nextTick(() => {
                    this.show = true
                })
            }
        },
        deleteClass(id) {
           if(confirm("Are you sure you want to delete this class? Note that this does not delete accounts in the class")){
               api.deleteClass(id)
               this.$store.state.activeClass = null
           }
        }
    }
};
</script>

<style scoped></style>
