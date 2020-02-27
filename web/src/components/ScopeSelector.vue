<template>
  <div>
    <div style="align-content: center;">
      <b-form @submit="onSubmit" inline align-center>
        <label class="sr-only" for="inline-form-input-system">System</label>
        <b-form-select
          class="mb-2 mr-sm-2 mb-sm-0"
          :value="null"
          v-model="form.system"
          :options="systems"
          id="inline-form-input-system"
        >
          <template v-slot:first>
            <option :value="null" disabled>System</option>
          </template>
        </b-form-select>

        <label class="sr-only" for="inline-form-input-class">Class</label>
        <b-form-select
          class="mb-2 mr-sm-2 mb-sm-0"
          :value="null"
          v-model="form.class"
          :options="classes"
          id="inline-form-input-class"
        >
          <template v-slot:first>
            <option :value="null" disabled>Class</option>
          </template>
        </b-form-select>

        <label class="sr-only" for="inline-form-input-experiment"
          >Experiment</label
        >
        <b-form-select
          class="mb-2 mr-sm-2 mb-sm-0"
          :value="null"
          v-model="form.experiment"
          :options="experiments"
          id="inline-form-input-experiment"
        >
          <template v-slot:first>
            <option :value="null" disabled>Experiment</option>
          </template>
        </b-form-select>

        <b-button type="submit" variant="primary">Set</b-button>
      </b-form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        system: null,
        class: null,
        experiment: null
      },
      systems: ["SLUdev1", "SLUdev2"],
      classes: ["1st hour", "3rd hour", "5th hour"],
      experiments: [
        "Basil - normal",
        "Basil - gravel",
        "Basil - sand",
        "Sage - normal",
        "Sage - gravel",
        "Sage - sand"
      ]
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      alert(JSON.stringify(this.form));
    }
  }
};
</script>

<style>
form {
  margin-bottom: 5px;
  margin-top: 5px;
}
</style>
