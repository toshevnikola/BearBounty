

<template>
  <v-app>
    <div id="app">
      <!-- <Landing></Landing> -->
      <!-- <div id="nav"> -->
      <!-- <router-link :to="{ name: 'Algorithms' }"></router-link> -->
      <!-- <router-link :to="{ name: 'Plans' }"></router-link> -->
      <!-- <router-link :to="{ name: 'Charts' }"></router-link> -->
      <!-- <router-link :to="{ name: 'Landing' }">Landing</router-link> |
        <router-link :to="{ name: 'Dashboard' }">Dashboard</router-link> |
        <router-link :to="{ name: 'About' }">About</router-link> -->
      <!-- </div> -->
      <Menu />
      <router-view />
      <Footer />
    </div>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Footer from "./components/Footer.vue";
import Menu from "./components/Menu.vue";
@Component({
  components: { Footer, Menu },
})
export default class App extends Vue {}
</script>

<style>
#app {
  background-color: #dddddd;
}
body {
  margin: 0;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
}
</style>
