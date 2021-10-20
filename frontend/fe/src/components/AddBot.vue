<template id='container'>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      @click:outside="close()"
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
                <LineChart :key="chartId" :chartData="datacollection" />
                <h4>Total required amount: {{ totalRequiredAmount }} USDT</h4>
                <h4>Account Balance: 52.513123 USDT</h4>
                <v-btn width="100%" @click="createBot()" color="secondary">
                  Create Bot
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script lang="ts">
import LineChart from "./Linechart.vue.js";
import { Component, Emit, Prop, Vue } from "vue-property-decorator";
import { BotCreate, UserExchange } from "../interfaces";
import { api } from "../api";
@Component({ components: { LineChart } })
export default class AddBot extends Vue {
  @Prop(Object) readonly selectedAccount!: UserExchange;
  public token: string = localStorage.authToken;
  public dialog: boolean = true;
  public botName: string = "";
  public botDescription: string = "";
  public selectedAvatar: any = "";
  public baseCoin: string = "USDT";
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
  public async createBot(): Promise<void> {
    const payload: BotCreate = {
      name: this.botName,
      trading_pairs: this.selectedMarkets,
      base_coin: this.baseCoin,
      base_order_amount: this.baseOrderAmount,
      safety_order_amount: this.safetyOrderAmount,
      max_safety_orders: this.maxNumberOfSafetyOrders,
      max_active_safety_orders: this.maxNumberOfSafetyOrders,
      safety_order_price_deviation_pct: this.priceDeviationforSafetyOrdersPct,
      safety_order_price_deviation_scale: this.safetyOrderStepScale,
      allocated_funds: this.totalRequiredAmount,
      consider_overall_sentiment: false,
      stop_loss_pct: this.stopLossPct,
      take_profit_pct: this.targetProfit,
      is_running: true,
      in_deal: false,
      user_exchange_id: this.selectedAccount.id,
    };

    await api.createBot(this.token, payload).then((res) => {
      console.log(res.data);
      this.close();
    });
  }
  public avatars: Array<any> = [
    { path: "robot_purple.png", selected: true },
    { path: "robot_orange.png", selected: false },
    { path: "robot_blue.png", selected: false },
    { path: "robot_dark_blue.png", selected: false },
    { path: "robot_green.png", selected: false },
    { path: "robot_silver.png", selected: false },
  ];
  public selectedMarkets: Array<any> = ["ETHUSDT", "BTCUSDT"];
  public markets: Array<any> = [
    "BTCUSDT",
    "ETHUSDT",
    "LSKUSDT",
    "ZILUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "BNBUSDT",
    "SUNUSDT",
    "DOGEUSDT",
    "SHIBUDST",
    "BTCGUSDT",
  ];
  public orderAmounts: Array<number> = [];
  public orderLabels: Array<number> = [];
  public cummulativeOrderAmounts: Array<number> = [];
  public datacollection: any = {
    labels: this.orderLabels,
    datasets: [
      {
        label: "Single",
        pointBackgroundColor: "#f0943d",
        borderColor: "#f0943d",
        data: this.orderAmounts,
      },
      {
        label: "Cummulative",
        pointBackgroundColor: "#113c4a",
        borderColor: "#113c4a",
        data: this.cummulativeOrderAmounts,
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
  public mounted(): void {
    this.setSelected(this.avatars[0]);
    this.setMaxActiveDealsValue();
    this.updateChart();
  }
  public updateChart(): void {
    this.orderAmounts.length = this.maxNumberOfSafetyOrders;
    this.orderLabels.length = this.maxNumberOfSafetyOrders;
    this.cummulativeOrderAmounts.length = this.maxNumberOfSafetyOrders;
    this.setOrderAmounts();
    this.setOrderLabels();
    this.setCummulativeOrderAmounts();
    this.getTotalRequiredAmount();
    this.reRenderChart();
  }
  public setMaxActiveDealsValue(): void {
    this.maxActiveDeals = this.selectedMarkets.length;
  }
  public setOrderAmounts(): void {
    this.orderAmounts[0] = this.baseOrderAmount;
    this.orderAmounts[1] = this.safetyOrderAmount;
    for (let i = 2; i <= this.maxNumberOfSafetyOrders; i++) {
      this.orderAmounts[i] =
        this.orderAmounts[i - 1] * this.safetyOrderAmountScale;
      // console.log(this.orderAmounts[i - 1] * this.safetyOrderAmountScale);
    }
    // console.log(this.orderAmounts);
  }
  public setCummulativeOrderAmounts(): void {
    for (let i = 0; i < this.orderAmounts.length; i++) {
      let k: number = 0;
      for (let j = 0; j <= i; j++) {
        k += this.orderAmounts[j];
        // console.log("k=", k);
      }
      this.cummulativeOrderAmounts[i] = k;
    }
    // console.log(this.cummulativeOrderAmounts);
  }
  public setOrderLabels(): void {
    for (let i = 0; i < this.orderAmounts.length; i++) {
      this.orderLabels[i] = i + 1;
    }
  }
  public reRenderChart(): void {
    this.chartId += 1;
  }

  @Emit("isAddBotShown")
  public isBotShown(show: boolean): boolean {
    return show;
  }
  public close(): void {
    this.isBotShown(true);
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
</style>
