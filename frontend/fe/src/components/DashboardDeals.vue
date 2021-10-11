<template>
  <div id="dealsWrapper" v-if="dealsFetched">
    <v-data-table :headers="headers" :items="deals" :footer-props="{}">
      <template slot="items" slot-scope="props">
        <td class="text-xs-right">{{ props.item.bot_name }}</td>
        <td class="text-xs-right">{{ props.item.pair }}</td>
        <td class="text-xs-right">150</td>
        <td class="text-xs-right">15</td>
        <td class="text-xs-right">{{ props.item.is_active }}</td>
        <td class="text-xs-right">{{ props.item.created_at }}</td>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { api } from "@/api";
import { UserExchange, Deal } from "@/interfaces";
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class DashboardDeals extends Vue {
  public deals: Array<Deal> = [];
  @Prop(Object) readonly selectedAccount!: UserExchange;
  public dealsFetched: boolean = false;
  public token: string = localStorage.authToken;
  public headers: Array<any> = [
    {
      text: "Bot",
      align: "left",
      value: "bot_name",
    },
    {
      text: "Pair",
      value: "pair",
    },
    {
      text: "Profit",
      value: "profit",
    },
    {
      text: "Volume",
      value: "volume",
    },
    {
      text: "Status",
      value: "is_active",
    },
    {
      text: "Actions",
      value: "created_at",
    },
  ];

  public async mounted(): Promise<void> {
    await api
      .getDealsByExchange(this.token, this.selectedAccount.id)
      .then((res) => {
        console.log(res.data);
        this.deals = res.data;
        let d1: Deal = {
          bot_id: 1,
          bot_name: "Test Bot",
          pair: "ETHUSDT",
          is_active: true,
          created_at: "123123",
          updated_at: "1231234",
        };
        let d2 = d1;
        this.deals = [d1, d2];
        console.log(this.deals);
        this.dealsFetched = true;
      });
  }
}
</script>

<style>
#dealsWrapper {
  padding-top: 10%;
  width: 80%;
  margin-left: 10%;
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
v-data-footer {
  background-color: red;
}
</style>