<template>
  <div class="hori">
    <Dashboard />
    <div v-if="done" id="content" class="site">
      <h1>
        Welcome {{ aps["user"].edit.forename }} {{ aps["user"].edit.surname }}
      </h1>
      <h3>manage your personal information here</h3>
      <br />
      <Saver class="home" :toserve="contents" />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

//import axios from "axios";
//import vars from "@/assets/vars";
import App from "@/App.vue";
import Dashboard from "@/components/Dashboard.vue";
import Saver from "@/components/Saver.vue";
export default {
  name: "Home-Site",
  data() {
    return {
      contents: [],
      aps: App.store,
      done: false,
    };
  },
  components: {
    Dashboard,
    Saver,
  },
  mounted() {
    this.contents.push(App.store["user"]);
    this.done = true;
  },
};
</script>

<style lang="scss">
#save {
  width: 100px;
  margin-bottom: -30px;
}
</style>
