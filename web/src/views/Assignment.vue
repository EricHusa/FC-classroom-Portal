<template>
  <b-container fluid>
    <b-layout align-start justify-center fill-height>
      <b-card class="card">
        <b-card-text>
          <b>Description</b>: This is assignment {{ getID() }}
        </b-card-text>
        <b-form ref="form" lazy-validation class="form">
          <b-text-field
            v-model="input"
            :rules="inputRules"
            label="Input"
            required
          ></b-text-field>
          <b-menu
            ref="menu"
            :close-on-content-click="false"
            :nudge-right="40"
            :return-value.sync="date"
            lazy
            transition="scale-transition"
            offset-y
            full-width
            min-width="290px"
          >
            <b-text-field
              slot="activator"
              v-model="date"
              label="Date"
              readonly
              :rules="dateRules"
            ></b-text-field>
            <!--        <b-date-picker v-model="date" no-title scrollable>-->
            <!--          <b-spacer></b-spacer>-->
            <!--          <b-btn flat color="primary" @click="$refs.menu.save(date)">OK</b-btn>-->
            <!--        </b-date-picker>-->
            <b-container fluid>
              <b-row key="text">
                <b-col sm="4"> </b-col>
                <b-col sm="4">
                  <b-form-input type="text"></b-form-input>
                </b-col>
              </b-row>
            </b-container>
          </b-menu>
          <b-text-field
            v-model="notes"
            :rules="notesRules"
            label="Notes"
          ></b-text-field>
          <br />
          <div class="buttonContainer">
            <b-btn color="red" @click="reset" class="reset">Reset Form</b-btn>
            <b-btn color="green" @click="submit" class="submit">Submit</b-btn>
          </div>
          <br />
          <div>
            <button><router-link to="/home">Home</router-link></button>
          </div>
        </b-form>
      </b-card>
    </b-layout>
  </b-container>
</template>

<script>
export default {
  data: () => ({
    id: this.assignment_id,
    date: "",
    dateRules: [v => !!v || "Date is required"],
    input: "",
    inputRules: [v => !!v || "Input is required"],
    notes: "",
    notesRules: [],
    types: ["text"]
  }),
  methods: {
    validate() {
      if (this.$refs.form.validate()) {
        this.acceptable = true;
      }
    },
    reset() {
      this.$refs.form.reset();
    },
    submit() {
      alert("assignment submitted");
    },
    getID() {
      return this.assignment_id;
    }
  },
  beforeMount: function() {
    this.assignment_id = this.$route.params.id;
  }
};
</script>
