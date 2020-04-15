<template>
  <div>
<!--      <div >{{ currClass }}</div>-->
      <div><b-button v-b-toggle.collapse-1 class="m-1" variant="primary" :disabled="this.$store.state.activeClass == null">Add students</b-button>
      <b-collapse id="collapse-1">
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

            <b-button type="submit" variant="success">Add</b-button>
          </b-form>
      </b-collapse></div>
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
    {{ this.$store.state.activeClass }}
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
          }
      }
  },
    methods: {
      validate() {
        return this.form.fname.indexOf(" ") === -1 &&
                this.form.lname.indexOf(" ") === -1 &&
                this.form.username.indexOf(" ") === -1 &&
                this.form.password.indexOf(" ") === -1
      },
       isActive(){
          return this.$store.state.activeClass == null
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
        }
    }
};
</script>

<style scoped></style>
