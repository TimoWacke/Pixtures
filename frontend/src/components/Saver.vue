<template>
  <div v-if="done">
    <div v-for="item in toserve" :key="item.name">
      <Content
        v-if="((!item.invisible || admin) && !nodisplay)"
        :class="item.invisible ? 'invisible' : ''"
        :item="structured[item._id]"
        :prjid="item.project"
        :path="''"
        @refresh="forceUpdate()"
        :id="item._id"
      />
      <div v-if="item.edit" :id="'saver-' + item._id" class="saver">
        <br />
        <div>
          <div class="crl" id="cr1"></div>
          <div class="crl" id="cr2"></div>
          <div class="crl" id="cr3"></div>
        </div>
      </div>
      <br />
    </div>
  </div>
</template>

<script>
import VueCookie from "vue-cookies";
import axios from "axios";
import vars from "@/assets/vars";
import Content from "@/components/Content.vue";
//import { structNode } from "@/config/utils";

export default {
  name: "saver-item",
  data() {
    return {
      structured: {},
      unsaved: {},
      done: false,
    };
  },
  props: ["toserve", "admin", "nodisplay"],
  async mounted() {
    //for content in toserve (contents)
    for (var i in this.toserve) {
      this.structured[this.toserve[i]._id] = this.toserve[i];
      this.unsaved[this.toserve[i]._id] = {};
      if (this.toserve[i].edit) {
        this.watch(i, this.toserve[i]._id, 300); //watches this.unsaved['user'] for example
      }
    }
    this.done = true;
  },
  methods: {
    async save(i, use) {
      console.log("saving:", this.toserve[i]);
      await axios
        .post(vars.url + "/cms/update", {
          token: VueCookie.get("session_token"),
          id: use,
          doc: (this.nodisplay || this.admin) ? this.toserve[i] : {edit: this.toserve[i].edit},
        })
        .then((response) => {
          console.log(response.data);
          if (response.data == "success") {
            this.unsaved[use] = {};
            this.$forceUpdate();
          }
        })
        .catch((err) => console.log(err));
    },
    watch(i, use, speed) {
      var initial = JSON.stringify(this.toserve[i]);
      var before = JSON.stringify(this.toserve[i]);
      var count = 0;
      var constant = 0;
      setInterval(async () => {
        if (before != JSON.stringify(this.toserve[i])) {
          before = JSON.stringify(this.toserve[i]);
          count += 1;
          constant = 0;
          document.getElementById("saver-" + use).classList.add("sync");
        } else if (initial == JSON.stringify(this.toserve[i])) {
          before = initial;
          count = 0;
          constant = 0;
          try {
            document.getElementById("saver-" + use).classList.remove("sync");
          } catch (e) {
            console.log("error with use:", use);
          }
        }
        if (count > 0 && constant > 6) {
          await this.save(i, use);
          document.getElementById("saver-" + use).classList.add("save");
          setTimeout(() => {
            document.getElementById("saver-" + use).classList.remove("sync");
            document.getElementById("saver-" + use).classList.remove("save");
          }, 1000);

          initial = JSON.stringify(this.toserve[i]);
          before = initial;

          count = 0;
          constant = 0;
        } else {
          constant += 1;
        }
      }, speed);
    },
    async forceUpdate() {
      for (var use in this.unsaved) {
        if (Object.keys(this.unsaved[use]).length != 0) {
          await this.save(use);
        }
      }
      window.location.reload();
    },
  },
  components: {
    Content,
  },
};
</script>

<style lang="scss" scoped>
$width: 5px;

a {
  margin-bottom: 10px;
}

.saver {
  opacity: 0%;
  margin-right: 50px;
  transition: all 1s ease;
  display: flex;
  justify-content: flex-end;
  div {
    display: flex;
  }
}
.crl {
  width: $width;
  height: $width;
  border-radius: 50%;
  background: #0f476f;
  margin-left: 2px;
  margin-right: 2px;
}

.sync {
  opacity: 1 !important;
  div {
    .crl {
      animation-iteration-count: infinite;
      animation-duration: 2.5s;
      animation-timing-function: ease-out;
    }
    #cr1 {
      animation-name: synca;
    }
    #cr2 {
      animation-name: syncb;
    }
    #cr3 {
      animation-name: syncc;
    }
  }
}

.save {
  padding-right: 150px;
  opacity: 0%;
}

.invisible {
  opacity: 0.66;
}

//tracking bzw synching animation

@keyframes synca {
  15% {
    transform: translateX(0px);
  }
  35% {
    transform: translateX(50px);
  }
  50% {
    transform: translateX(50px);
  }
  75% {
    transform: translateX(0px);
  }
}
@keyframes syncb {
  10% {
    transform: translateX(0px);
  }
  30% {
    transform: translateX(50px);
  }
  60% {
    transform: translateX(50px);
  }
  80% {
    transform: translateX(0px);
  }
}

@keyframes syncc {
  0% {
    transform: translateX(0px);
  }
  25% {
    transform: translateX(50px);
  }
  65% {
    transform: translateX(50px);
  }
  85% {
    transform: translateX(0px);
  }
}
</style>