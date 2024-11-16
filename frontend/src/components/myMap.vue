<template>
  <div id="GMap">
    <GMapMap :center="center" :zoom="zoom" :options="options"> </GMapMap>
  </div>
</template>
  
<script>
export default {
  name: "GMap",
  data() {
    return {
      center: {},
      zoom: 0,
      options: {
        zoomControl: false,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false,
        disableDefaultUi: false,
        mapId: "6b1f31442f4ffc3b", //here comes your map id
      },
    };
  },
  props: ["coordinates"],
  mounted() {
    this.center = {lat: this.coordinates.lat, lng: this.coordinates.lng};
    this.zoom = this.coordinates.zm;
  },
  methods: {},
};
</script>
  <style lang="scss">
.vue-map-container {
  width: 100%;
  height: 100%;
}
</style>
  