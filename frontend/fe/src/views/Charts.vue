<template>
  <div>
    <DashboardHeader @changeSelectedAccount="changeSelectedAccount" />
    <div id="dealsWrapper" v-if="currenciesFetched">
      <v-data-table
        :items="currencies"
        :headers="headers"
        @page-count="pageCount = $event"
        :items-per-page="itemsPerPage"
        :page.sync="page"
      >
        <template v-slot:item="{ item }">
          <tr>
            <td class="custom-class">
              {{ item.cmc_rank }}
            </td>
            <td class="custom-class">
              <v-img
                aspect-ratio="1"
                :src="`https://s2.coinmarketcap.com/static/img/coins/64x64/${item.id}.png`"
                lazy-src="https://s2.coinmarketcap.com/static/img/coins/64x64/1.png"
                max-width="25px"
                style="display: inline-block; float: left"
              >
              </v-img>
              <span style="margin: 0 10px; float: left">
                {{ item.name }}
              </span>
              <span style="color: #113c4a">{{ item.symbol }}</span>
            </td>
            <td class="custom-class">{{ item.quote.USD.price.toFixed(5) }}</td>
            <td
              class="custom-class positiveProfit"
              v-if="item.quote.USD.percent_change_24h > 0"
            >
              {{ item.quote.USD.percent_change_24h.toFixed(3) }}%
            </td>
            <td class="custom-class negativeProfit" v-else>
              {{ item.quote.USD.percent_change_24h.toFixed(3) }}%
            </td>
            <td class="custom-class">
              {{ item.quote.USD.volume_24h.toFixed(3) }}
            </td>
            <td class="custom-class">
              {{ item.quote.USD.market_cap.toFixed(3) }}
            </td>
          </tr></template
        >
      </v-data-table>
    </div>
    <div v-else>
      <v-progress-circular
        :size="70"
        :width="10"
        color="secondary"
        indeterminate
      ></v-progress-circular>
    </div>
  </div>
</template>

<script lang="ts">
import { CoinMarketCapResponse, UserExchange } from "@/interfaces";
import { Component, Vue } from "vue-property-decorator";
import DashboardHeader from "../components/DashboardHeader.vue";
import { api } from "../api";
@Component({ components: { DashboardHeader } })
export default class Charts extends Vue {
  public selectedAccount!: UserExchange;
  public coinGeckoResponse: CoinMarketCapResponse | undefined;
  public selectedAccountLoaded: boolean = false;
  public currenciesFetched: boolean = false;
  public currencies: Array<any> = [];
  public headers: Array<any> = [
    { text: "Rank", align: "left", value: "cmc_rank" },
    { text: "Name", align: "left", value: "symbol" },
    { text: "Price(USD)", align: "left", value: "quote.USD.price" },
    {
      text: "24h Change ",
      align: "left",
      value: "quote.USD.percent_change_24h",
    },
    { text: "24h Volume(USD)", align: "left", value: "quote.USD.volume_24h" },
    { text: "Market Cap(USD)", align: "left", value: "quote.USD.market_cap" },
  ];
  public itemsPerPage: number = 10;
  public page: number = 1;
  public mounted() {
    const token: string = localStorage.authToken;
    api.getCurrencies(token, "binance").then((res) => {
      this.coinGeckoResponse = res.data;
      if (this.coinGeckoResponse) this.currencies = this.coinGeckoResponse.data;
      console.log(this.currencies);
      this.currenciesFetched = true;
    });
  }
  public changeSelectedAccount(e: any): any {
    this.selectedAccount = e;
    this.selectedAccountLoaded = true;
  }
}
</script>

<style scoped>
.positiveProfit {
  color: #489258;
}
.negativeProfit {
  color: #ff3d3d;
}
</style>