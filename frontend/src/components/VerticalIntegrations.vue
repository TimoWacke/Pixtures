<template>
  <div>
    <div id="banner" class="hori zontal mobile-cmpr">
      <img id="logo-d" alt="logo" src="../assets/logo.svg" class="svg" />
      <img
        style="display: none"
        id="logo-l"
        alt="logo"
        src="../assets/lightlogo.svg"
        class="svg"
      />
      <hr class="vertical" />
      <p id="title">vertical integrations</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "logo-item",
  props: ["variant"],
  data() {
    return {};
  },
  mounted() {
    if (this.variant == "light") {
      document.getElementById("banner").classList.add(this.variant);
      document.getElementById("banner").classList.remove("dark");
      document.getElementById("logo-l").style = "display: block";
      document.getElementById("logo-d").style = "display: none";
    } else {
      document.getElementById("banner").classList.add(this.variant);
      document.getElementById("banner").classList.remove("light");
      document.getElementById("logo-l").style = "display: none";
      document.getElementById("logo-d").style = "display: block";
    }
  },
};
</script>


<style lang="scss">
.light {
  hr {
    background: #000;
  }
  #title {
    color: #000 !important;
  }
}
.svg {
  width: calc(20px + 25%);
  @media only screen and (max-width: 1200px) {
    width: 90px;
  }
}

#title {
  max-width: 42%;
  letter-spacing: 0.21px;
  font-size: 1em;
  text-align: left;
  margin-left: 8px;
}

#dashboard #banner {
  @media only screen and (min-width: 700px) {
    padding: 0px 10%;

    justify-content: space-around;
    &.light {
      justify-content: space-between;
    }
  }
  @media only screen and (max-width: 700px) {
    transform: translatey(80vh);
  }
}
</style>
