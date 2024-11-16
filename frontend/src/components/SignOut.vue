<template>
  <div id="signout" class="horizontal">
    <a style="text-decoration: none" href="/profile">
      {{ aps["user"].edit.forename }} {{ aps["user"].edit.surname }}
    </a>
    <button @click="signOut()">Sign out</button>
  </div>
</template>

<script>
import router from "@/router";
import VueCookie from "vue-cookies";
import axios from "axios";
import vars from "@/assets/vars";
import App from "@/App.vue";

export default {
  name: "SignOut-item",
  data() {
    return {
      aps: App.store,
    };
  },
  methods: {
    async signOut() {
      var admin_token = VueCookie.get("admin_token");
      if (admin_token) {
        await axios
          .post(vars.url + "/super/token", {
            adminToken: admin_token,
          })
          .then((response) => {
            VueCookie.set("session_token", response.data);
            VueCookie.remove("admin_token");
            router.push({ name: "Admin" });
          })
          .catch((err) => {
            VueCookie.remove("admin_token");
            console.log("error at signout from admin visit", err);
          });
      } else {
        await axios
          .post(vars.url + "/signout", {
            token: VueCookie.get("session_token"),
          })
          .then(async () => {
            VueCookie.remove("session_token");
            try {
              await this.$gAuth.signOut();
              this.isSignIn = this.$gAuth.isAuthorized;
            } catch (error) {
              console.error(error);
            }
            router.push({ name: "Login" });
          });
      }
    },
  },
  components: {},
};
</script>
<style lang="scss">
#signout {
  display: flex;
  align-items: center;
  font-weight: 600;
  button {
    margin-left: 1vw;
    width: 100px;
  }
  a:hover {
    transform: translateY(2px);
  }

  position: fixed;
  top: 45px;
  right: 70px;

  @media only screen and (max-width: 1200px) {
    right: 120px;
  }
  @media only screen and (max-width: 700px) {
    right: auto;
    left: 40px;
  }
}
</style>
