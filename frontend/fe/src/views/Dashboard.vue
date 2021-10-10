<template>
  <div class="home">
    <DashboardHeader
      @setClicked="setClicked"
      @changeSelectedAccount="changeSelectedAccount"
    ></DashboardHeader>
    <DashboardBots
      v-bind:selectedAccount="selectedAccount"
      v-if="selectedAccountLoaded == true && headerClickedSubMenu === 'Bots'"
    />
    <DashboardDeals v-else-if="headerClickedSubMenu === 'Deals'" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import DashboardHeader from "../components/DashboardHeader.vue";
import DashboardBots from "../components/DashboardBots.vue";
import DashboardDeals from "../components/DashboardDeals.vue";
import { UserExchange } from "@/interfaces";
@Component({ components: { DashboardHeader, DashboardBots, DashboardDeals } })
export default class Dashboard extends Vue {
  public headerClickedSubMenu: string = "";
  public selectedAccount!: UserExchange;
  public selectedAccountLoaded: boolean = false;
  public setClicked(e: string): void {
    this.headerClickedSubMenu = e;
  }
  public changeSelectedAccount(e: any): any {
    this.selectedAccount = e;
    this.selectedAccountLoaded = true;
  }
}
</script>
