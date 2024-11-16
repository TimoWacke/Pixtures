<template>
  <div class="sign-page">
    <div class="container">
      <h1>Reset Password</h1>
      <div class="card">
        <div>
          <p>Enter a new Password</p>
          <p>for {{ data.email }}</p>
        </div>
        <input
          type="password"
          v-model="data.password"
          placeholder="1safePa$§word"
        />
        <input type="password" v-model="rppass" placeholder="1safePa$§word" />
        <div>
          <p id="error">{{ error }}</p>
        </div>
        <button id="send" @click="reset()">login</button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.content {
  margin: 0;
}
#error {
  color: #ff0000;
}
</style>

<script>
import axios from "axios";
import router from "../router";
import vars from "../assets/vars";

export default {
  name: "Reset-Site",
  data() {
    return {
      data: {
        code: "",
        id: "",
        email: "",
        password: "",
      },
      error: "",
      rppass: "",
    };
  },
  mounted() {
    const me = this;
    var re_id = /&(\S+)$/;
    var re_code = /\?(\S+)&/;
    this.data.id = window.location.href.match(re_id)[1];
    this.data.code = window.location.href.match(re_code)[1];
    axios
      .get(vars.url + "/user/" + this.data.id)
      .then((response) => {
        me.data.email = response.data;
      })
      .catch(() => {
        me.error = "no user found or server error";
      });
  },
  methods: {
    reset: function () {
      if (this.rppass != this.data.password) {
        this.error = "passwords do not match";
        return;
      }
      const me = this;
      console.log("axios get to /user/", this.data);

      axios
        .post(vars.url + "/new_pswd", this.data)
        .then(function (response) {
          if (response.data == "success") {
            router.push({name:"Login"});
            return;
          }
          me.error = response.data;
          if (response.data.includes("password")) {
            document.getElementById("error").attribute = "block";
          }
        })
        .catch(function () {
          me.error = "server error";
        });
    },
  },
  components: {},
};
</script>