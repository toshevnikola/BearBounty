<template>
  <div>
    <div id="dealsWrapper" v-if="dealsFetched">
      <v-data-table
        :items="deals"
        :headers="headers"
        @page-count="pageCount = $event"
        :items-per-page="itemsPerPage"
        :page.sync="page"
      >
        <template v-slot:item="{ item }">
          <tr>
            <td class="custom-class">{{ item.bot.name }}</td>
            <td class="custom-class">{{ item.pair }}</td>
            <td
              class="custom-class positiveProfit"
              v-if="computeProfit(item) > 0"
            >
              {{ computeProfit(item).toFixed(3) }} USDT
            </td>
            <td v-else-if="computeProfit(item) == null" class="custom-class">
              Active deal
            </td>
            <td class="custom-class negativeProfit" v-else>
              {{ computeProfit(item) }}
            </td>
            <td class="custom-class">
              {{ computeVolume(item).toFixed(3) }} USDT
            </td>
            <td class="custom-class">{{ computeStatus(item) }}</td>
            <td class="custom-class">{{ computeCreatedAt(item) }}</td>
            <td class="custom-class">
              <v-tooltip bottom open-delay="300">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    color="primary"
                    v-bind="attrs"
                    v-on="on"
                    @click="openDealDetails(item)"
                  >
                    mdi-view-list
                  </v-icon>
                </template>
                <span>Deal details</span>
              </v-tooltip>

              <v-tooltip bottom open-delay="300">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    color="red"
                    v-if="item.is_active == true"
                    v-bind="attrs"
                    v-on="on"
                    @click="stopDeal(item)"
                  >
                    mdi-stop
                  </v-icon>
                  <v-icon v-else disabled>mdi-stop</v-icon>
                </template>
                <span>Stop deal</span>
              </v-tooltip>
            </td>
          </tr>
        </template>
      </v-data-table>
    </div>
    <div v-else>
      <v-progress-circular
        :size="50"
        color="primary"
        indeterminate
      ></v-progress-circular>
    </div>
    <v-dialog v-model="dialog" v-if="dealDetails" max-width="700px">
      <v-card>
        <v-card-title>
          <span class="text-h4">Deal summary</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-timeline>
              <v-timeline-item
                v-for="(order, i) in dealDetails.orders"
                :key="i"
                :color="computeOrderColorType(order)"
              >
                <v-card :color="computeOrderColorType(order)" dark>
                  <v-card-title class="text-h6">
                    {{ order.type == 1 ? "Buy" : "Sell" }} Order
                  </v-card-title>
                  <v-card-text class="white text--primary">
                    <pre>
At: {{ computeCreatedAt(order) }}
Price: {{ order.price.toFixed(3) }}
Amount: {{ order.amount.toFixed(1) }} {{dealDetails.bot.base_coin}} 
Status: <span :class="computeOrderColorStatus(order)">{{ computeOrderStatus(order) }}</span>
 </pre>
                  </v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="accent" @click="closeDealDetails()"> Cancel </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import { api } from "@/api";
import { UserExchange, Deal, Order } from "@/interfaces";
import moment from "moment";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class DashboardDeals extends Vue {
  public dialog: boolean = false;
  public dealDetails: Deal | null = null;
  public deals: Array<Deal> = [];
  public pageCount: number = 5;
  public pageSize: number = 3;
  public page: number = 1;
  public itemsPerPage: number = 10;
  @Prop(Object) readonly selectedAccount!: UserExchange;
  public dealsFetched: boolean = false;
  public token: string = localStorage.authToken;
  public headers: Array<any> = [
    { text: "Bot", align: "left", value: "bot.name" },
    { text: "Pair", align: "left", value: "bot.pair" },
    { text: "Profit", align: "left", sortable: false },
    { text: "Volume", align: "left", sortable: false },
    { text: "Status", align: "left", value: "is_active" },
    { text: "Date created", align: "left", value: "created_at" },
    { text: "Actions", align: "left", sortable: false },
  ];

  public async mounted(): Promise<void> {
    await api
      .getDealsByExchange(this.token, this.selectedAccount.id)
      .then((res) => {
        this.deals = res.data;
        this.dealsFetched = true;
      });
  }
  public computeStatus(d: Deal): string {
    return d.is_active ? "Active" : "Completed";
  }
  public computeOrderStatus(o: Order): string {
    let s = o.status;
    switch (s) {
      case 1:
        return "Active";
      case 2:
        return "Completed";
      case 3:
        return "Canceled";
      default:
        return "Undefined";
    }
  }
  public computeOrderColorType(o: Order): string {
    let t = o.type;
    switch (t) {
      case 1:
        return "primary";
      case 2:
        return "secondary";
      default:
        return "accent";
    }
  }
  public computeOrderColorStatus(o: Order): string {
    let s = o.status;
    switch (s) {
      case 1:
        return "accentColor";
      case 2:
        return "greenColor";
      case 3:
        return "redColor";
      default:
        return "primaryColor";
    }
  }
  public computeCreatedAt(d: Deal | Order) {
    var dateObj = new Date(d.created_at);
    let mom = moment(dateObj).format("YYYY/MM/DD HH:mm:ss");
    console.log(d.created_at);
    console.log(mom);
    return mom;
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
  public computeVolume(d: Deal): number {
    let totalVolume = 0;
    d.orders.forEach((o) => {
      if (o.type == 1 && o.status == 2) {
        totalVolume += o.amount;
      }
    });
    return totalVolume;
  }
  public openDealDetails(deal: Deal) {
    this.dealDetails = deal;
    console.log(this.dealDetails);
    this.dialog = true;
  }
  public closeDealDetails() {
    this.dialog = false;
  }
}
</script>

<style>
#dealsWrapper {
  padding-top: 10%;
  width: 80%;
  margin-left: 10%;
  height: 500px;
}
th {
  background-color: #c4c4c4;
}
tr {
  color: #1c5d73;
  font-weight: bold;
}
td,
th {
  font-size: 18px !important;
}
th {
  color: #113c4a !important;
}
tr:nth-of-type(odd) {
  background-color: #f2f2f2;
}
tr:nth-of-type(even) {
  background-color: #ebebeb;
}
.positiveProfit {
  color: #489258;
}
.negativeProfit {
  color: #ff3d3d;
}
.accentColor {
  color: #3f7b70;
  font-weight: bolder;
}
.greenColor {
  color: #489258;
  font-weight: bolder;
}
.redColor {
  color: #ff3d3d;
  font-weight: bolder;
}
.primaryColor {
  color: #113c4a;
  font-weight: bolder;
}
</style>