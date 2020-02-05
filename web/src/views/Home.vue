<template>
  <div>
    <!--  <div>-->
    <!--    <b-dropdown split text="System" class="m-2">-->
    <!--      <b-dropdown-item href="#">SLUdev1</b-dropdown-item>-->
    <!--      <b-dropdown-item href="#">SLUdev2</b-dropdown-item>-->
    <!--    </b-dropdown>-->
    <!--      <b-dropdown split text="Class" class="m-2">-->
    <!--      <b-dropdown-item href="#">1st hour</b-dropdown-item>-->
    <!--      <b-dropdown-item href="#">3nd hour</b-dropdown-item>-->
    <!--      <b-dropdown-item href="#">5th hour</b-dropdown-item>-->
    <!--    </b-dropdown>-->
    <!--      <b-dropdown split text="Experiment" class="m-2">-->
    <!--      <b-dropdown-item href="#">Basil - normal</b-dropdown-item>-->
    <!--      <b-dropdown-item href="#">Basil - gravel</b-dropdown-item>-->
    <!--      <b-dropdown-item href="#">Basil - sand</b-dropdown-item>-->
    <!--      <b-dropdown-item href="#">Sage - normal</b-dropdown-item>-->
    <!--      <b-dropdown-item href="#">Sage - gravel</b-dropdown-item>-->
    <!--      <b-dropdown-item href="#">Sage - sand</b-dropdown-item>-->
    <!--    </b-dropdown>-->
    <!--</div>-->

    <div style="align-content: center;">
      <b-form @submit="onSubmit" inline>
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

    <div>
      <b-card no-body>
        <b-tabs card justified>
          <b-tab title="Experiment" active>
            <b-card-text>Tab contents 1</b-card-text>
          </b-tab>
          <b-tab title="Assignments">
            <b-card-text>Tab contents 2</b-card-text>
          </b-tab>
          <b-tab title="Data">
            <b-card-text>Tab contents 3</b-card-text>
          </b-tab>
          <b-tab title="Images">
            <b-card-text>Tab contents 4</b-card-text>
          </b-tab>
        </b-tabs>
      </b-card>
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
