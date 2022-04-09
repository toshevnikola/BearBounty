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
          large
          color="#1C5D73"
          class="dddddd--text"
          id="addExchangeBtn"
          @click="openAddExchange()"
        >
          Add Exchange
          <v-icon>mdi-plus-box</v-icon>
        </v-btn>
      </div>
    </div>
    <div id="dealsWrapper" v-if="exchangesFetched">
      <v-data-table
        :headers="headers"
        :items="exchanges"
        @page-count="pageCount = $event"
        :items-per-page="itemsPerPage"
        :page.sync="page"
      >
        <template v-slot:item="{ item }">
          <tr>
            <td class="text-xs-right">{{ item.exchange.name }}</td>
            <td class="text-xs-right">{{ computeCreatedAt(item) }}</td>
            <td class="text-xs-right">
              <v-btn icon> <v-icon color="primary"> mdi-delete</v-icon> </v-btn>
              <v-btn icon> <v-icon color="primary"> mdi-pencil</v-icon> </v-btn>
              <v-btn icon> <v-icon color="primary"> mdi-robot</v-icon> </v-btn>
            </td>
          </tr>
        </template>
      </v-data-table>
    </div>
    <AddExchange
      @isAddExchangeShown="closeAddExchange()"
      v-if="isAddExchangeShown"
    />
  </div>
</template>

<script lang="ts">
import { api } from "@/api";
import { Deal, Order, UserExchange } from "@/interfaces";
import moment from "moment";
import { Component, Prop, Vue } from "vue-property-decorator";
import AddExchange from "../components/AddExchange.vue";
@Component({ components: { AddExchange } })
export default class ExchangesView extends Vue {
  public exchanges: Array<UserExchange> = [];
  public pageCount: number = 5;
  public pageSize: number = 3;
  public page: number = 1;
  @Prop(Object) readonly selectedAccount!: UserExchange;
  public exchangesFetched: boolean = false;
  public isAddExchangeShown: boolean = false;
  public token: string = localStorage.authToken;
  public headers: Array<any> = [
    {
      text: "Exchange",
      align: "left",
      value: "exchange.name",
    },
    {
      text: "Date connected",
      value: "created_at",
      align: "left",
    },
    {
      text: "Actions",
      value: "actions",
      align: "left",
    },
  ];

  public async mounted(): Promise<void> {
    console.log("MOUNTED!");
    await api.getUserExchanges(this.token).then((res) => {
      this.exchanges = res.data;
      this.exchangesFetched = true;
      console.log(this.exchanges);
    });
  }
  public openAddExchange(): void {
    this.isAddExchangeShown = true;
    console.log("Exchange shown");
  }
  public closeAddExchange(): void {
    this.isAddExchangeShown = false;
    console.log("Exchange closed");
  }
  public computeCreatedAt(d: Deal | Order) {
    var dateObj = new Date(d.created_at);
    let mom = moment(dateObj).format("YYYY/MM/DD HH:mm:ss");
    console.log(d.created_at);
    console.log(mom);
    return mom;
  }
}
</script>

<style scoped>
#dealsWrapper {
  padding-top: 50px;
  width: 70%;
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
#optionsContainer {
  height: 50px;
  margin-bottom: 10px;
  width: 90%;
}
#container {
  padding-top: 7%;
  margin-left: 10%;
}
#addExchangeBtn {
  text-transform: none;
  font-size: 14px;
  font-weight: normal;
  font-family: Roboto;
}
</style>