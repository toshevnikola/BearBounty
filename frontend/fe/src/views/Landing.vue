<template>
  <div>
    <img id="logo" src="../assets/bb.svg" alt="" />
    <div id="nav">
      <div id="leftNav">
        <router-link class="navItem" :to="{ name: 'Algorithms' }">
          Algorithms</router-link
        >
        <router-link class="navItem" :to="{ name: 'Plans' }">Plans</router-link>
        <router-link class="navItem" :to="{ name: 'Charts' }"
          >Charts</router-link
        >
      </div>
      <div id="rightNav">
        <router-link class="navItem" :to="{ name: 'Sign In' }"
          >Sign In</router-link
        >
        <router-link
          id="joinForFree"
          class="navItem"
          :to="{ name: 'Join for free' }"
          >Join for free</router-link
        >
      </div>
    </div>
    <div id="headingCtaWrapper">
      <h1>Smart trading terminal<br />and crypto trading bots</h1>
      <a href="" display="block" id="cta">Start trading</a>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class Landing extends Vue {}
</script>

<style scoped>
#logo {
  float: left;
}
.navItem {
  font-size: 24px;
  text-decoration: none;
  margin-left: 5%;
  display: inline-block;
  color: #3f7b70;
  padding: 15px;
}
.navItem:visited {
  color: #3f7b70;
}
#nav {
  float: left;
  width: 80%;
  height: 200px;
}
#leftNav {
  width: 50%;
  float: left;
  margin-top: 3%;
  font-weight: 600;
}
#rightNav {
  width: 30%;
  float: right;
  margin-top: 3%;
  font-weight: 600;
  position: relative;
}
#joinForFree {
  border: 3px solid #f0943d;
  border-radius: 4px;
}
h1 {
  color: #1c5d73;
}
#headingCtaWrapper {
  width: 40%;
  float: left;
}
#cta {
  width: 248px;
  font-size: 24px;
  display: block;
  background-color: #f0943d;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  float: left;
  text-align: center;
  padding: 35px 0;
  margin-top: 1%;
}
</style>