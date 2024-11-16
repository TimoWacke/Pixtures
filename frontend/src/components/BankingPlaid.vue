<template>
  <div class="project fat">
    <h2>Check your Bank Account</h2>
    <p>{{ plaid_errorcorde }}</p>
    <PlaidLink
      v-if="link_key"
      clientName="FinancePictures"
      env="development"
      :link_token="link_key"
      :products="['auth', 'transactions']"
      :onSuccess="exchange"
      :onLoad="nothing"
      :onEvent="nothing"
      :onExit="nothing"
    >
      <button>Open Link Slot</button>
    </PlaidLink>
    <br />
    <div v-if="Object.keys(bankData).length !== 0">
      <div
        id="chart-1"
        class="chart"
        v-for="account in bankData"
        :key="account.account_id"
      >
        <line-chart :data="account" :colors="['#0f476f']" suffix=" €"></line-chart>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import VueCookie from "vue-cookies";
import axios from "axios";
import vars from "@/assets/vars";
import PlaidLink from "vue-plaid-link2";
import App from "@/App.vue";

export default {
  name: "Admin-Site",
  props: ["timeline"],
  data() {
    return {
      link_key: null,
      plaid_errorcorde: "",
      bankData: {},
      startDate: new Date(this.timeline),
    };
  },
  async mounted() {
    await this.initBankData(); // if no plaid_token set plaid_token or link_key
    if (VueCookie.get("plaid_token"))
      this.getBankData(VueCookie.get("plaid_token"));
  },
  methods: {
    async initBankData() {
      if (!App.store["user"].plaidaccess) {
        if (!VueCookie.get("plaid_token")) {
          await axios
            .get(vars.finance + "/create-link-token")
            .then((response) => {
              this.link_key = response.data.link_token;
              return;
            });
        }
        App.store["user"].plaidaccess = VueCookie.get("plaid_token");
        await axios.post(vars.url + "/cms/update", {
          token: VueCookie.get("session_token"),
          id: App.store["user"]._id,
          doc: App.store["user"],
        });
      } else if (!VueCookie.get("plaid_token")) {
        VueCookie.set("plaid_token", App.store["user"].plaidaccess);
      }
    },
    getBankData(accessToken) {
      var me = this;
      axios
        .post(vars.finance + "/transactions", {
          access_token: accessToken,
          startDate: me.startDate,
        })
        .then((response) => {
          console.log(response.data);
          if (response.data.error) {
            if (response.data.error.error_code == "ITEM_LOGIN_REQUIRED") {
              VueCookie.remove("plaid_token");
              App.store["user"].plaidaccess = null;
              me.initBankData();
              return;
            } else {
              me.plaid_errorcorde = response.data.error;
            }
          }

          var accounts = {};
          var balances = {};
          for (var i in response.data.accounts) {
            accounts[response.data.accounts[i].account_id] = {};
            balances[response.data.accounts[i].account_id] =
              response.data.accounts[i].balances.current;
          }
          for (var j in response.data.transactions) {
            if (
              !accounts[response.data.transactions[j].account_id][
                response.data.transactions[j].date
              ]
            ) {
              accounts[response.data.transactions[j].account_id][
                response.data.transactions[j].date
              ] =
                Math.round(
                  balances[response.data.transactions[j].account_id] * 100
                ) / 100;
            }
            balances[response.data.transactions[j].account_id] +=
              response.data.transactions[j].amount;
          }
          this.bankData = accounts;
        });
    },
    nothing: function () {},
    exchange: function (publicToken, metadata) {
      console.log("public token:", publicToken);
      console.log("metadata:", metadata);
      console.log(vars.finance);
      axios
        .post(vars.finance + "/token-exchange", {
          public_token: publicToken,
        })
        .then(async (res) => {
          if (res.data.access_token) {
            this.getBankData(res.data.access_token);
            VueCookie.set("plaid_token", res.data.access_token);
          } else {
            VueCookie.remove("plaid_token");
          }
        });
    },
  },
  components: {
    PlaidLink,
  },
};
</script>