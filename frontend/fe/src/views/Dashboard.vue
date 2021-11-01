<template>
  <div>
    <div>
      <DashboardHeader
        @setClicked="setClicked"
        @changeSelectedAccount="changeSelectedAccount"
      ></DashboardHeader>
      <DashboardBots
        :key="botComponentId"
        v-bind:selectedAccount="selectedAccount"
        v-if="selectedAccountLoaded == true && headerClickedSubMenu === 'Bots'"
      />
      <DashboardDeals
        :key="dealComponentId"
        v-bind:selectedAccount="selectedAccount"
        v-else-if="
          selectedAccountLoaded == true && headerClickedSubMenu === 'Deals'
        "
      />
    </div>
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
  public dealComponentId: number = 1;
  public botComponentId: number = 1;
  public headerClickedSubMenu: string = "";
  public selectedAccount!: UserExchange;
  public selectedAccountLoaded: boolean = false;
  public setClicked(e: string): void {
    this.headerClickedSubMenu = e;
  }
  public changeSelectedAccount(e: any): any {
    this.selectedAccount = e;
    this.selectedAccountLoaded = true;
    this.reRenderComponents();
  }
  public reRenderComponents() {
    this.dealComponentId += 1;
    this.botComponentId += 1;
  }
}
</script>
