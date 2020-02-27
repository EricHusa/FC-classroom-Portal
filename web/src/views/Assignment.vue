<template>
  <!--
  <v-container fluid>
    <v-layout align-start justify-center fill-height>
  -->
  <v-card class="card">
    <b-card-text>
      Description:
    </b-card-text>
    <v-form ref="form" lazy-validation class="form">
      <v-text-field
        v-model="input"
        :rules="inputRules"
        label="Input"
        required
      ></v-text-field>
      <v-menu
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
        <v-text-field
          slot="activator"
          v-model="date"
          label="Date"
          readonly
          :rules="dateRules"
        ></v-text-field>
        <v-date-picker v-model="date" no-title scrollable>
          <v-spacer></v-spacer>
          <v-btn flat color="primary" @click="$refs.menu.save(date)">OK</v-btn>
        </v-date-picker>
      </v-menu>
      <v-text-field
        v-model="notes"
        :rules="notesRules"
        label="Notes"
      ></v-text-field>

      <div class="buttonContainer">
        <v-btn color="error" @click="reset" class="reset">Reset Form</v-btn>
        <v-btn color="success" @click="submit" class="submit">Submit</v-btn>
      </div>
    </v-form>
  </v-card>
  <!--
    </v-layout>
  </v-container>
  -->
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
    notesRules: []
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
    }
  },
  beforeMount: function() {
    this.assignment_id = this.$route.params.id;
  }
};
</script>
