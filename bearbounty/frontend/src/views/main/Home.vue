<template>
  <v-container class="my-5">
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
import { dispatchGetBots } from '@/store/main/actions';
import { readBots } from '@/store/main/getters';
import { IBot } from '@/interfaces';

@Component
export default class Home extends Vue {
  public bots: IBot[] = [];

  private getBots() {
    return readBots(this.$store);
  }

  private async mounted() {
    await dispatchGetBots(this.$store);
    this.bots = this.getBots();
  }
  private color(isRunning) {
    return isRunning ? 'activeBot' : 'inactiveBot';
  }
  private profitColor(profit) {
    console.log(profit);
    if (profit >= 0) {
      console.log('positive');
      return 'positiveProfit';
    }
    return 'negativeProfit';
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
