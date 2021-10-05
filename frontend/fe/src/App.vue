

<template>
  <div id="app">
    <Landing></Landing>
    <!-- <div id="nav"> -->
    <!-- <router-link :to="{ name: 'Algorithms' }"></router-link> -->
    <!-- <router-link :to="{ name: 'Plans' }"></router-link> -->
    <!-- <router-link :to="{ name: 'Charts' }"></router-link> -->
    <!-- <router-link :to="{ name: 'Landing' }">Landing</router-link> |
        <router-link :to="{ name: 'Dashboard' }">Dashboard</router-link> |
        <router-link :to="{ name: 'About' }">About</router-link> -->
    <!-- </div> -->
    <Footer />
    <!-- <router-view /> -->
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Landing from "./views/Landing.vue";
import Footer from "./components/Footer.vue";
@Component({
  components: { Landing, Footer },
})
export default class App extends Vue {}
</script>

<style>
body {
  background-color: #dddddd;
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
