<template>
  <div id="headerContainer">
    <div id="leftHeader">
      <h1>Dashboard</h1>
      <button
        v-for="subMenu in subMenus"
        :key="subMenu.btn"
        class="subMenuBtn"
        v-bind:class="{ activeSubMenuBtn: subMenu.clicked }"
        @click="setClicked(subMenu)"
      >
        {{ subMenu.btn }}
      </button>
    </div>
    <div
      id="rightHeader"
      v-if="accountsFetched && selectedAccount != null && accounts.length > 0"
    >
      <v-select
        v-model="selectedAccount"
        @input="changeAccount"
        id="selection"
        return-object
        style="width: 45%; display: inline-block; float: left"
        :items="accounts"
        item-text="exchange.name"
        filled
        label="Account"
        persistent-hint
      ></v-select>
      <h3 id="accountName">{{ selectedAccount.exchange.name }}</h3>
      <h3 id="accountBalance">Balance {{ "$" }}</h3>
    </div>
    <div style="margin-top: 30px" v-else-if="accounts.length == 0">
      Connect to exchange before continuing
    </div>
    <div v-else>
      <v-progress-circular
        :size="70"
        :width="8"
        color="secondary"
        indeterminate
      ></v-progress-circular>
    </div>
  </div>
</template>

<script lang="ts">
import { UserExchange, Bot } from "@/interfaces";
import { Component, Emit, Vue, Watch } from "vue-property-decorator";
import { api } from "../api";
@Component
export default class DashboardHeader extends Vue {
  public subMenus: Array<any> = [
    { btn: "Bots", clicked: true },
    { btn: "Deals", clicked: false },
    { btn: "Strategies", clicked: false },
  ];
  public accounts: Array<UserExchange> = [];
  public selectedAccount: UserExchange | null = null;
  public accountsFetched: boolean = false;
  public beforeMount(): any {
    this.setClicked(this.subMenus[0]);
  }
  public async mounted(): Promise<void> {
    const token = localStorage.authToken;
    await api.getUserExchanges(token).then((res: any) => {
      this.accounts = res.data;
      if (this.accounts.length > 0) {
        this.changeAccount(this.accounts[0]);
      }
      this.accountsFetched = true;
    });
  }
  @Emit("setClicked")
  public setClicked(subMenu: any): string {
    this.subMenus.forEach((x) => {
      if (x.btn === subMenu.btn) {
        x.clicked = true;
      } else {
        x.clicked = false;
      }
    });
    return subMenu.btn;
  }
  @Emit("changeSelectedAccount")
  public changeAccount(event: any): void {
    this.selectedAccount = event;
  }
}
</script>

<style scoped>
#headerContainer {
  width: 100%;
  height: 100px;
  float: left;
  padding-left: 5%;
  border-bottom: 5px solid #113c4a;
}
.subMenuBtn {
  font-weight: normal;
  width: 178px;
  height: 44px;
  border-radius: 5px;
  font-size: 24px;
  color: #113c4a;
  background-color: #dddddd;
  margin-right: 30px;
}
.subMenuBtn:hover {
  background-color: #cccccc;
}
.activeSubMenuBtn {
  color: #dddddd;
  background-color: #113c4a !important;
}
#leftHeader {
  width: 70%;
  float: left;
}
#rightHeader {
  width: 30%;
  float: left;
  margin-top: 20px;
}
h3 {
  padding-left: 2%;
  display: inline;
  width: 45%;
  float: left;
}
#accountName {
  color: #3f7b70;
}
#accountBalance {
  color: #1c5d73;
}
</style>