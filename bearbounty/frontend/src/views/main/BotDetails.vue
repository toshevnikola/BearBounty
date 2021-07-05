<template>
  <v-container v-if="ready">
    <v-layout>
      <v-flex md6>
        <v-layout>
          <v-flex md12>
            <v-card>
              <v-card-title>Name: {{ botName }}</v-card-title>
              <v-card-text>Description: {{ botDescription }}</v-card-text>
              <v-card-text>Strategy: {{ selectedStrategy.name }}</v-card-text>
              <v-card-text>Profit24h: {{ botProfit24h }}</v-card-text>
              <v-card-text>Profit All Time: {{ botProfitAllTime }}</v-card-text>
              <v-card-text>Status: {{ isEnabled() }}</v-card-text>
              <v-card-actions>
                <!-- activate/deactivate bot button -->
                <v-btn
                  class="mx-2"
                  fab
                  small
                  color="white"
                  @click="changeStatus(botIsRunning)"
                >
                  <v-icon v-if="botIsRunning" color="red">
                    stop
                  </v-icon>
                  <v-icon v-else color="green">
                    play_arrow
                  </v-icon>
                </v-btn>
                <!-- edit bot button -->
                <v-btn
                  color="primary"
                  class="mr-2 ml-0"
                  :to="{ name: 'main-bots-edit', params: { id: bot.id } }"
                >
                  Edit
                </v-btn>
                <!-- delete bot button -->
                <v-btn
                  color="silver"
                  class="mr-4 ml-0"
                  @click="deleteBot(parseInt($route.params.id))"
                >
                  Delete
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>
<script lang="ts">
import { IBot, IBotUpdate, IStrategy } from '@/interfaces';

import { Component, Vue } from 'vue-property-decorator';
import {
  dispatchGetStrategies,
  dispatchGetBots,
  dispatchUpdateBot,
  dispatchDeleteBot,
} from '@/store/main/actions';
import { readStrategies, readBots } from '@/store/main/getters';

@Component
export default class BotDetails extends Vue {
  public strategies: IStrategy[] = [];
  public bot?: IBot = undefined;
  public botName: string = '';
  public botDescription: string = '';
  public botProfit24h: number = -1;
  public botProfitAllTime: number = -1;
  public botIsRunning: boolean = false;
  public bots?: IBot[] = [];
  public selectedStrategy?: IStrategy = undefined;
  public valid = false;
  public ready = false;
  nameRules = [
    (v) => !!v || 'Name is required',
    (v) =>
      (v.length >= 5 && v.length <= 15) ||
      'Name must be between 5 and 15 characters',
  ];
  private isEnabled() {
    return this.botIsRunning ? 'Enabled' : 'Disabled';
  }
  private getStrategies() {
    return readStrategies(this.$store);
  }
  private getBots() {
    return readBots(this.$store);
  }
  private async beforeMount() {
    await dispatchGetStrategies(this.$store);
    this.strategies = this.getStrategies();
    this.bots = this.getBots();
    if (this.bots.length === 0) {
      await dispatchGetBots(this.$store).then();
    }
    this.bots = this.getBots();
    this.bot = this.bots.find((element) => {
      return element.id === parseInt(this.$route.params.id);
    });
    this.selectedStrategy = this.strategies.find((el) => {
      return el.id === this.bot!.strategy_id;
    });
    this.botName = this.bot!.name;
    this.botDescription = this.bot!.description;
    this.botIsRunning = this.bot!.is_running;
    this.botProfit24h = this.bot!.profit_24h;
    this.botProfitAllTime = this.bot!.profit_all_time;
    this.ready = true;
    console.log('Ready is true');
    console.log(this.botIsRunning);
  }

  async deleteBot(id: number) {
    // TODO: check out @Watch
    await dispatchDeleteBot(this.$store, { id: id });
    this.$router.push('/main/home');
  }
  async changeStatus(status: boolean) {
    console.log(status);
    const updatedBot: IBotUpdate = this.bot!;
    updatedBot.is_running = !status;
    await dispatchUpdateBot(this.$store, updatedBot);
    this.botIsRunning = !status;
  }
}
</script>
