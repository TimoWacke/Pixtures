<template>
  <div class="container">
    <br>
    <h1>CityCanvas</h1>
    <img v-for="url in imageUrls" :src="url" v-bind:key="url" />
    <a href="/create">
      <button>Try it yourself</button>
    </a>
  </div>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@1,900&display=swap");
</style>

<script>
import axios from "axios";
import vars from "../assets/vars";

export default {
  name: "Landing-Site",
  data() {
    return {
      imageUrls: []
    }
  },
  mounted() {
    try {
      let me = this;
      axios
        .get(vars.pixtures + "/api/v1/artpiece/")
        .then((response) => {
          me.imageUrls = response.data;
        });
    } catch {
      this.coordinates = this.suggestedCities[0];
    }
    setTimeout(() => this.reloadScale(), 2500);
  },
  methods: {

  },
  components: {},
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@1,900&display=swap");
</style>