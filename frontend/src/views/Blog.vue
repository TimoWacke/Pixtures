<template>
  <div class="hori highlvl blog">
    <Dashboard />
    <div v-if="done" id="content" class="site blog">
      <h3 id="onmind">What's on your mind {{ aps["user"].edit.forename }}?</h3>
      <div id="editor">
        <br />
        <div class="hori">
          <input
            class="h2"
            type="text"
            id="blogtitle"
            v-model="blog.title"
            v-autowidth="{
              maxWidth: '100%',
              minWidth: '0px',
              comfortZone: 0,
            }"
          />
          <div id="settingsbar">
            <input
              type="date"
              v-if="this.$root.formatDate(blog.customdate) != blog.title"
              v-model="formdate"
              @input="blog.customdate = new Date(formdate)"
            />
            <label class="toggle" for="uniqueID">
              <input
                type="checkbox"
                class="toggle__input"
                id="uniqueID"
                v-model="blog.ispublic"
              />
              <span class="toggle-track">
                <span class="toggle-indicator">
                  <span class="checkMark">
                    <svg
                      viewBox="0 0 24 24"
                      id="ghq-svg-check"
                      role="presentation"
                      aria-hidden="true"
                    >
                      <path
                        d="M9.86 18a1 1 0 01-.73-.32l-4.86-5.17a1.001 1.001 0 011.46-1.37l4.12 4.39 8.41-9.2a1 1 0 111.48 1.34l-9.14 10a1 1 0 01-.73.33h-.01z"
                      ></path>
                    </svg>
                  </span>
                </span>
              </span>
              {{ blog.ispublic ? "public" : "private" }}
            </label>
          </div>
        </div>
        <div
          class="bullet"
          @click.self="setFocus(b)"
          v-for="(bullet, b) in blog.draftbullets"
          v-bind:key="b"
        >
          <div class="hori">
            <div class="dot-wrp">
              <div class="dot"></div>
            </div>
            <contenteditable
              :id="'li-' + b"
              class="content-wrp"
              tag="div"
              @input="syncInner(b)"
              :contenteditable="true"
              :noHtml="true"
              @keydown.tab="checkTab(b, $event)"
              @keydown.backspace="checkBackspace(b)"
              @paste="checkPaste($event)"
            />
          </div>
          <hr class="underline" />
        </div>
      </div>
      <div id="addbullet" class="plus bullet" @click="newBullet(-1)">
        <div class="hori">
          <div class="dot-wrp">
            <div class="dot"></div>
          </div>
        </div>
      </div>
      <Saver class="blog" :toserve="[blog]" :nodisplay="true" />

      <button class="inputnone" id="send"></button>
      <div id="divider" @click="toggleDivider()">
        <div id="upbutton">
          <hr id="line1" />
          <hr id="line2" />
        </div>
        <hr class="breakline" />
      </div>
      <Journal
        :class="'compr'"
        :redirect="editurl"
        :usr_prj_id="aps['user']._id"
        :exclude="this.blog._id"
      />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

//import axios from "axios";
//import vars from "@/assets/vars";
import App from "@/App.vue";
import vars from "@/assets/vars";
import VueCookie from "vue-cookies";
import Dashboard from "@/components/Dashboard.vue";
import Saver from "@/components/Saver.vue";
import Journal from "@/components/Journal.vue";

import axios from "axios";
export default {
  name: "Blog-Site",
  data() {
    return {
      aps: App.store,
      blog: {},
      done: false,
      editurl: "",
      formdate: "",
    };
  },
  components: {
    Dashboard,
    Saver,
    Journal,
  },
  async mounted() {
    var selfurl = window.location.href;
    var match = selfurl.match(/^([^\s?]+)\??([0-9a-zA-Z]*)$/);
    this.editurl = match[1];
    var openid = match[2];
    window.history.pushState({ path: this.editurl }, "", this.editurl);

    await axios
      .post(vars.url + "/cms/blog", {
        token: VueCookie.get("session_token"),
        id: openid,
      })
      .then((response) => {
        this.blog = response.data;
        this.blog["edit"] = true;
        if (this.blog.draftbullets.length == 0) {
          this.blog.draftbullets = [{ data: "" }];
        }
        this.formdate = this.$root.formatDate(
          this.blog.customdate,
          "YYYY-MM-DD"
        );
        this.done = true;
        setTimeout(this.initialise, 50);
      })
      .catch((error) => {
        console.log(error);
      });
  },
  methods: {
    syncInner(b) {
      this.blog.draftbullets[b].data = document.getElementById(
        "li-" + b
      ).innerHTML;
      this.blog.draftdate = new Date();
      //check if last bullet is empty? show add bullet button?
      document.getElementById("addbullet").classList.remove("compr");
      if (
        this.blog.draftbullets[this.blog.draftbullets.length - 1].data == ""
      ) {
        document.getElementById("addbullet").classList.add("compr");
      }
    },
    initialise() {
      for (var b in this.blog.draftbullets) {
        document.getElementById("li-" + b).innerHTML =
          this.blog.draftbullets[b].data;
      }
      document.getElementById("addbullet").classList.remove("compr");
      if (
        this.blog.draftbullets[this.blog.draftbullets.length - 1].data == ""
      ) {
        document.getElementById("addbullet").classList.add("compr");
      }
    },
    checkTab(b, e) {
      console.log("check on bullet b:", b);
      if (e.shiftKey) {
        if (b > 0) {
          this.setFocus(b);
        }
        return;
      }
      if (this.blog.draftbullets.length - 1 == b) {
        this.newBullet(b + 1);
      } else if (this.blog.draftbullets[b + 1].data != "") {
        console.log("new bullet");
        this.newBullet(b + 1);
      }
    },
    checkBackspace(b) {
      if (this.blog.draftbullets[b].data == "" && b > 0) {
        this.deleteBullet(b);
      }
    },
    newBullet(b) {
      if (b == -1) {
        b = this.blog.draftbullets.length;
      }
      this.blog.draftbullets.splice(b, 0, { data: "", isEditable: true });
      setTimeout(this.initialise, 25);
      setTimeout(this.setFocus(b), 100);
    },
    deleteBullet(b) {
      this.blog.draftbullets.splice(b, 1);
      setTimeout(this.initialise, 25);
      setTimeout(this.setFocus(b - 1), 50);
    },
    setFocus(b) {
      var bullet = document.getElementById("li-" + b);
      bullet.focus();
    },
    toggleDivider() {
      document.getElementById("onmind").classList.toggle("none");
      document.getElementById("settingsbar").classList.toggle("none");
      document.getElementById("divider").classList.toggle("flipped");
      document.getElementById("editor").classList.toggle("compr");
      document.getElementById("addbullet").classList.toggle("compr");
      document.getElementById("iframe").classList.toggle("compr");
    },
    checkPaste(e) {
      // cancel paste
      e.preventDefault();

      // get text representation of clipboard
      var text = (e.originalEvent || e).clipboardData.getData("text/plain");

      // insert text manually
      document.execCommand("insertHTML", true, text);
    },
  },
};
</script>

<style lang="scss">
#save {
  width: 100px;
  margin-bottom: -30px;
}

#cursor {
  width: 0;
}

#upbutton {
  height: 15px;
  position: relative;
  hr {
    background-color: #777;
    height: 27px;
    width: 4px;
    border-radius: 4px;
    position: absolute;

    &#line1 {
      transform: rotate(45deg) translateX(-12px);
    }
    &#line2 {
      transform: rotate(-45deg) translateX(12px);
    }
  }
}

.highlvl.blog {
  flex-direction: row !important;
  min-height: 100vh;

  @media only screen and (max-width: 1400px) {
    #content {
      padding-top: 50px;
    }
  }
}

#content {
  min-height: 100%;
}

#iframe.compr {
  margin-top: -50px;
  transform: translateY(50px);
}

#iframe {
  height: 100%;
}

#settingsbar {
  display: flex;
  align-items: center;
}

.compr .bullet {
  display: none;
}

#blogtitle {
  padding: 0;
}

#editor:not(.compr) {
  margin-bottom: auto;
}

#iframe.compr {
  max-height: 200px;
  overflow-y: hidden;
}

#divider {
  margin-top: -50px;
  margin-bottom: 10px;
  &.flipped {
    margin-top: -80px;
    transform: scaleY(-1);
  }
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  transition: all 0.5s ease;
  padding: 20px 0;
  &:hover {
    &:not(.flipped) {
      transform: translateY(-10px);
    }
    &.flipped {
      transform: scaleY(-1) translateY(-10px);
    }
  }
  cursor: pointer;
}

.inputnone {
  position: fixed;
  opacity: 0;
  bottom: 0;
  right: 0;
  z-index: -10;
}
#content.blog {
  display: flex;
  width: 100%;
}

input.h2 {
  font-size: 24px;
  margin: 0 0 25px;
  font-weight: 600;
  color: #0f476f;
}

hr.underline {
  width: calc(100% - 20px);
  height: 1px;
  margin: 10px 5px 5px;
  background-color: #eee;
}

hr.breakline {
  width: calc(100%);
  background-color: #777;
  border-radius: 65%;
  height: 4px;
  margin: 10px 0;
}

.bullet {
  min-height: 50px !important;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  div.dot-wrp,
  div.content-wrp {
    min-height: 21px;
  }
  div.dot-wrp {
    width: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    div.dot {
      display: flex;
      background-color: #0f476f;
      height: 10px;
      width: 10px;
      width: 10px;
      border-radius: 50%;
      z-index: 3;
    }
  }

  .content-wrp {
    display: inline;
    margin-left: 15px;
    font-size: 20px;
    line-height: 24px;
    vertical-align: baseline;
    width: calc(100% - 40px);
    outline: none;
  }
}

div.plus.bullet {
  cursor: pointer;
  margin-top: -5px !important;
  margin-bottom: -30px !important;
  opacity: 40%;
  &.compr {
    display: none;
  }
  @media (hover: hover) and (pointer: fine) {
    display: none;
  }
}

div.bullet {
  margin: 20px 0 30px !important;
}
@keyframes blink-animation {
  to {
    visibility: hidden;
  }
}
@-webkit-keyframes blink-animation {
  to {
    visibility: hidden;
  }
}

$toggle-indicator-size: 15px; // changing this number will resize the whole toggle
$track-height: $toggle-indicator-size + 5;
$track-width: $toggle-indicator-size * 2.5;
$highContrastModeSupport: solid 2px transparent;

$mid: #0f476f;
$speed: 0.5s;

$track-border: $mid;
$track-background: #fff;
$focus-ring: 0px 0px 0px 0px $mid;

// Toggle specific styles
.toggle {
  border-radius: 100px;
  display: flex;
  font-weight: 600;
  margin: 0;
  height: min-content;
}

// Since we can't style the checkbox directly, we "hide" it so we can draw the toggle.
.toggle__input {
  clip: rect(0 0 0 0);
  clip-path: inset(50%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;

  &:disabled + .toggle-track {
    cursor: not-allowed;
    opacity: 0.7;
  }
}

.toggle-track {
  background: $track-background;
  border: 1px solid $track-border;
  border-radius: 100px;
  cursor: pointer;
  display: flex;
  height: $track-height;
  margin-right: 12px;
  position: relative;
  width: $track-width;
}

.toggle-indicator {
  align-items: center;
  background: transparent;
  border: 1px solid $mid;
  border-radius: $toggle-indicator-size;
  bottom: 1px;
  display: flex;
  height: $toggle-indicator-size;
  justify-content: center;
  left: 1px;
  outline: $highContrastModeSupport;
  position: absolute;
  transition: $speed;
  width: $toggle-indicator-size;
}

// The check mark is optional
.checkMark {
  fill: #fff;
  height: $toggle-indicator-size + 4px;
  width: $toggle-indicator-size;
  opacity: 0;
  transition: opacity $speed ease-in-out;
}

.toggle__input:checked + .toggle-track .toggle-indicator {
  background: $mid;
  transform: translateX($track-width - $track-height);

  .checkMark {
    opacity: 1;
    transition: opacity $speed ease-in-out;
  }
}
</style>
