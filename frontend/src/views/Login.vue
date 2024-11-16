<template>
  <div class="sign-page">
    <div class="container tight">
      <VerticalIntegrations id="vlogo" variant="light" />

      <h1>Login</h1>
      <div class="card">
        <input type="text" v-model="user.email" placeholder="email" />
        <input type="password" v-model="user.password" placeholder="password" />
        <input
          type="text"
          placeholder="token"
          v-model="user.token"
          style="display: none"
          id="token"
        />
        <div class="hori zontal d spce">
          <div class="small">
            <p id="error">{{ error }}</p>
            <a style="display: none" @click="reset()" id="reset"
              >reset password</a
            >
          </div>
          <button id="send" @click="postLogin()">shape your brand</button>
        </div>
      </div>
      <br />
      <p class="mobile-white">
        You don't have an Account?
        <a class="mobile-white" href="/signup">Sign up</a>
        or use what you're familiar with:
      </p>

      <br />
      <button id="g-signin" @click="googleSignIn()" class="hori zontal shadow">
        <svg
          width="64px"
          height="64px"
          viewBox="0 0 46 46"
          version="1.1"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
          xmlns:sketch="http://www.bohemiancoding.com/sketch/ns"
        >
          <g
            id="Google-Button"
            stroke="none"
            stroke-width="1"
            fill="none"
            fill-rule="evenodd"
            sketch:type="MSPage"
          >
            <g id="button-bg">
              <use
                fill="#FFFFFF"
                fill-rule="evenodd"
                sketch:type="MSShapeGroup"
                xlink:href="#path-2"
              ></use>
              <use fill="none" xlink:href="#path-2"></use>
              <use fill="none" xlink:href="#path-2"></use>
              <use fill="none" xlink:href="#path-2"></use>
            </g>
            <g
              id="logo_googleg_48dp"
              sketch:type="MSLayerGroup"
              transform="translate(15.000000, 15.000000)"
            >
              <path
                d="M17.64,9.20454545 C17.64,8.56636364 17.5827273,7.95272727 17.4763636,7.36363636 L9,7.36363636 L9,10.845 L13.8436364,10.845 C13.635,11.97 13.0009091,12.9231818 12.0477273,13.5613636 L12.0477273,15.8195455 L14.9563636,15.8195455 C16.6581818,14.2527273 17.64,11.9454545 17.64,9.20454545 L17.64,9.20454545 Z"
                id="Shape"
                fill="#4285F4"
                sketch:type="MSShapeGroup"
              ></path>
              <path
                d="M9,18 C11.43,18 13.4672727,17.1940909 14.9563636,15.8195455 L12.0477273,13.5613636 C11.2418182,14.1013636 10.2109091,14.4204545 9,14.4204545 C6.65590909,14.4204545 4.67181818,12.8372727 3.96409091,10.71 L0.957272727,10.71 L0.957272727,13.0418182 C2.43818182,15.9831818 5.48181818,18 9,18 L9,18 Z"
                id="Shape"
                fill="#34A853"
                sketch:type="MSShapeGroup"
              ></path>
              <path
                d="M3.96409091,10.71 C3.78409091,10.17 3.68181818,9.59318182 3.68181818,9 C3.68181818,8.40681818 3.78409091,7.83 3.96409091,7.29 L3.96409091,4.95818182 L0.957272727,4.95818182 C0.347727273,6.17318182 0,7.54772727 0,9 C0,10.4522727 0.347727273,11.8268182 0.957272727,13.0418182 L3.96409091,10.71 L3.96409091,10.71 Z"
                id="Shape"
                fill="#FBBC05"
                sketch:type="MSShapeGroup"
              ></path>
              <path
                d="M9,3.57954545 C10.3213636,3.57954545 11.5077273,4.03363636 12.4404545,4.92545455 L15.0218182,2.34409091 C13.4631818,0.891818182 11.4259091,0 9,0 C5.48181818,0 2.43818182,2.01681818 0.957272727,4.95818182 L3.96409091,7.29 C4.67181818,5.16272727 6.65590909,3.57954545 9,3.57954545 L9,3.57954545 Z"
                id="Shape"
                fill="#EA4335"
                sketch:type="MSShapeGroup"
              ></path>
              <path
                d="M0,0 L18,0 L18,18 L0,18 L0,0 Z"
                id="Shape"
                sketch:type="MSShapeGroup"
              ></path>
            </g>
            <g id="handles_square" sketch:type="MSLayerGroup"></g>
          </g>
        </svg>
        <p>Sign in with Google</p>
      </button>
    </div>
    <div id="frame">
      <img id="footer-img" src="../assets/brandung.jpg" alt="" />
    </div>
  </div>
</template>



<script>
import axios from "axios";
import router from "../router";
import vars from "../assets/vars";
import VueCookie from "vue-cookies";
import VerticalIntegrations from "@/components/VerticalIntegrations.vue";

export default {
  name: "Login-Site",
  data() {
    return {
      user: {
        name: "",
        email: "",
        password: "",
        token: "",
      },
      error: "",
    };
  },
  methods: {
    async googleSignIn() {
      const googleUser = await this.$gAuth.signIn();
      if (!googleUser) {
        return null;
      }
      this.user.token = googleUser.getAuthResponse().id_token;
      this.postLogin();
    },
    postLogin() {
      this.error = "";
      const me = this;
      axios
        .post(vars.url + "/login", this.user)
        .then(function (response) {
          if (response.data.msg == "success") {
            VueCookie.set("session_token", response.data.token);
            //as the token has been set it will redirect to Home anyways
            // -> but index.js now can bring the admin to admin page direclty
            router.push({ name: "SignUp" });
            return;
          }
          if (response.data.msg.includes("password")) {
            document.getElementById("reset").style.display = "block";
            return;
          }
          me.error = response.data.msg;
        })
        .catch(function () {
          me.error = "server error";
        });
    },
    reset() {
      const me = this;
      axios
        .get(vars.url + "/reset/" + this.user.email)
        .then(function (response) {
          if (response.data != "success") {
            me.error = response.data;
            return;
          }
          (document.getElementById("content").innerHTML =
            "a password reset link was sent to"),
            me.user.email;
        })
        .catch(function () {
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
#error {
  color: #ff0000;
}

a {
  text-decoration: underline;
  cursor: pointer;
}

#g-signin {
  font-family: "Nunito", "Roboto";
  font-weight: 750;
  font-size: 16px;
  color: #444;
  background: #fff;
  padding: 0 20px;
  svg {
    margin: -12px 0 -10px -20px;
  }
  &:hover {
    transform: translateY(-2px);
  }

  @media only screen and (max-width: 600px) {
    width: 100%;
    p {
      width: 100%;
      text-align: center;
    }
  }
}

@media only screen and (max-width: 700px) {
  #vlogo {
    margin: 10% 0 20% auto;
  }

  .mobile-white {
    margin-top: 100px;
  }
}

#send {
  margin-left: auto;
}
</style>