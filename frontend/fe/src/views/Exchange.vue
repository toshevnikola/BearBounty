<template>
  <div>
    <DashboardHeader @changeSelectedAccount="changeSelectedAccount" />
    <ExchangesView v-bind:selectedAccount="selectedAccount" />
  </div>
</template>

<script lang="ts">
import { UserExchange } from "@/interfaces";
import { Component, Vue } from "vue-property-decorator";
import DashboardHeader from "../components/DashboardHeader.vue";
import ExchangesView from "../components/ExchnagesView.vue";
@Component({ components: { DashboardHeader, ExchangesView } })
export default class Exchange extends Vue {
  public selectedAccount!: UserExchange;
  public selectedAccountLoaded: boolean = false;
  public isAddExchangeShown: boolean = false;
  public mounted() {
    console.log("MOUNTED!!!!");
  }
  public changeSelectedAccount(e: any): any {
    this.selectedAccount = e;
    this.selectedAccountLoaded = true;
    console.log(this.selectedAccount);
  }
  public toggleAddExchange(): void {
    this.isAddExchangeShown = !this.isAddExchangeShown;
  }
}
</script>

<style scoped>
</style>