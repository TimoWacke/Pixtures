<template>
  <div class="sign-page">
    <div class="container tight" :key="keyCode">
      <VerticalIntegrations id="vlogo" variant="light" />

      <div class="headers">
        <h1>Sign Up</h1>
        <h2>for the modern way of branding</h2>
      </div>
      <div class="card" id="card">
        <h3>Enter your Details</h3>
        <div v-if="ename">
          <p>empfohlen von</p>
          <p>{{ ename }}</p>
        </div>
        <div class="hori zontal spce mobile-cmpr">
          <input type="text" v-model="user.forename" placeholder="Forename" />
          <hr class="hidden" />
          <input type="text" v-model="user.surname" placeholder="Surname" />
        </div>
        <input
          type="text"
          v-model="user.email"
          placeholder="musk@neuralink.com"
        />
        <input
          type="password"
          v-model="user.password"
          placeholder="1safePa$§word"
        />
        <input type="password" v-model="rppass" placeholder="1safePa$§word" />
        <div class="small">
          <p id="error">{{ error }}</p>
          <p>
            I hereby confirm that the above indications are true and complete.
          </p>
          <p>I accept the <a href="/agb">terms and conditions</a></p>
        </div>
        <button id="send" class="right" @click="postRegister()">
          register
        </button>
      </div>
      <p id="gtl">go to <a class="shadow" href="/login">login</a></p>
    </div>
    <div id="frame">
      <img id="footer-img" src="../assets/brandung.jpg" alt="" />
    </div>
  </div>
</template>



<script>
import axios from "axios";
import vars from "../assets/vars";
import VerticalIntegrations from "@/components/VerticalIntegrations.vue";

export default {
  name: "Register-Site",
  data() {
    return {
      user: {
        forename: "",
        surname: "",
        email: "",
        password: "",
      },
      rppass: "",
      error: "",
      ename: null,
      keyCode: 0,
    };
  },
  mounted() {
    var match = window.location.href.match(/referral=(\S+)$/);
    if (match && match[1]) {
      this.user["empfohlen"] = match[1];
      axios.get(vars.url + "/user/" + this.user.empfohlen).then((response) => {
        this.ename = response.data;
      });
    } else {
      console.log("lost");
    }
  },
  methods: {
    postRegister() {
      this.error = "";
      if (this.rppass != this.user.password) {
        this.error = "passwords do not match";
        return;
      }
      var minlength = 6
      if (this.user.password.length < minlength) {
        this.error = `please choose a password with at least ${minlength} characters`;
        this.keyCode += 1;
        return;
      }

      const me = this;
      axios
        .post(vars.url + "/register", this.user)
        .then((response) => {
          if (response.data == "success") {
            document.getElementById("card").innerHTML =
              "Click on the link we sent to your e-mail address for verification which logs you in right away.";
          }
          me.error = response.data;
          return;
        })
        .catch((response) => {
          console.log(response.data);
          me.error = "server error";
        });
    },
  },
  components: {
    VerticalIntegrations,
  },
};
</script>

<style lang="scss" scoped>
#gtl {
  font-weight: 600;
  @media only screen and (max-width: 468px) {
    color: #fff;
  }
  a {
    background: #9994;
    &:hover {
      opacity: 100%;
      background: #ffffffff;
    }
    cursor: pointer;
    color: #0f476f;
    text-decoration: none;
    padding: 4px 15px;
    border-radius: 3px;
    margin-left: 5px;
  }
}
h3 {
  margin-top: 5px;
  font-size: 24px;
}

input {
  width: calc(100% - 20px) !important;
}

.app {
  display: none;
}
</style>

