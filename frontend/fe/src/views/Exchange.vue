<template>
  <div>
    <Header @changeSelectedAccount="changeSelectedAccount" />
    <ExchangesView
      selectedAccountLoaded
      v-bind:selectedAccount="selectedAccount"
      v-if="selectedAccountLoaded == true"
    />
  </div>
</template>

<script lang="ts">
import { UserExchange } from "@/interfaces";
import { Component, Vue } from "vue-property-decorator";
import Header from "../components/Header.vue";
import ExchangesView from "../components/ExchnagesView.vue";
@Component({ components: { Header, ExchangesView } })
export default class Exchange extends Vue {
  public selectedAccount!: UserExchange;
  public selectedAccountLoaded: boolean = false;
  public isAddExchangeShown: boolean = false;
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