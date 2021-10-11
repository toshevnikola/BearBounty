<template>
  <div id="headerContainer">
    <div id="leftHeader">
      <h1>Exchanges</h1>
    </div>
    <div id="rightHeader" v-if="accountsFetched">
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
import { UserExchange } from "@/interfaces";
import { Component, Emit, Vue, Watch } from "vue-property-decorator";
import { api } from "../api";
@Component
export default class Header extends Vue {
  public accounts: Array<UserExchange> = [];
  public selectedAccount: UserExchange | null = null;
  public accountsFetched: boolean = false;

  public async mounted(): Promise<void> {
    const token = localStorage.authToken;
    await api.getUserExchanges(token).then((res: any) => {
      this.accounts = res.data;
      this.changeAccount(this.accounts[0]);
      this.accountsFetched = true;
    });
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