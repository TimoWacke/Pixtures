<template>
  <div id="dashboard">
    <div id="dashboard-div" class="hiddendash">
      <div class="sideboard column gradient">
        <VerticalIntegrations variant="dark" />
        <div id="sections">
          <div v-for="sect in features" :key="sect">
            <a            
              :href="
                '/' + (sect.toLowerCase() != 'paper' ? sect.toLowerCase() : '')
              "
              :class="'/' + encodeURIComponent(sect.toLowerCase()) == current || sect.toLowerCase() == 'paper' && current == '/' ? 'current' : ''"
              :id="'/' + encodeURIComponent(sect.toLowerCase()) == current || sect.toLowerCase() == 'paper' && current == '/' ? 'current' : ''"
              >{{ sect }}</a
            >
          </div>
        </div>
      </div>
      <SignOut id="signout" />
    </div>
    <div @click="showDashboard()" id="menubtn">
      <hr id="line1" />
      <hr id="line2" />
      <hr id="line3" />
    </div>
  </div>
</template>

<script>
import SignOut from "@/components/SignOut.vue";
import VerticalIntegrations from "@/components/VerticalIntegrations.vue";
import App from "@/App.vue";

export default {
  name: "dashboard-item",
  data() {
    return {
      features: App.store["user"].features,
      current: "",
    };
  },
  mounted() {
    this.current = window.location.pathname;
  },
  methods: {
    showDashboard() {
      document.getElementById("dashboard-div").classList.toggle("hiddendash");
      document.getElementById("menubtn").classList.toggle("open");
    },
  },
  components: {
    SignOut,
    VerticalIntegrations,
  },
};
</script>

<style lang="scss">
.sideboard {
  width: calc(200px + 8vw);
  padding: 45px 2vw;
  height: calc(100vh - 90px);
  font-size: 20px;
  position: sticky;
  top: 0;
  @media only screen and (max-width: 1200px) {
    font-size: 16px;
    a {
      font-size: 22px;
    }
  }
}
#sections {
  display: flex;
  flex-direction: column;
  height: 100%;
  margin: 100px 30px;
  div {
    margin: 2vh 0;
    a {
      font-size: 24px;
      text-decoration: none;
      &:hover,
      &.current {
        text-decoration: underline;
      }
    }
  }
}

#dashboard-div {
  box-shadow: 0px 0px 3px 3px #bbbb;
  position: fixed;
  z-index: 4;
}

SignOut {
  position: fixed;
}

#content {
  margin-left: calc(200px + 8vw + 4vw) !important;
}

#menubtn {
  hr {
    background: #0f476f;
    height: 5px;
    border-radius: 2.5px;
    width: 35px;
    outline: none;
    border: none;
    transition: all 0.25s ease;
    margin: 5px;
  }
  position: fixed;
  z-index: 5;
  top: 45px;
  right: 30px;

  &.open {
    hr {
      background: #fff;
    }
  }
}
#menubtn.open #line1 {
  transform: translateY(10px) rotate(45deg);
  background: #fff;
}

#menubtn.open #line2 {
  display: none;
}

#menubtn.open #line3 {
  transform: rotate(135deg);
}
@media only screen and (min-width: 1200px) {
  #menubtn {
    display: none;
  }
}
@media only screen and (max-width: 1200px) {
  #dashboard-div {
    &.hiddendash {
      display: none;
    }
    width: 100vw;
  }
  #content {
    margin-left: 0 !important;
  }
  #banner {
    max-width: 200px;
  }

  #signout {
    a {
      color: #fff;
    }
    button {
      background-color: #fff;
      color: #0f476f;
    }
  }

  .sideboard {
    width: calc(100% - 4vw);
  }
}
</style>