<template>
  <button @click="pp(123)">{{ text }}</button>
</template>

<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  data(): { test: string } {
    return {
      test: "",
    };
  },
  methods: {
    pp(numb: number) {
      console.log(numb);
    },
  },
  props: {
    text: String,
  },
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Ubuntu&display=swap");
button {
  background-color: #f0943d;
  border: #f0943d;
  padding: 0;
  border-radius: 5px;
  width: 248px;
  height: 88px;
  color: #ffffff;
  font-size: 24px;
  font-weight: 500;
  font-family: "Ubuntu";
}
</style>
