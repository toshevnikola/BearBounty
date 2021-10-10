<template>
  <div class="home">
    <DashboardHeader
      @setClicked="setClicked"
      @changeSelectedAccount="changeSelectedAccount"
    ></DashboardHeader>
    <DashboardBot
      v-bind:selectedAccount="selectedAccount"
      v-if="selectedAccountLoaded == true && headerClickedSubMenu === 'Bots'"
    />
    <DashboardDeal v-else-if="headerClickedSubMenu === 'Deals'" />
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";
import DashboardHeader from "../components/DashboardHeader.vue";
import DashboardBot from "../components/DashboardBot.vue";
import DashboardDeal from "../components/DashboardDeal.vue";
import { UserExchange } from "@/interfaces";
@Component({ components: { DashboardHeader, DashboardBot, DashboardDeal } })
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
