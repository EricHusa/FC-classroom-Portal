<template>
  <div>
    <b-row>
      <b-col sm="6">
        <b-jumbotron header="View the experiment!">
          <b-img
            v-bind:src="image_url_with_ts"
            fluid
            alt="No image to show"
            class="zoom"
          /><br />
          <hr />
          <label for="static-image-datepicker">Choose a date</label>
          <b-form-datepicker
            id="static-image-datepicker"
            today-button
            reset-button
            close-button
            locale="en"
          ></b-form-datepicker>
          <b-btn
            @click="fetchImage"
            variant="success"
            dark
            class="mb-2 image-reset"
            v-b-popover.hover.top="'Images are typically updated every hour'"
            >Get newest image</b-btn
          >
        </b-jumbotron>
      </b-col>

      <b-col sm="6">
        <b-overlay show rounded="sm">
          <b-jumbotron header="Or make a video!">
            <b-img
              v-bind:src="image_url_with_ts"
              fluid
              alt="No video to show"
              class="zoom"
            /><br />
            <hr />
            <b-row>
              <b-col sm="6">
                <label for="gif-start-datepicker">Start date</label>
                <b-form-datepicker
                  id="gif-start-datepicker"
                  today-button
                  reset-button
                  close-button
                  locale="en"
                ></b-form-datepicker>
              </b-col>
              <b-col sm="6">
                <label for="gif-end-datepicker">End date</label>
                <b-form-datepicker
                  id="gif-end-datepicker"
                  today-button
                  reset-button
                  close-button
                  locale="en"
                ></b-form-datepicker>
              </b-col>
            </b-row>
            <b-btn
              @click="fetchImage"
              variant="success"
              dark
              class="mb-2 image-reset"
              >Create</b-btn
            >
            <b-btn
              @click="fetchImage"
              variant="danger"
              dark
              class="mb-2 image-reset"
              >Clear</b-btn
            >
          </b-jumbotron>
          <template v-slot:overlay>
            <div class="text-center">
              <b-icon icon="blank" font-scale="3"></b-icon>
              <div id="cancel-label"><h3>New feature coming soon</h3></div>
            </div>
          </template>
        </b-overlay>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Fop from "../constants/Fop.ts";
export default {
  name: "ImageViewer",
  methods: {
    fetchImage: function(ts = new Date().getTime()) {
      this.image_url_with_ts = this.imageBase + "?ts=" + ts;
    }
  },
  beforeMount: function() {
    this.imageBase = Fop.api + "/image/" + this.$store.state.device;
    this.image_url_with_ts = this.imageBase + "?ts=" + new Date().getTime();
  }
};
</script>

<style scoped>
h2 {
  text-decoration: underline;
}

.image-reset {
  margin: 0.5em;
}

.zoom {
  transition: transform 0.2s;
  border-style: ridge;
}

/*.zoom:hover {*/
/*  transform: scale(1.5);*/
/*}*/
</style>
