<template>
  <div id="container">
    <div id="optionsContainer">
      <div style="width: 50%; display: inline-block; float: left">
        <h3 style="font-size: 24px">
          <v-icon large color="#1C5D73">mdi-swap-vertical</v-icon> Created time
        </h3>
        <h3 style="font-size: 24px">
          <v-icon large color="#1C5D73">mdi-filter</v-icon> All
        </h3>
      </div>
      <div
        style="
          width: 50%;
          display: inline-block;
          text-align: right;
          height: 100%;
          float: left;
          padding-top: 20px;
        "
      >
        <v-btn
          @click="openAddBot()"
          large
          color="#1C5D73"
          class="dddddd--text"
          id="addBotBtn"
        >
          Add Bot
          <v-icon>mdi-plus-box</v-icon>
        </v-btn>
      </div>
    </div>
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
                    <v-icon v-if="bot.is_running" class="marketchipsbg--text">
                      mdi-pause
                    </v-icon>
                    <v-icon v-else class="marketchipsbg--text">
                      mdi-play
                    </v-icon>
                    <span v-if="bot.is_running"> Pause</span>
                    <span v-else>Start</span>
                  </v-list-item-title>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title
                    class="marketchipsbg--text"
                    style="cursor: pointer"
                    @click="editBot(bot)"
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
          <img :src="require('../assets/robot_' + bot.avatar_color + '.png')" />
          <!-- <img src="../assets/robot_orange.png" alt="" /> -->
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
              small
              v-for="market in bot.trading_pairs.slice(0, 9)"
              :key="market"
              color="marketchipsbg"
              class="marketchipstext--text market"
            >
              {{ market }}
            </v-chip>
          </div>
          <span class="greenText">Allocated funds</span> <br />
          <span class="blueText">
            {{ bot.allocated_funds.toFixed(2) }} {{ bot.base_coin }}
          </span>
          <br />
          <!-- <span class="greenText">Total profit</span> <br /> -->
          <!-- <span class="blueText"> {{ totalProfit(bot).toFixed(3) }} USDT </span> -->
        </div>
      </div>
    </div>
    <AddBot
      :selectedAccount="selectedAccount"
      @isAddBotShown="closeAddBot"
      v-if="isAddBotShown"
    />
    <EditBot
      @isEditBotShown="closeEditBot"
      v-if="isEditBotShown"
      :selectedAccount="selectedAccount"
      :bot="botToEdit"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { Bot, UserExchange, BotEdit, Deal } from "../interfaces";
import { api } from "../api";
import AddBot from "../components/AddBot.vue";
import EditBot from "../components/EditBot.vue";
@Component({ components: { AddBot, EditBot } })
export default class DashboardBots extends Vue {
  public bots: Array<Bot> = [];
  @Prop(Object) readonly selectedAccount!: UserExchange;
  public botsFetched: boolean = false;
  public token: string = localStorage.authToken;
  public isAddBotShown: boolean = false;
  public isEditBotShown: boolean = false;
  public botToEdit: Bot | undefined;

  public botActionOptions: Array<any> = [
    { title: "Pause", icon: "mdi-pause" },
    { title: "Delete", icon: "mdi-delete" },
    { title: "Edit", icon: "mdi-pencil" },
  ];
  public async mounted() {
    this.refreshBots();
  }
  public async refreshBots(): Promise<any> {
    await api
      .getBotsByUserExchange(this.token, this.selectedAccount.id)
      .then((res: any) => {
        this.bots = res.data;
        this.botsFetched = true;
      });
  }
  public editBot(bot: any): void {
    this.botToEdit = bot;
    this.openEditBot();
  }

  public computeProfitForDeal(d: Deal): number | null {
    let totalBuy = 0;
    let avgBuy = 0;
    let totalSell = 0;
    let sellAmount = 0;
    let sellPrice = 0;
    d.orders.forEach((order) => {
      if (order.status === 1) {
        return 0;
      } else if (order.type === 1 && order.status === 2) {
        totalBuy += order.amount / order.price;
      } else if (order.type === 2 && order.status === 2) {
        totalSell = order.amount / order.price;
        sellAmount = order.amount;
        sellPrice = order.price;
      }
    });
    if (sellAmount != 0) {
      return (totalBuy - totalSell) * sellPrice;
    }
    return null;
  }

  public totalProfit(bot: Bot): number {
    let totalProfit = 0;
    if (bot.deals) {
      bot.deals.forEach((d) => {
        if (d) {
          console.log(d);
          let profitForDeal = this.computeProfitForDeal(d);
          if (profitForDeal) {
            totalProfit += profitForDeal;
          }
        }
      });
      return totalProfit;
    }
    return 0;
  }
  public computeProfit(d: Deal): number | null {
    let totalBuy = 0;
    let avgBuy = 0;
    let totalSell = 0;
    let sellAmount = 0;
    let sellPrice = 0;
    d.orders.forEach((order) => {
      if (order.status === 1) {
        return 0;
      } else if (order.type === 1 && order.status === 2) {
        totalBuy += order.amount / order.price;
      } else if (order.type === 2 && order.status === 2) {
        totalSell = order.amount / order.price;
        sellAmount = order.amount;
        sellPrice = order.price;
      }
    });
    if (sellAmount != 0) {
      return (totalBuy - totalSell) * sellPrice;
    }
    return null;
  }

  public async deleteBot(bot: any): Promise<void> {
    await api.deleteBot(this.token, bot.id).then((res) => {
      this.bots = this.bots.filter((b) => b !== bot);
    });
  }

  public openAddBot(): void {
    this.isAddBotShown = true;
  }
  public openEditBot(): void {
    this.isEditBotShown = true;
  }

  public closeAddBot(e: any): void {
    this.isAddBotShown = !e["show"];
    let isCreated: boolean = e["isCreated"];
    if (isCreated) {
      this.refreshBots();
    }
  }
  public closeEditBot(e: any): void {
    this.isEditBotShown = !e["show"];
    let isCreated: boolean = e["isCreated"];
    if (isCreated) {
      this.refreshBots();
    }
  }

  public async toggleIsRunning(bot: Bot): Promise<void> {
    const payload: BotEdit = {
      id: bot.id,
      is_running: !bot.is_running,
    };
    await api.updateBot(this.token, payload).then((res) => {
      this.bots.forEach((x) => {
        if (x.id === bot.id) {
          x.is_running = !x.is_running;
        }
      });
    });
  }
  public viewDeals(e: any): void {}
}
</script>

<style scoped>
#botsContainer {
  width: 100%;
}
.botCard {
  border-radius: 10px;
  background-color: #c4c4c4;
  float: left;
  width: 300px;
  height: 380px;
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
  font-size: 28px;
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
#optionsContainer {
  height: 100px;
  margin-bottom: 10px;
  width: 90%;
}
#container {
  padding-top: 7%;
  margin-left: 10%;
}
#addBotBtn {
  text-transform: none;
  font-size: 16px;
  font-weight: normal;
  font-family: Roboto;
}
</style>