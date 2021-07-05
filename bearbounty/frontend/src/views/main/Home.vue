<template>
  <v-container class="my-5" v-if="ready">
    <v-layout>
      Current Account:
      <span class="font-weight-bold">{{ currentAccount.name }}</span>
    </v-layout>
    <v-layout>
      <v-btn-toggle mandatory tile v-model="toggle_one">
        <v-flex ma-2 v-for="account in accounts" :key="account.id">
          <v-btn @click="setCurrentAccount(account)" class="accButtons">{{
            account.name
          }}</v-btn>
        </v-flex>
      </v-btn-toggle>
    </v-layout>

    <v-layout row wrap md6 lg6>
      <v-flex md3 v-for="bot in bots" :key="bot.id">
        <v-card
          class="mx-auto ma-4"
          max-width="400"
          v-bind:class="color(bot.is_running)"
        >
          <v-card-title class="font-weight-400 large-font ">{{
            bot.name
          }}</v-card-title>
          <v-card-text
            class="ma-0 pt-0 small-font"
            v-bind:class="profitColor(bot.profit_24h)"
          >
            Profit(24h): {{ bot.profit_24h }}
          </v-card-text>
          <v-card-text
            class="ma-0 pt-0 small-font"
            v-bind:class="profitColor(bot.profit_all_time)"
          >
            Profit(all time): {{ bot.profit_all_time }}
          </v-card-text>
          <v-card-actions to p>
            <v-btn
              medium
              icon
              outlined
              color="white"
              class="ma-2 pa-0"
              :to="{ name: 'main-bots-details', params: { id: bot.id } }"
            >
              <v-icon>list</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>

    <v-btn small class="ma-1 pa-0" :to="{ name: 'main-bots-create' }"
      >CREATE</v-btn
    >
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import {
  dispatchGetBots,
  dispatchGetAccounts,
  dispatchSetCurrentAccount,
} from '@/store/main/actions';
import {
  readAccounts,
  readBots,
  readCurrentAccount,
} from '@/store/main/getters';
import { IAccount, IBot } from '@/interfaces';
@Component
export default class Home extends Vue {
  public bots: IBot[] = [];
  public accounts: IAccount[] = [];
  public currentAccount?: IAccount;
  public ready = false;
  toggle_one = 0;
  private getBots() {
    return readBots(this.$store);
  }
  private getAccounts() {
    return readAccounts(this.$store);
  }
  private getCurrentAccount() {
    return readCurrentAccount(this.$store);
  }

  private async mounted() {
    await dispatchGetAccounts(this.$store);
    await dispatchGetBots(this.$store);
    this.accounts = this.getAccounts();
    this.bots = this.getBots();
    this.currentAccount = this.accounts[0];
    this.ready = true;
  }
  async setCurrentAccount(acc) {
    console.log(acc.name);
    this.currentAccount = acc;
    await dispatchSetCurrentAccount(this.$store, this.currentAccount!);
  }
  private color(isRunning) {
    return isRunning ? 'activeBot' : 'inactiveBot';
  }
  private profitColor(profit) {
    if (profit > 0) {
      return 'positiveProfit';
    } else if (profit < 0) {
      return 'negativeProfit';
    }
  }
}
</script>

<style>
.small-font {
  font-size: 14px;
}

.large-font {
  font-size: 26px;
}
.activeBot {
  border-left: 5px solid green !important;
}
.inactiveBot {
  border-left: 5px solid rgb(185, 16, 16) !important;
}
.negativeProfit {
  color: rgb(185, 16, 16);
}
.positiveProfit {
  color: green;
}
</style>
