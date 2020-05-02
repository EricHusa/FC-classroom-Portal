<template>
  <div>
    <NavBar />
    <b-card no-body>
      <b-tabs card justified>
        <b-tab title="Student List">
          <h3 style="text-align: center">All of your students</h3>
          <StudentList v-bind:students="allStudents" v-bind:headers="headers" v-bind:classView="false"/>
          <b-container fluid>
            <b-row>
              <b-col sm="3">
                <b-button v-b-toggle.add-student class="m-1" variant="primary"
                  >Create new student</b-button
                >
              </b-col>
              <b-col sm="9">
                <b-collapse id="add-student">
                  <b-row
                    class="my-1"
                    v-for="item in headers.slice(0, 4)"
                    :key="item"
                  >
                    <b-col sm="3">
                      <label :for="`new-student-form-${item.label}`"
                        >{{ item.label }}:</label
                      >
                    </b-col>
                    <b-col sm="9">
                      <b-form-input
                        trim
                        :id="`new-student-form-${item.label}`"
                        :placeholder="`${item.label}`"
                        v-model="form[item.key]"
                      ></b-form-input>
                    </b-col>
                  </b-row>
                  <b-button
                    style="text-align: center"
                    @click="addStudent()"
                    variant="success"
                    >Create</b-button
                  >
                </b-collapse>
              </b-col>
            </b-row>
          </b-container>
        </b-tab>

        <b-tab title="Class List">
          <br />
          <b-row>
            <b-col cols="6" md="4">
              <b-button class="m-1" variant="success" @click="addClass"
                >Create a new class</b-button
              >
              <b-collapse id="edit-class-name"> </b-collapse>
              <br />
              <b-list-group v-for="item in classes" :key="item.name">
                <b-list-group-item
                  button
                  @click="setClass(item.id)"
                  :active="item.id == currClass.id"
                  variant="secondary"
                  >{{ item.name }}</b-list-group-item
                >
              </b-list-group>
              <br />
              Your class list
            </b-col>

            <b-col cols="12" md="8">
              <b-overlay :show="classDeleted">
                <div>
                  <b-container fluid>
                    <b-form inline style="float: left;">
                      <b-input
                        v-model="className"
                        trim
                        id="inline-form-class-name"
                        class="mb-2 mr-sm-2 mb-sm-0"
                        :disabled="classDeleted"
                        :placeholder="currClass.name"
                      ></b-input>
                      <b-button
                        variant="warning"
                        @click="updateClassName(currClass, className)"
                        :disabled="classDeleted"
                        >Rename class</b-button
                      >
                    </b-form>
                    <b-button
                      style="float: right;"
                      variant="danger"
                      class="mb-2 mr-sm-2 mb-sm-0"
                      @click="deleteClass(currClass.id)"
                      :disabled="classDeleted"
                      >Delete class</b-button
                    >
                  </b-container>
                  <StudentList
                    v-bind:students="currStudents"
                    v-bind:headers="headers"
                    v-bind:classView="true"
                    @studentRemoved="removeStudent"
                  />
                  <b-row>
                    <b-col sm="3">
                      <b-button
                        v-b-toggle.import-student
                        class="m-1"
                        variant="primary"
                        :disabled="classDeleted"
                        >Add existing students</b-button
                      >
                    </b-col>
                    <b-col sm="9">
                      <b-collapse id="import-student">
                        <div style="text-align: center;">
                          <b-form-group
                            style="text-align: left; display: inline-block"
                          >
                            <b-form-checkbox-group
                              v-model="selectedStudents"
                              :options="formatCheckboxes"
                              name="flavour-2a"
                              stacked
                            ></b-form-checkbox-group>
                          </b-form-group>
                        </div>
                        <b-button
                          @click="importStudents"
                          variant="success"
                          :disabled="classDeleted"
                          >Add</b-button
                        >
                      </b-collapse>
                    </b-col>
                  </b-row>
                </div>
                <template v-slot:overlay>
                  <b-icon icon="exclamation-circle" font-scale="2"></b-icon>
                  <p>Select or create a class</p>
                </template>
              </b-overlay>
            </b-col>
          </b-row>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import StudentList from "../components/StudentList.vue";
import api from "../api/index.js";
import NavBar from "../components/NavBar";
export default {
  components: { StudentList, NavBar },
  data() {
    return {
      currStudents: api.getStudents(),
      allStudents: api.getStudents(),
      headers: [
        { key: "fname", label: "First Name", sortable: true },
        { key: "lname", label: "Last Name", sortable: true },
        { key: "username", label: "Username", sortable: true },
        { key: "password", label: "Password" },
        { key: "action", label: "Action" }
      ],
      classes: [{}],
      className: "",
      classDeleted: true,
      selectedStudents: [],
      form: {
        fname: null,
        lname: null,
        username: "",
        password: ""
      },
      currClass: null
    };
  },
  computed: {
    formatCheckboxes() {
      let students = api.getStudentCheckboxes();
      let rows = students.map(item => {
        let tmp = item;
        if (this.currClass.students.includes(item.value)) {
          tmp.disabled = true;
        }
        return tmp;
      });
      return rows;
    }
  },
  methods: {
    addClass() {
      api.addClass();
      this.classes = api.getClasses();
    },
    setClass(id) {
      this.currStudents = api.getStudents(id);
      this.currClass = api.getClass(id);
      this.classDeleted = false;
    },
    // getClassName(id) {
    //   if (id === null) {
    //     return "";
    //   }
    //   let c = api.getClass(id);
    //   return c.name;
    // },
    updateClassName(thisClass, name) {
      if (name.length > 0) {
        thisClass.name = name;
        api.updateClass(thisClass);
      }
      this.className = "";
    },
    deleteClass(id) {
      if (
        confirm(
          "Are you sure you want to delete this class? Note that this does not delete accounts in the class"
        )
      ) {
        api.deleteClass(id);
        this.classDeleted = true;
      }
    },
    addStudent() {
      if (!this.validate()) {
        alert("spaces are not allowed in input");
      } else {
        try {
          api.createStudent(JSON.parse(JSON.stringify(this.form)));
        } catch (err) {
          alert(err);
        }
        this.form.fname = null;
        this.form.lname = null;
        this.form.username = "";
        this.form.password = "";
      }
    },
    getStudentCheckboxes() {
      return api.getStudentCheckboxes();
    },
    async importStudents() {
      let newStudents = [];
      for (let i in this.selectedStudents) {
        newStudents.push(this.selectedStudents[i]);
        //this.currClass
      }
      let course = await updateClass.login(role, this.forms[role]).then(function(response) {
        return response;
      });
      this.currStudents = api.getStudents(this.currClass.id);
      this.selectedStudents = [];
    },
    removeStudent(studentId){
      api.removeStudentFromClass(this.currClass.id, studentId);
      this.setClass(this.currClass.id);
    },
    validate() {
      return (
        this.form.fname.indexOf(" ") === -1 &&
        this.form.lname.indexOf(" ") === -1 &&
        this.form.username.indexOf(" ") === -1 &&
        this.form.password.indexOf(" ") === -1
      );
    }
  },
  beforeMount() {
    this.classes = api.getClasses();
    if(this.classes.length > 0) {
      this.setClass(this.classes[0].id);
      this.classDeleted = false;
    }
    else{
      this.currClass = {id: null};
    }
  }
};
</script>

<style>
.center {
  margin: auto;
  width: 60%;
  padding: 10px;
}

#overlay {
  position: fixed;
  display: none;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 2;
}
</style>
