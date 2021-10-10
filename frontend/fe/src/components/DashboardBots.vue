<template>
  <div id="botsContainer">
    <div class="botCard" v-for="bot in bots" :key="bot.id">
      <div class="botActions">
        <div class="text-right">
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon color="primary" v-bind="attrs" v-on="on">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list color="marketchipstext">
              <v-list-item>
                <v-list-item-title
                  class="marketchipsbg--text"
                  style="cursor: pointer"
                  @click="toggleIsRunning(bot)"
                >
                  <v-icon v-if="bot.is_running" class="marketchipsbg--text"
                    >mdi-pause</v-icon
                  >
                  <v-icon v-else class="marketchipsbg--text"> mdi-play </v-icon>
                  <span v-if="bot.is_running"> Pause</span>
                  <span v-else>Start</span>
                </v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-list-item-title
                  class="marketchipsbg--text"
                  style="cursor: pointer"
                  @click="editBot(bot.id)"
                >
                  <v-icon class="marketchipsbg--text">mdi-pencil</v-icon>
                  Edit
                </v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-list-item-title
                  class="marketchipsbg--text"
                  style="cursor: pointer"
                  @click="deleteBot(bot)"
                >
                  <v-icon class="marketchipsbg--text">mdi-delete</v-icon>
                  Delete
                </v-list-item-title>
              </v-list-item>
              <v-list-item>
                <v-list-item-title
                  class="marketchipsbg--text"
                  style="cursor: pointer"
                  @click="deleteBot(bot.id)"
                >
                  <v-icon class="marketchipsbg--text">mdi-view-list</v-icon>
                  View deals
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </div>
      </div>
      <div
        class="botImgWrapper"
        :class="{ activeBot: bot.is_running, inactiveBot: !bot.is_running }"
      >
        <img src="../assets/robot.png" />
      </div>
      <div class="botTitleWrapper">
        <h2 class="botTitle">{{ bot.name }}</h2>
      </div>
      <div class="detailsWrapper">
        <span class="greenText">Type</span><br />
        <span class="blueText">Signals based</span><br />
        <span class="greenText">Markets</span><br />
        <div class="markets">
          <v-chip
            v-for="market in bot.trading_pairs"
            :key="market"
            color="marketchipsbg"
            class="marketchipstext--text market"
          >
            {{ market }}
          </v-chip>
        </div>
        <span class="greenText">Allocated funds</span><br />
        <span class="blueText">{{ bot.allocated_funds }}</span
        ><br />
        <span class="greenText">Base Coin</span><br />
        <span class="blueText">{{ bot.base_coin }}</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { Bot, UserExchange, BotEdit } from "../interfaces";
import { api } from "../api";
@Component
export default class DashboardBots extends Vue {
  public bots: Array<Bot> = [];
  @Prop(Object) readonly selectedAccount!: UserExchange;
  public botsFetched: boolean = false;
  public token: string = localStorage.authToken;

  public botActionOptions: Array<any> = [
    { title: "Pause", icon: "mdi-pause" },
    { title: "Delete", icon: "mdi-delete" },
    { title: "Edit", icon: "mdi-pencil" },
  ];
  public async mounted() {
    await api
      .getBotsByUserExchange(this.token, this.selectedAccount.id)
      .then((res: any) => {
        this.bots = res.data;
        this.botsFetched = true;
      });
  }
  public editBot(e: any): void {
    console.log(e);
  }
  public async deleteBot(bot: any): Promise<void> {
    await api.deleteBot(this.token, bot.id).then((res) => {
      this.bots = this.bots.filter((b) => b !== bot);
    });
  }
  public async toggleIsRunning(bot: Bot): Promise<void> {
    const payload: BotEdit = {
      is_running: !bot.is_running,
    };
    await api.updateBot(this.token, bot.id, payload).then((res) => {
      this.bots.forEach((x) => {
        if (x.id === bot.id) {
          x.is_running = !x.is_running;
        }
      });
    });
  }
  public viewDeals(e: any): void {
    console.log(e);
  }
}
</script>

<style scoped>
#botsContainer {
  width: 100%;
  margin-left: 10%;
  padding-top: 10%;
}
.botCard {
  border-radius: 5px;
  background-color: #c4c4c4;
  float: left;
  width: 300px;
  height: 430px;
  margin-right: 50px;
  margin-bottom: 5%;
}
.botImgWrapper > img {
  padding-left: 5px;
}
.botImgWrapper {
  float: left;
  width: 40%;
  display: inline-block;
  margin: 0;
}
.inactiveBot {
  border-left: 5px solid #ff3d3d;
}
.activeBot {
  border-left: 5px solid #489258;
}
.botTitle {
  float: left;
  /* display: inline-block; */
  color: #1c5d73;
  font-size: 32px;
}
.botTitleWrapper {
  height: 90px;
  vertical-align: 50%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: left;
}
.detailsWrapper {
  padding-left: 20px;
}
.greenText {
  font-size: 24px;
  font-weight: normal;
  color: #3f7b70;
}
.blueText {
  font-size: 24px;
  font-weight: normal;
  color: #1c5d73;
}
.market {
  margin-right: 10px;
}
.botActions {
  width: 100%;
  align-content: right;
  text-align: right;
  margin: 0;
  padding: 0;
}
</style>