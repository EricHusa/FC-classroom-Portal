<template>
  <div id="chart">
    <b-row sm="12">
      <b-col sm="2"></b-col>
      <b-col sm="3">
        <b-form-group label="Start date">
          <b-form-datepicker v-model="startDate" :max="today" locale="en"></b-form-datepicker>
        </b-form-group>
      </b-col>
      <b-col sm="2"></b-col>
      <b-col sm="3">
        <b-form-group label="End date">
          <b-form-datepicker v-model="endDate" :max="today" locale="en"></b-form-datepicker>
        </b-form-group>
      </b-col>
      <b-col sm="2"></b-col>
    </b-row>

    <apexchart
      type="area"
      height="350"
      :options="chartOptions"
      :series="series"
    ></apexchart>
    <br/>
    <b-button @click="reloadData">Reload Chart</b-button>
    <hr/>
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
      today: null,
      startDate: null,
      endDate: null,
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
            opacityFrom: 1,
            opacityTo: 0.25,
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
    this.today = api.getToday(new Date());
    this.startDate = this.today;
    this.endDate = this.today;
    this.setChart();
  },
  methods: {
    setChart(){
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
    },
    reloadData(){
      api.pullCSV(this.startDate, this.endDate);
      // this.$emit("refresh");
      this.setChart();
    }
  }
};
</script>

<style scoped></style>
