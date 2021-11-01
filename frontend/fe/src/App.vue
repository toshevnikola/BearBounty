

<template>
  <v-app>
    <div id="app">
      <Menu v-if="!isLandingShown" />
      <router-view />
      <!-- <Footer /> -->
    </div>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import Footer from "./components/Footer.vue";
import Menu from "./components/Menu.vue";
@Component({
  components: { Footer, Menu },
})
export default class App extends Vue {
  [x: string]: any;
  public isLandingShown: boolean = false;
  public isSignIn: boolean = false;
  @Watch("$route", { immediate: true, deep: true })
  onUrlChange(newVal: any) {
    // Some action
    if (newVal.name === "Landing") {
      this.isLandingShown = true;
    } else {
      this.isLandingShown = false;
    }
  }
}
</script>

<style>
#app {
  background-color: #dddddd;
}
body {
  margin: 0;
}
#app {
  font-family: Ubuntu, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
}
</style>
