<template>
  <div class="hori spce">
    <button
      v-for="rangeName in Object.keys(timelineRanges)"
      :key="rangeName"
      :class="rangeName == currentRange ? '' : 'invert'"
      style="margin-right: 5px"
      @click="setTimeline(rangeName)"
    >
      {{ rangeName }}
    </button>
  </div>
</template>

<script>
export default {
  props: ["default"],
  data() {
    return {
      timelineRanges: {
        "24 hours": 1,
        "7 days": 7,
        "30 days": 30,
        "90 days": 90,
        "1 year": 365.25,
      },
      currentRange: false,
    };
  },
  async mounted() {
    // for all ranges, if it matches the selected range, set it to currentRange interval set current as it
    for (let range in this.timelineRanges) {
      if (this.timelineRanges[range] == this.default) {
        this.currentRange = range;
      }
    }
  },
  methods: {
    setTimeline(rangeName) {
      this.currentRange = rangeName;
      this.$emit("setTimeline", this.timelineRanges[rangeName]);
    },
  },
};
</script>