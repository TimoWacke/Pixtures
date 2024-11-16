<template>
  <div id="iframe" v-if="done" :key="keyCode">
    <button @click="share()">share</button>
    <div class="journal-view">
      <div
        class="blogcard"
        @click.self="openBlog(blog._id)"
        v-for="blog in journalView"
        v-bind:key="blog.title"
      >
        <div v-if="blog._id != exclude">
          <div @click.self="openBlog(blog._id)" class="hori spce">
            <h2
              @click="openBlog(blog._id)"
              :class="
                this.$root.formatDate(blog.customdate) != blog.title
                  ? 'named'
                  : ''
              "
            >
              {{ blog.title }}
            </h2>
            <div v-if="'ispublic' in blog">
              <img
                v-if="!blog.ispublic"
                @click="deleteBlog(blog._id)"
                src="@/assets/delete.svg"
                class="del-btn"
              />
              <div v-else class="public-indicator">
                <span class="Mark">
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
              </div>
            </div>
          </div>
          <p
            @click="openBlog(blog._id)"
            class="date"
            v-if="this.$root.formatDate(blog.customdate) != blog.title"
          >
            {{ this.$root.formatDate(blog.customdate) }}
          </p>
          <div
            @click="openBlog(blog._id)"
            class="preview"
            v-html="
              blog.draftbullets[0].data.substring(0, 100) +
              (blog.draftbullets[0].data.length > 100 ? '...' : '')
            "
          ></div>
          <div
            @click="openBlog(blog._id)"
            class="preview"
            v-if="blog.draftbullets[0].data.length < 50 && blog.draftbullets[1]"
            v-html="
              blog.draftbullets[1].data.substring(
                0,
                100 - blog.draftbullets[0].data.length
              ) +
              (blog.draftbullets[0].data.length >
              100 - blog.draftbullets[0].data.length
                ? '...'
                : '')
            "
          ></div>
        </div>
      </div>
    </div>
    <div id="showBlog">
      <div class="hori">
        <a v-if="focusBlog.title" class="back-btn" @click="goBack()">back</a>
        <h3>{{ focusBlog.title }}</h3>
      </div>
      <div v-for="bullet in focusBlog.draftbullets" v-bind:key="bullet">
        <br />
        <div>{{ bullet.data }}</div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

//import axios from "axios";
//import vars from "@/assets/vars";
import VueCookie from "vue-cookies";
import vars from "@/assets/vars";
import axios from "axios";

export default {
  name: "Journal-view",
  props: ["redirect", "blank", "usr_prj_id", "exclude"],
  data() {
    return {
      journal: [],
      journalView: [],
      usedid: false,
      focusBlog: {},
      backlink: "",
      keyCode: 0,
      done: false,
    };
  },
  components: {},
  async mounted() {
    this.usedid = this.usr_prj_id;
    var match = decodeURI(window.location.href).match(
      /\?([^?]*)id=([a-zA-Z0-9]{24})/
    );

    if (!this.usedid) {
      try {
        this.usedid = match[2];
      } catch (e) {
        console.log(e);
      }
    }
    await axios
      .post(vars.url + "/cms/journal", {
        token: VueCookie.get("session_token"),
        usr_prj_id: this.usedid,
      })
      .then((response) => {
        this.journal = response.data.blogs;
        this.journalView = response.data.blogs;
        this.done = true;
      });
    var isnull = document.getElementById("editor");
    if (!isnull) {
      document.getElementById("iframe").classList.remove("compr");
    }
    try {
      if (match[1]) {
        console.log("open:", match[1]);
        this.openBlog(match[1]);
      }
    } catch {
      console.log("main page");
    }
  },
  methods: {
    openBlog(id) {
      if (this.redirect) {
        if (this.blank) {
          window.open(this.redirect + "?" + id, "_blank");
        } else {
          window.location.href = this.redirect + "?" + id;
        }
      } else {
        this.journalView = [];
        for (var i in this.journal) {
          if (this.journal[i]._id == id || this.journal[i].title == id) {
            this.focusBlog = this.journal[i];
            var match = window.location.href.match(
              /^([^?]+\/journal\?)[^?]*(id=[a-zA-Z0-9]{24})/
            );
            this.backlink = match[1] + match[2];
            var newurl = match[1] + this.focusBlog.title + match[2];
            window.history.pushState({ path: newurl }, "", newurl);
          }
        }
      }
    },
    goBack() {
      var match = window.location.href.match(
        /^([^?]+\/journal\?)[^?]*(id=[a-zA-Z0-9]{24})/
      );
      this.focusBlog = {};
      var newurl = match[1] + match[2];
      window.history.pushState({ path: newurl }, "", newurl);
      this.keyCode += 1;
      this.journalView = this.journal;
    },
   
    async deleteBlog(bid) {
      await axios
        .post(vars.url + "/cms/delete-blog", {
          token: VueCookie.get("session_token"),
          id: bid,
        })
        .then((response) => {
          if (response.data == "success") {
            for (var i in this.journal) {
              if (this.journal[i]._id == bid) this.journal.splice(i, 1);
            }
          }
        });
    },
    async share() {
      var shareurl =
        vars.loyalty +
        "/journal?id=" +
        (this.focusBlog._id ? this.focusBlog._id : this.usedid);
     
      if (navigator.share) {
        await navigator
          .share({
            title: "Share your Journal",
            url: shareurl,
          })
          .then(() => {
            console.log("Thanks for sharing!");
          })
          .catch(console.error);
      } else {
        alert("couldnt share: " + shareurl);
      }
    },
  },
};
</script>

<style lang="scss">
.journal-view {
  width: 100%;
  max-width: 1400px;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

#showBlog {
  width: min(1200px, 65vw);
  max-width: 90vw;
  margin: 100px auto;
}

.blogcard {
  cursor: pointer;
  min-width: max(200px, 15.906vw);
  margin: calc(10px + 0.02vw) calc(10px + 0.02vw);
  width: min-content;
  max-width: calc(100vw - 20px);
  @media only screen and (max-width: 530px) {
    width: calc(100% - 30px);
  }
  box-shadow: 0 0 5px #bbb;
  padding: 15px;
  border-radius: 5px;

  h2 {
    margin-top: 0;
    margin-bottom: 12px;
    font-size: 20px;
    &.named {
      margin-bottom: 2px;
      font-size: 16px;
    }
  }

  .preview {
    font-size: 1em;
    margin: 10px 0;
  }
}
img.del-btn {
  width: 12px;

  height: 15px;
  &:hover {
    transform: translateY(-2px);
  }
}

.public-indicator {
  align-items: center;
  background: #0f476f;
  border-radius: 50%;
  display: flex;
  height: 16px;
  width: 16px;
  justify-content: center;
}

// The check mark is optional
.Mark {
  fill: #fff;
  width: 14px;
  height: 20px;
  z-index: 15;
}

p.date {
  color: #444;
  font-size: 10px;
  margin-bottom: 4px;
}

.back-btn {
  width: 40px;
  margin-left: -40px;
  padding: 0;
  transform: translateX(-40px);
}
</style>
