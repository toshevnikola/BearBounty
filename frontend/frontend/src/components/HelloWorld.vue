<template>
  <div>
    <button @click="getRandom()"></button>
    <p>{{ beautifyRandomList }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
export default defineComponent({
  data(): {
    randomNumberList: Array<number>;
    testData: string;
  } {
    return {
      testData: "TestData123",
      randomNumberList: [],
    };
  },
  methods: {
    getRandom() {
      let randomNumber: number = Math.random();
      this.randomNumberList = [...this.randomNumberList, randomNumber];
    },
  },
  computed: {
    beautifyRandomList(): string {
      return this.randomNumberList.toString();
    },
  },
  props: {
    msg: String,
  },
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
* {
  color: black;
}
</style>
