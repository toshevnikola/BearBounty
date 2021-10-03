<template>
  <div class="home">
    <HelloWorld msg="Welcome to Your Vue.js + TypeScript App" />
    <Button text="Click me" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import HelloWorld from "../components/HelloWorld.vue"; // @ is an alias to /src
import Button from "../components/Button.vue";
export default defineComponent({
  name: "Home",
  components: {
    HelloWorld,
    Button,
  },
});
</script>
