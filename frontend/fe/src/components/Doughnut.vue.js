import { Doughnut, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins

export default {
  extends: Doughnut,
  mixins: [reactiveProp],
  props: ['chartData'],
//   watch: {
//     'chartData' (to, from) {
//       this.renderChart(this.chartData, this.options)
//     },

  mounted () {
      
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
    this.options = Object.assign({}, this.options, { cutoutPercentage: 60 });
    this.renderChart(this.chartData, this.options);
  }
}