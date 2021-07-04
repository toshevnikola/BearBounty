<template>
  <v-container v-if="ready">
    <v-form ref="form" lazy-validation v-model="valid">
      <v-layout>
        <v-flex md4>
          <v-text-field
            v-model="botName"
            counter
            maxlength="15"
            label="Bot name"
            :rules="nameRules"
            v-validate="{ required: true }"
          ></v-text-field>
        </v-flex>
      </v-layout>
      <v-layout>
        <v-flex md4>
          <v-textarea
            rows="2"
            label="Bot description"
            v-model="botDescription"
          ></v-textarea>
        </v-flex>
      </v-layout>

      <v-layout>
        <v-flex md4>
          <v-label>Strategy</v-label>
          <v-select
            v-model="selectedStrategy"
            :items="strategies"
            item-text="name"
            item-value="id"
            label="Strategy"
            persistent-hint
            return-object
            single-line
          ></v-select>
        </v-flex>
      </v-layout>
      <v-layout>
        <v-flex>
          <v-switch
            color="success"
            v-model="botIsRunning"
            :label="`Running: ${botIsRunning.toString()}`"
          ></v-switch>
        </v-flex>
      </v-layout>
      <v-btn
        color="primary"
        class="mr-4 ml-0"
        @click="submit"
        :disabled="!valid"
      >
        Update
      </v-btn>
      <v-btn
        color="danger"
        class="mr-4 ml-0"
        :to="{ name: 'main-bots-details', params: { id: bot.id } }"
      >
        Cancel
      </v-btn>
    </v-form>
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
export default class EditBot extends Vue {
  public strategies: IStrategy[] = [];
  public bot?: IBot = undefined;
  public botName: string = '';
  public botDescription: string = '';
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
    console.log(this.bots);
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
    this.ready = true;
    console.log('Ready is true');
  }

  async deleteBot(id: number) {
    // TODO: check out @Watch
    await dispatchDeleteBot(this.$store, { id: id });
    this.$router.push('/main/home');
  }
  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedBot: IBotUpdate = {
        id: this.bot!.id,
        name: this.botName,
        description: this.botDescription,
        strategy_id: this.selectedStrategy!.id,
        is_running: this.botIsRunning,
      };
      console.log(this.botIsRunning);
      if (updatedBot.description === '') {
        updatedBot.description = this.bot!.name;
      }
      await dispatchUpdateBot(this.$store, updatedBot);
      this.$router.push(`/main/bots/details/${this.$route.params.id}`);
    }
  }
}
</script>
