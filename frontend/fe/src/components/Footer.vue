<template>
  <div>test</div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component
export default class Footer extends Vue {}
</script>

<style scoped>
div {
  position: fixed;
  bottom: 0;
  height: 100px;
  background-color: #113c4a;
  width: 100%;
  margin: 0;
  /* other styles omitted for brevity */
}
</style>