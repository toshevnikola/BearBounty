<template>
  <v-container fluid>
    <v-layout wrap>
      <v-flex md4 v-for="bot in bots" :key="bot.id">
        <v-card class="mx-auto ma-4" max-width="400">
          <v-card-title class="font-weight-600 display-1 ">{{
            bot.name
          }}</v-card-title>
          <v-card-text>{{ bot.description }}</v-card-text>
          <v-btn @click="deleteBot(bot.id)">Delete</v-btn>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { dispatchGetBots, dispatchDeleteBot } from '@/store/main/actions';
import { readBots } from '@/store/main/getters';
import { IBot } from '@/interfaces';

@Component
export default class Home extends Vue {
  public bots: IBot[] = [];

  getBots() {
    return readBots(this.$store);
  }
  async deleteBot(id: number) {
    // TODO: check out @Watch to avoid removing the deleted bot this twice.
    await dispatchDeleteBot(this.$store, { id: id });
    for (var i = 0; i < this.bots.length; i++) {
      if (this.bots[i].id === id) {
        this.bots.splice(i, 1);
        break;
      }
    }
  }

  public async mounted() {
    await dispatchGetBots(this.$store);
    this.bots = this.getBots();
  }
}
</script>
