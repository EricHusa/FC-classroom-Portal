export default {
    climate_file: {
id: "pfc_stable_grow",
  format: "flexformat",
  version: "1.0",
  seeds: ["basil", "http://www.edenbrothers.com/store/sweet_basil_seeds.html"],
  plant_type: ["basil", "warm"],
  certified_by: ["Peter Konjoian"],
  optimization: ["general"],
  author: "Jake Rye",
  rating: 0,
  downloads: 0,
  date_created: "2017-08-10",
  phases: [
    { name: "growth",
      cycles: 28,
      time_units: "hours",
      step:
        { air_temperature: [
            {start_time: 0, end_time: 22, value: 25},
            {start_time: 22, end_time: 23, value: 18}],
          light_intensity: [
            {start_time: 0, end_time: 22, value: 1},
            {start_time: 22, end_time: 23, value: 0}],
          air_flush: [
            {start_time: 0, end_time: 22, interval: 15, duration:2}]
      }
    }
  ]
}
}