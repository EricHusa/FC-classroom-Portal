<template>
  <b-container fluid>
    <br />
    <b-row class="my-1" v-for="item in items" :key="item">
      <b-col sm="3">
        <label :for="`type-${item.name}`"
          ><code>{{ item.name }}</code
          >:</label
        >
      </b-col>
      <b-col sm="9">
        <b-form-input
          :id="`type-${item.type}`"
          :type="item.type"
          :value="item.val"
          :disabled="checkRole()"
        ></b-form-input>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data() {
    return {
      items: [
        { name: "Experiment Name", type: "text", val: "Layer of Sand" },
        { name: "Plant", type: "text", val: "Basil" },
        { name: "Days Active", type: "number", val: 12 },
        { name: "Start Date", type: "date" },
        {
          name: "Description",
          type: "text",
          val: "What happens when we give our plant soil a layer of sand?"
        }
      ],
      names: [
        "Experiment Name",
        "Plant",
        "Days Active",
        "Start Date",
        "Description"
      ]
    };
  },
  methods: {
    checkRole() {
      return this.$store.state.role == "student";
    }
  }
};
</script>
