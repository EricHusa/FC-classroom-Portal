<template>
  <div id="app">
    <div id="nav">
      <!--    <div id="nav">-->
      <!--      <router-link to="/student">Student</router-link> |-->
      <!--      <router-link to="/teacher">Teacher</router-link>-->
      <!--      <h2>Food Computer Portal<b-icon icon="person-fill"></b-icon></h2>-->
      <!--    </div>-->
      <b-navbar toggleable="lg" class="navbar navbar-expand-sm">
        <!--          <a href="#"><h2>Food Computer Portal</h2></a>-->
        <b-navbar-brand
          class="nav navbar-nav flex-fill justify-content-center"
          href="#"
          style="margin-right: 0px;margin-left: 63px;"
          ><h3>Food Computer Portal</h3></b-navbar-brand
        >
        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto settings-dropdown">
          <b-nav-item-dropdown right>
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              <b-icon icon="person-fill" style="color: white;"></b-icon>
            </template>
            <b-dropdown-item>
              <router-link to="/settings">Settings</router-link>
            </b-dropdown-item>
            <b-dropdown-item>
              <router-link to="/school">Settings</router-link>
            </b-dropdown-item>
            <b-dropdown-item
              ><router-link to="/login">Sign out</router-link></b-dropdown-item
            >
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-navbar>
    </div>
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  /*padding-top: 10px;*/
  /*padding-bottom: 5px;*/
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-image: linear-gradient(
    to bottom left,
    #344675,
    #263148,
    #344675
  ) !important;
  text-align: center;
}

#nav a {
  font-weight: bold;
  color: white;
  text-align: center;
}

#nav li a {
  color: #007bff;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
