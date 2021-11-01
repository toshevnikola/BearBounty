<template>
  <div>
    <DashboardHeader @changeSelectedAccount="changeSelectedAccount" />
    <v-container v-if="selectedAccountLoaded">
      <v-row>
        <v-col cols="7" class="lineChartContainer">
          <h3>Portfolio over past 7 days</h3>
          <Linechart
            :key="lineChartId"
            :chartData="lineChartData"
            :options="lineChartOptions"
          />
          <v-col cols="1"></v-col>
        </v-col>
        <v-col cols="4" class="doughnutContainer">
          <div style="padding: 20px">
            <h3>Portfolio Allocation in USDT</h3>
            <Doughnut :key="chartId" :chartData="chartData" id="doughnut" />
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { UserExchange } from "@/interfaces";
import { Component, Vue, Watch } from "vue-property-decorator";
import Doughnut from "../components/Doughnut.vue";
import Linechart from "../components/Linechart.vue";
import DashboardHeader from "../components/DashboardHeader.vue";
import moment from "moment";
@Component({ components: { Doughnut, DashboardHeader, Linechart } })
export default class Statistics extends Vue {
  public chartId: number = 1;
  public lineChartId: number = 1;
  public selectedAccount!: UserExchange;
  public selectedAccountLoaded: boolean = false;
  public doughnutColors: Array<string> = [
    "#FF3D3D",
    "#3F7B70",
    "#F0B90B",
    "#FAA453",
    "#2F88FF",
    "#113C4A",
    "#1C5D73",
    "#6B3DF0",
    "#489258",
    "#00B312",
  ];
  public assets: Array<any> = [];
  public values: Array<any> = [];
  public generateDays() {
    let daysAgo = [];
    for (var i = 0; i <= 6; i++) {
      daysAgo[i] = moment().subtract(i, "days").format("DD/MM/YYYY");
    }
    return daysAgo.reverse();
  }

  public generateFakeSnapshots() {
    return [
      this.calculatetotalBalance() - (this.calculatetotalBalance() * 3) / 100,
      this.calculatetotalBalance() - (this.calculatetotalBalance() * 5) / 100,
      this.calculatetotalBalance() + (this.calculatetotalBalance() * 1) / 100,
      this.calculatetotalBalance() + (this.calculatetotalBalance() * 1.5) / 100,
      this.calculatetotalBalance() - (this.calculatetotalBalance() * 2.9) / 100,
      this.calculatetotalBalance() - (this.calculatetotalBalance() * 3) / 100,
      this.calculatetotalBalance(),
    ];
  }
  public mounted() {}
  public changeSelectedAccount(e: any): any {
    this.selectedAccount = e;
    this.selectedAccountLoaded = true;
    this.setAssets();
    this.reRenderCharts();
  }
  public reRenderCharts(): void {
    this.chartId += 1;
    this.lineChartId += 1;
  }
  public calculatetotalBalance(): number {
    let s: number = 0;

    this.selectedAccount.assets.forEach((x) => {
      if (x.asset !== "USDT")
        s += (parseFloat(x.locked) + parseFloat(x.free)) * parseFloat(x.price);
      else s += parseFloat(x.free) + parseFloat(x.locked);
    });
    return s;
  }
  @Watch("assets", { deep: true })
  public changeAssets(newVal: any, oldVal: any) {
    this.chartData.labels = newVal.map((x: any) => x.asset);
    this.chartData.datasets[0].data = newVal.map((x: any) => {
      console.log(x);
      if (x.asset !== "USDT")
        return (
          (parseFloat(x.locked) + parseFloat(x.free)) * parseFloat(x.price)
        );
      else return parseFloat(x.free) + parseFloat(x.locked);
    });

    this.chartData.datasets[0].backgroundColor = this.generateColors(
      newVal.length
    );
    this.lineChartData.datasets[0].data = this.generateFakeSnapshots();
  }
  public generateColors(assetsLength: number): Array<any> {
    let arr: Array<any> = [];
    for (let i = 0; i < assetsLength; i++) {
      let color = this.doughnutColors[i];
      arr.push(color);
    }
    return arr;
  }

  public setAssets() {
    this.assets = this.selectedAccount.assets;
  }

  public chartData = {
    hoverBorderWidth: 0,
    labels: ["teasdf", "Red", "Blue", "Purple", "yellow"],
    datasets: [
      {
        borderWidth: "1.5",
        cutout: 20,
        label: "Data One",
        backgroundColor: ["#41B883", "#E46651", "#00D8FF"],
        data: [1],
      },
    ],
  };

  public lineChartData = {
    labels: this.generateDays(),
    datasets: [
      {
        pointRadius: 1,
        borderWidth: 4,
        label: "USDT over time",
        fill: false,
        pointBackgroundColor: "#f0943d",
        borderColor: "#f0943d",
        data: [1],
      },
    ],
  };
  public lineChartOptions = {
    elements: {
      line: {
        tension: 0,
      },
    },
  };
}
</script>

<style scoped>
#doughnut {
  max-width: 350px;
}
.lineChartContainer {
  height: 90vh;
  border-radius: 20px;
  background: #ebebeb;
  margin: 20px;
}
.doughnutContainer {
  height: 70vh;
  border-radius: 20px;
  align-items: center;
  justify-content: center;
  display: inline-flex;
  background: #ebebeb;
  padding: 50px;
  margin-top: 20px;
}
</style>