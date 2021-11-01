<template id='container'>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      @click:outside="close(false)"
      content-class="custom-dialog"
      width="80%"
    >
      <v-card style="margin: 0; width: 100%; background: #ebebeb">
        <v-card-text style="margin: 0; width: 100%; padding: 0">
          <v-container>
            <v-row>
              <v-col cols="3" id="leftSide">
                <h2>Descriptive settings</h2>
                <br />
                <label>Name</label>
                <v-text-field
                  placeholder="Example Bot Name"
                  v-model="botName"
                />
                <label>Description</label>
                <v-textarea
                  placeholder="Example Bot Description"
                  rows="2"
                  v-model="botDescription"
                />
                <label>Avatar</label>
                <v-card style="background: #ebebeb">
                  <v-list-item
                    style="
                      display: inline-block;
                      width: 40%;
                      padding: 15px;
                      margin: 5px;
                    "
                    v-for="item in avatars"
                    :key="item.index"
                    class="avatarChoice"
                    :class="{ activeAvatar: item.selected }"
                    @click="setSelected(item)"
                  >
                    <v-img :src="require(`../assets/${item.path}`)" />
                  </v-list-item>
                </v-card>
              </v-col>
              <v-col cols="3">
                <h2>General settings</h2>
                <br />
                <label for="baseCoin">Base Coin</label>
                <v-text-field
                  name="baseCoin"
                  value="USDT"
                  disabled
                  readonly
                ></v-text-field>
                <label for="markets">Markets</label>
                <v-autocomplete
                  name="markets"
                  class="combobox"
                  v-model="selectedMarkets"
                  :items="markets"
                  label="Select markets"
                  multiple
                  small-chips
                  deletable-chips
                />
                <label for="maxActiveDeals">Max active deals</label>
                <v-text-field
                  v-model="maxActiveDeals"
                  name="maxActiveDeals"
                  :value="maxActiveDeals"
                  placeholder="1"
                />

                <label for="targetProfit">Target Profit(%)</label><br />
                <v-text-field
                  v-model="targetProfit"
                  style="width: 30%; display: inline-block"
                  name="targetProfit"
                  :value="targetProfit"
                  @input="updateChart()"
                  placeholder="1.25"
                  suffix="%"
                />
                <label> of total volume </label><br />
                <label for="stopLoss"
                  >Stop Loss ({{
                    stopLossSwitch ? "enabled" : "disabled"
                  }})</label
                >
                <v-switch
                  name="stopLoss"
                  inset
                  color="accent"
                  input-value="true"
                  v-model="stopLossSwitch"
                  style="width: 50px"
                />
                <label>Stop Loss(%)</label><br />
                <v-text-field
                  v-if="stopLossSwitch"
                  style="width: 30%; display: inline-block"
                  v-model.number="stopLossPct"
                  :value="stopLossPct"
                  placeholder="1.00"
                  suffix="%"
                />
                <v-text-field
                  v-else-if="!stopLossSwitch"
                  style="width: 30%; display: inline-block"
                  suffix="%"
                  :value="stopLossPct"
                  disabled
                />
              </v-col>
              <v-col cols="3">
                <h2>Order settings</h2>
                <br />
                <label>Base order amount</label>
                <v-text-field
                  v-model.number="baseOrderAmount"
                  @input="updateChart()"
                  :value="baseOrderAmount"
                  placeholder="10.00"
                  suffix="USDT"
                />
                <label>Safety order amount</label>
                <v-text-field
                  v-model.number="safetyOrderAmount"
                  :value="safetyOrderAmount"
                  @input="updateChart()"
                  placeholder="10.00"
                  suffix="USDT"
                />
                <label>
                  Safety order step scale
                  <v-tooltip right max-width="200px" color="accent">
                    <template v-slot:activator="{ on }">
                      <v-icon v-on="on"> mdi-information-outline </v-icon>
                    </template>
                    <span>
                      The Safety Order Step Scale is used to multiply the Price
                      Deviation percentage used by the last Safety Order for the
                      given deal.
                    </span>
                  </v-tooltip>
                </label>
                <v-text-field
                  :value="safetyOrderStepScale"
                  v-model="safetyOrderStepScale"
                  placeholder="1.5"
                />
                <label>Max. number of safety orders</label>
                <v-text-field
                  :value="maxNumberOfSafetyOrders"
                  v-model.number="maxNumberOfSafetyOrders"
                  @input="updateChart()"
                  placeholder="3"
                />
                <label>
                  Price deviation for safety orders (% from initial order)
                </label>
                <v-text-field
                  :value="priceDeviationforSafetyOrdersPct"
                  v-model="priceDeviationforSafetyOrdersPct"
                  placeholder="2.00"
                  suffix="%"
                />
                <label>Safety order amount scale</label>
                <v-text-field
                  :value="safetyOrderAmountScale"
                  v-model="safetyOrderAmountScale"
                  @input="updateChart()"
                  placeholder="1.25"
                />
              </v-col>
              <v-col cols="3">
                <h2>Finalize bot</h2>
                <br />
                <label>Amount used per order</label>
                <Linechart :key="chartId" :chartData="datacollection" />
                <h4>
                  Total required amount:
                  {{ parseFloat(totalRequiredAmount).toPrecision(6) }}
                  USDT
                </h4>
                <h4
                  :class="{
                    canCreate: totalRequiredAmount < baseAssetAvailable,
                    cannotCreate: totalRequiredAmount > baseAssetAvailable,
                  }"
                >
                  Account Balance: {{ baseAssetAvailable }} USDT
                </h4>
                <v-btn width="100%" @click="editBot()" color="secondary">
                  Edit Bot
                </v-btn>
                <v-btn width="100%" text @click="close(false)">Close</v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script lang="ts">
import Linechart from "./Linechart.vue";
import { Component, Emit, Prop, Vue } from "vue-property-decorator";
import { Bot, BotCreate, BotEdit, UserExchange } from "../interfaces";
import { api } from "../api";
@Component({ components: { Linechart } })
export default class EditBot extends Vue {
  @Prop(Object) readonly selectedAccount!: UserExchange;
  @Prop(Object) readonly bot!: Bot;
  public token: string = localStorage.authToken;
  public dialog: boolean = true;
  public botName: string = "";
  public botDescription: string = "";
  public selectedAvatar: any = "";
  public baseCoin: string = "USDT";
  public baseAssetAvailable: number = 0;
  public maxActiveDeals: number = 1;
  public stopLossSwitch: boolean = false;
  public targetProfit: number = 1.25;
  public stopLossPct: number = 10.0;
  public baseOrderAmount: number = 10.0;
  public safetyOrderAmount: number = 10.0;
  public safetyOrderStepScale: number = 1.5;
  public maxNumberOfSafetyOrders: number = 3;
  public priceDeviationforSafetyOrdersPct: number = 2.0;
  public safetyOrderAmountScale: number = 1.25;
  public chartId = 1;
  public editBotId: number = -1;
  public async editBot(): Promise<void> {
    if (!this.stopLossSwitch) {
      this.stopLossPct = 0;
    }
    const payload: BotEdit = {
      id: this.editBotId,
      name: this.botName,
      description: this.botDescription,
      trading_pairs: this.selectedMarkets,
      base_coin: this.baseCoin,
      base_order_amount: this.baseOrderAmount,
      safety_order_amount: this.safetyOrderAmount,
      max_safety_orders: this.maxNumberOfSafetyOrders,
      max_active_safety_orders: this.maxNumberOfSafetyOrders,
      safety_order_price_deviation_pct: this.priceDeviationforSafetyOrdersPct,
      safety_order_price_deviation_scale: this.safetyOrderStepScale,
      allocated_funds: this.totalRequiredAmount,
      stop_loss_pct: this.stopLossPct,
      take_profit_pct: this.targetProfit,
      avatar_color: this.selectedAvatar.color,
    };

    await api.updateBot(this.token, payload).then((res) => {
      console.log(res.data);
      this.close(true);
    });
  }
  public avatars: Array<any> = [
    { path: "robot_purple.png", selected: true, color: "purple" },
    { path: "robot_orange.png", selected: false, color: "orange" },
    { path: "robot_blue.png", selected: false, color: "blue" },
    { path: "robot_dark_blue.png", selected: false, color: "dark_blue" },
    { path: "robot_green.png", selected: false, color: "green" },
    { path: "robot_silver.png", selected: false, color: "silver" },
  ];
  public selectedMarkets: Array<any> = [];
  public markets: Array<any> = [];
  public orderAmounts: Array<number> = [];
  public orderLabels: Array<number> = [];
  public cummulativeOrderAmounts: Array<number> = [];
  public potentialProfits: Array<number> = [];
  public datacollection: any = {
    labels: this.orderLabels,
    datasets: [
      {
        label: "Orders",
        pointBackgroundColor: "#f0943d",
        borderColor: "#f0943d",
        data: this.orderAmounts,
      },
      {
        label: "Cummulative Required",
        pointBackgroundColor: "#113c4a",
        borderColor: "#113c4a",
        data: this.cummulativeOrderAmounts,
      },
      {
        label: "Profits",
        pointBackgroundColor: "#2e6361",
        borderColor: "#2e6361",
        data: this.potentialProfits,
      },
    ],
  };
  public totalRequiredAmount = 0;
  public getTotalRequiredAmount(): void {
    this.totalRequiredAmount = this.orderAmounts.reduce(
      (accumulator, currentValue) => accumulator + currentValue
    );
  }
  public setSelected(avatar: any): void {
    this.avatars.forEach((x) => {
      if (x.path === avatar.path) x.selected = true;
      else x.selected = false;
    });
    this.selectedAvatar = avatar;
  }
  public setSelectedAvatarByColor(avatarColor: string): void {
    this.avatars.forEach((x) => {
      if (x.color === avatarColor) {
        x.selected = true;
        this.selectedAvatar = x;
      } else x.selected = false;
    });
  }
  public mounted(): void {
    this.markets = this.selectedAccount.exchange.supported_pairs;

    if (typeof this.bot.stop_loss_pct !== "undefined") {
      this.stopLossPct = this.bot.stop_loss_pct;
      console.log("stoplosspct", this.stopLossPct);
      if (this.bot.stop_loss_pct === 0) {
        this.stopLossSwitch = false;
      } else {
        this.stopLossSwitch = true;
      }
    }
    this.editBotId = this.bot.id;
    if (this.bot.avatar_color)
      this.setSelectedAvatarByColor(this.bot.avatar_color);
    if (this.bot.base_coin) this.baseCoin = this.bot.base_coin;
    this.getAsset(this.baseCoin);
    if (this.bot.name) this.botName = this.bot.name;
    if (this.bot.description) this.botDescription = this.bot.description;
    if (this.bot.trading_pairs) this.selectedMarkets = this.bot.trading_pairs;
    if (this.bot.take_profit_pct) this.targetProfit = this.bot.take_profit_pct;
    if (this.bot.base_order_amount)
      this.baseOrderAmount = this.bot.base_order_amount;
    if (this.bot.safety_order_amount)
      this.safetyOrderAmount = this.bot.safety_order_amount;
    if (this.bot.safety_order_price_deviation_scale)
      this.safetyOrderAmountScale = this.bot.safety_order_price_deviation_scale;
    if (this.bot.safety_order_price_deviation_pct)
      this.priceDeviationforSafetyOrdersPct =
        this.bot.safety_order_price_deviation_pct;
    if (this.bot.max_safety_orders)
      this.maxNumberOfSafetyOrders = this.bot.max_safety_orders;
    if (this.bot.max_active_safety_orders)
      this.maxActiveDeals = this.bot.max_active_safety_orders;
    this.updateChart();
  }
  public updateChart(): void {
    this.orderAmounts.length = this.maxNumberOfSafetyOrders;
    this.orderLabels.length = this.maxNumberOfSafetyOrders;
    this.cummulativeOrderAmounts.length = this.maxNumberOfSafetyOrders;
    this.potentialProfits.length = this.maxNumberOfSafetyOrders;
    this.setOrderAmounts();
    this.setOrderLabels();
    this.setCummulativeOrderAmounts();
    this.getTotalRequiredAmount();
    this.reRenderChart();
  }

  public setOrderAmounts(): void {
    this.orderAmounts[0] = this.baseOrderAmount;
    this.orderAmounts[1] = this.safetyOrderAmount;
    for (let i = 2; i <= this.maxNumberOfSafetyOrders; i++) {
      this.orderAmounts[i] =
        this.orderAmounts[i - 1] * this.safetyOrderAmountScale;
    }
  }
  public setCummulativeOrderAmounts(): void {
    for (let i = 0; i < this.orderAmounts.length; i++) {
      let k: number = 0;
      for (let j = 0; j <= i; j++) {
        k += this.orderAmounts[j];
      }
      this.cummulativeOrderAmounts[i] = k;
      this.potentialProfits[i] = (this.targetProfit / 100) * k;
    }
  }
  public setOrderLabels(): void {
    for (let i = 0; i < this.orderAmounts.length; i++) {
      this.orderLabels[i] = i + 1;
    }
  }
  public reRenderChart(): void {
    this.chartId += 1;
  }

  @Emit("isEditBotShown")
  public isBotShown(show: boolean, isCreated: boolean): any {
    return { show, isCreated };
  }
  public close(isCreated: boolean): void {
    this.isBotShown(true, isCreated);
  }
  public getAsset(asset: string): any {
    this.selectedAccount.assets.forEach((element) => {
      if (element["asset"] === asset) {
        this.baseAssetAvailable = parseFloat(element["free"]);
      }
    });
  }
}
</script>


<style scoped>
h1 {
  color: #1c5d73;
}
input {
  font-size: 20px;
  font-family: Helvetica, Arial, sans-serif;
  color: #929292;
  font-weight: 700;
  background-color: #c4c4c4;
  width: 395px;
  height: 47px;
  padding-left: 20px;
}
input:focus {
  border: none;
}
.avatarChoice:hover {
  background-color: #86b7c7d3;
  border-radius: 5%;
}
/* #rightSide {
  background-color: #113c4a;
  vertical-align: middle;
  position: relative;
  padding: 0;
} */
#leftSide {
  background-color: #ebebeb;
  border-right: 5px solid #dddddd;
  padding-right: 20px;
}
#add {
  width: 40%;
  font-size: 20px;
  display: inline-block;
  background: #f0943d;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  text-align: center;
  padding: 25px 0;
  margin-top: 1%;
  margin-left: 10px;
}

#cancel {
  width: 40%;
  font-size: 20px;
  display: inline-block;
  color: #113c4a;
  text-decoration: none;
  border-radius: 5px;
  text-align: center;
  padding: 25px 0;
  margin-top: 1%;
}
#loginGoogle {
  width: 395px;
  font-size: 20px;
  display: block;
  background-color: #2e6361;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  float: left;
  text-align: center;
  padding: 25px 0;
  margin-top: 1%;
  margin-bottom: 50px;
}
.activeAvatar {
  background-color: #1c5d73b9 !important;
  border-radius: 5%;
}
div.container {
  padding-top: 40px;
  padding-bottom: 40px;
}
.canCreate {
  color: #489258;
}
.cannotCreate {
  color: #ff3d3d;
}
</style>
