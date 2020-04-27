<template>
  <div id="chart">
    <apexchart
      type="area"
      height="350"
      :options="chartOptions"
      :series="series"
    ></apexchart>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import api from "../api/index.js";
export default {
  name: "ChartViewer",
  components: { apexchart: VueApexCharts },
  props: {
      dataName: String,
      xDataUnit: String
  },
  data() {
    return {
      series: [
        {
          name: "",
          data: null
        }
      ],
      chartOptions: {
        chart: {
          type: "area",
          stacked: false,
          height: 350,
          zoom: {
            type: "x",
            enabled: true,
            autoScaleYaxis: true
          },
          toolbar: {
            autoSelected: "zoom"
          }
        },
        dataLabels: {
          enabled: false
        },
        markers: {
          size: 0
        },
        title: {
          text: "Chart Data",
          align: "center"
        },
        fill: {
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            inverseColors: false,
            opacityFrom: 0.5,
            opacityTo: 0,
            stops: [0, 90, 100]
          }
        },
        yaxis: {
          labels: {
            formatter: function(val) {
              return val.toFixed(1);
            }
          }
        },
        xaxis: {
          type: "datetime"
        },
        tooltip: {
          shared: false,
          y: {
            formatter: function(val) {
              return parseFloat(val).toFixed(2);
            }
          }
        }
      }
    };
  },
  beforeMount() {
    let chartData = api.getDataArrays(this.dataName);
    this.series[0].data = chartData.data;
    this.series[0].name = chartData.name;
    this.chartOptions.title.text = chartData.name + " (" + chartData.units + ")";
    this.chartOptions.yaxis.labels.formatter = (value) => {
      return value.toFixed(1) + " " + this.xDataUnit;
    };
    this.chartOptions.tooltip.y.formatter = (value) => {
      return value.toFixed(1) + " " + this.xDataUnit;
    };
  }
};
</script>

<style scoped></style>
