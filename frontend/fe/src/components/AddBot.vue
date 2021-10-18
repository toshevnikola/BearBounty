<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      max-width="80%"
      persistent
      @click:outside="close()"
    >
      <v-card style="margin: 0; width: 100%; background: #ebebeb">
        <v-card-text style="margin: 0; width: 100%; padding: 0">
          <v-container>
            <v-row>
              <v-col cols="4" id="leftSide">
                <h2>Descriptive settings</h2>
                <br />
                <label>Name</label>
                <v-text-field placeholder="Example Bot Name" />
                <label>Description</label>
                <v-textarea placeholder="Example Bot Description" rows="2" />
                <label>Avatar</label>
                <v-card
                  style="
                    background: #ebebeb;
                    padding-left: 2.5%;
                    padding-top: 2.5%;
                    padding-bottom: 2.5%;
                  "
                >
                  <v-list-item
                    style="
                      display: inline-block;
                      width: 30%;
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
              <v-col cols="4">
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
                <label for="baseOrderAmount">Base order amount</label>
                <v-text-field value="10.00" placeholder="10.00" suffix="USDT" />

                <label for="targetProfit">Target Profit(%)</label><br />
                <v-text-field
                  style="width: 30%; display: inline-block"
                  name="targetProfit;"
                  value="1.00"
                  placeholder="1.00"
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
              </v-col>
              <v-col cols="4">test</v-col>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script lang="ts">
import { Component, Emit, Vue } from "vue-property-decorator";

@Component
export default class AddBot extends Vue {
  public dialog: boolean = true;
  public stopLossSwitch: boolean = false;
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
  public selectedAvatar: any = "";
  public setSelected(avatar: any): void {
    this.avatars.forEach((x) => {
      if (x.path === avatar.path) x.selected = true;
      else x.selected = false;
    });
    this.selectedAvatar = avatar;
  }
  public mounted(): void {
    this.setSelected(this.avatars[0]);
  }

  @Emit("isAddBotShown")
  public isBotShown(show: boolean): boolean {
    console.log("Emitting event");
    return show;
  }
  public close(): void {
    this.isBotShown(true);
  }

  public addBot(): void {
    console.log("close");
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
.combobox {
}
.combobox > * span {
  background-color: blue !important;
  color: green !important;
}
</style>