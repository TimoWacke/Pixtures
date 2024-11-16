<template>
  <div class="sign-page">
    <div class="container">
      <div class="card">
        <div>
          <h1>{{ title }}</h1>
          <p>{{ message }}</p>
        </div>
        <p>you will be redirected...</p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
#error {
  color: #ff0000;
}
.card {
  * {
    color: #fff;
  }
  div {
    align-self: flex-start;
  }
}
</style>

<script>
import axios from "axios";
import router from "../router";
import vars from "../assets/vars";
import VueCookie from "vue-cookies";

export default {
  name: "Flyby-Site",
  data() {
    return {
      title: "",
      link: "",
      message: "",
      urll: "",
    };
  },
  mounted() {
    const me = this;
    var re_title = /link\?(\S+)&/;
    var re_link = /link\?(\S+)$/;
    this.urll = window.location.href
    this.title = this.urll.match(re_title)[1];
    this.link = this.urll.match(re_link)[1].replace("&", "/");
    axios
      .get(vars.url + "/" + this.link)
      .then((response) => {
        me.message = response.data.msg + "!";
        if (response.data.cookie) {
          for (var key in response.data.cookie) {
            VueCookie.set(key, response.data.cookie[key]);
          }
        }
        setTimeout(() => {
          me.message = "3 seconds.."
          router.push({ name: "Home" });
        }, 3000);
      })
      .catch(() => {
        me.error = "sorry something went wrong";
      });
  },
  methods: {},
  components: {},
};
</script>