<template>
  <div id="headerContainer">
    <div id="leftHeader">
      <h1>{{ pageName }}</h1>
      <div v-if="shouldShowButtons()">
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
      <h3 id="accountName">
        {{ selectedAccount.exchange.name }}
      </h3>
      <h3 id="accountBalance">
        Balance ${{ totalAccountBalance() }}
        <v-btn
          :loading="isRefreshLoading"
          @click="refreshAssets()"
          color="primary"
          icon
        >
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </h3>
    </div>
    <div
      style="margin-top: 30px"
      v-else-if="accountsFetched && accounts.length == 0"
    >
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
import { setSelectedAccountId } from "../utils";
@Component
export default class DashboardHeader extends Vue {
  public subMenus: Array<any> = [
    { btn: "Bots", clicked: true },
    { btn: "Deals", clicked: false },
  ];
  public accounts: Array<UserExchange> = [];
  public isRefreshLoading: boolean = false;
  public selectedAccount: UserExchange | null = null;
  public accountsFetched: boolean = false;
  public pageName: string | undefined | null = "";
  public beforeMount(): any {
    this.setClicked(this.subMenus[0]);
    this.pageName = this.$route.name;
  }
  public async mounted(): Promise<void> {
    const token = localStorage.authToken;
    await api.getUserExchanges(token).then((res: any) => {
      this.accounts = res.data;
      let selectedAccount = localStorage.selectedAccountId;
      if (selectedAccount) {
        this.changeAccount(
          this.accounts.find((x) => x.id.toString() === selectedAccount)
        );
      } else if (this.accounts.length > 0) {
        this.changeAccount(this.accounts[0]);
      }
      this.accountsFetched = true;
    });
  }
  public shouldShowButtons(): boolean {
    return this.$route.name === "Dashboard" ? true : false;
  }
  public totalAccountBalance(): string {
    let total = 0;
    this.selectedAccount?.assets.forEach((element) => {
      console.log(element);
      if (element.asset === "USDT") {
        total += parseFloat(element.free) + parseFloat(element.locked);
      } else {
        total +=
          (parseFloat(element.free) + parseFloat(element.locked)) *
          parseFloat(element.price);
      }
    });
    return total.toFixed(2);
  }
  public async refreshAssets(): Promise<void> {
    this.isRefreshLoading = true;
    if (this.selectedAccount) {
      api
        .refreshAssets(localStorage.authToken, this.selectedAccount?.id)
        .then((res) => {
          this.isRefreshLoading = false;
          this.changeAccount(res.data);
        })
        .catch((e) => {
          this.isRefreshLoading = false;
        });
    }
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
    if (this.selectedAccount)
      setSelectedAccountId(this.selectedAccount?.id.toString());
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
  width: 65%;
  float: left;
}
#rightHeader {
  width: 35%;
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