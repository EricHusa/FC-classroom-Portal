<template>
  <div id="nav">
    <b-navbar toggleable="lg" class="navbar navbar-expand-sm">
      <b-navbar-brand
        class="nav navbar-nav flex-fill justify-content-center"
        href="#"
        style="margin-right: 0px;margin-left: 63px;"
        ><h3>Food Computer Portal</h3></b-navbar-brand
      >
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto settings-dropdown">
        <b-nav-item-dropdown right>
          <b-dropdown-item
            v-for="item in options"
            :key="item"
            :to="`${item.path}`"
          >
            {{ item.name }}
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
import NavOptions from "../constants/NavOptions.ts";
export default {
  data() {
    return { options: NavOptions[this.$store.state.role] };
  }
};
</script>

<style scoped></style>
