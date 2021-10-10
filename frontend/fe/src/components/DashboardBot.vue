<template>
  <div></div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { Bot, UserExchange } from "../interfaces";
import { api } from "../api";
@Component
export default class DashboardBot extends Vue {
  public bots: Array<Bot> = [];
  @Prop(Object) readonly selectedAccount!: UserExchange;
  public async mounted() {
    const token = localStorage.authToken;
    console.log(this.selectedAccount.id);
    await api
      .getBotsByUserExchange(token, this.selectedAccount.id)
      .then((res: any) => {
        this.bots = res.data;
      });
    console.log(this.bots[0]);
  }
}
</script>

<style scoped>
</style>