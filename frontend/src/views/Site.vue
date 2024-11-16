<template>
  <div class="hori highlvl">
    <Dashboard />
    <div v-if="done" id="content" class="site">
      <h1 class="tight">{{ subsite }}</h1>
      <h3
        class="tight"
        v-if="!subsite.includes('Document') && !subsite.includes('Points')"
      >
        manage your relating items here
      </h3>
      <h3 class="tight" v-else>Have a look at them</h3>
      <br />
      <div class="wrap">
        <div v-for="project in fdata" :key="project._id">
          <div class="project">
            <h3
              :title="admin ? 'click to copy prjid' : ''"
              @click="copyToClibboard(project._id, admin)"
            >
              {{ project.name }}
            </h3>
            <Saver :toserve="project.contents" :admin="admin" />
          </div>
          <div
            v-if="project.note && project.note.blog"
            class="project blog"
            id="content"
          >
            <h3>Edit your Blog relating to {{ project.name }}</h3>

            <div class="field column">
              <label for="">Select the blog article to edit</label>
              <div class="hori spce">
                <select
                  class="bborder"
                  id="blog-select"
                  @change="loadArticle(project.articles)"
                  v-model="blogid"
                >
                  <option selected value="">create a new blog article</option>
                  <option
                    v-for="blog in project.articles"
                    :value="blog.id"
                    :key="blog.id"
                  >
                    {{ blog.title }}
                  </option>
                </select>
                <hr style="height: 0" />
                <button
                  style="width: 100px; margin-right: 10px"
                  @click="reload()"
                >
                  refresh
                </button>
              </div>
            </div>
            <div class="field column">
              <label for="">Title</label>
              <input
                @input="publishBlog(project._id, false)"
                type="text"
                class="bborder"
                v-model="blogtitle"
              />
            </div>
            <div class="field column">
              <label for="">Text</label>
              <textarea
                style="min-height: 30vh; margin-top: 5px"
                class="bborder blogtext"
                v-model="blogtext"
                @input="publishBlog(project._id, false)"
              />
            </div>
            <br />
            {{ synced ? "saved" : "..." }}
            <label for="">show publicly</label>

            <div class="hori spce">
              <label class="switch">
                <input
                  type="checkbox"
                  v-model="blogpublic"
                  @change="publishBlog(project._id, false)"
                />
                <span class="slider round"></span>
              </label>
              <button
                :disabled="!blogid || blogpublic"
                style="width: 120px; margin-right: 10px"
                @click="publishBlog(project._id, true)"
              >
                delete draft
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import VueCookie from "vue-cookies";
import axios from "axios";
import vars from "@/assets/vars";
import Dashboard from "@/components/Dashboard.vue";
import Saver from "@/components/Saver.vue";

export default {
  name: "Site-space",
  data() {
    return {
      fdata: [],
      subsite: "",
      admin: false,
      done: false,
      blogtext: "",
      blogtitle: "",
      blogid: "",
      blogpublic: "",
      synced: false,
    };
  },
  async mounted() {
    var admin_token = VueCookie.get("admin_token");
    if (admin_token) {
      await axios
        .post(vars.url + "/super/token", {
          adminToken: admin_token,
        })
        .then((response) => {
          VueCookie.set("admin_token", response.data);
          this.admin = true;
        })
        .catch(() => {});
    }
    this.subsite = window.location.pathname;
    axios
      .post(vars.url + "/cms/get" + this.subsite, {
        token: VueCookie.get("session_token"),
      })
      .then((response) => {
        for (var project in response.data) {
          console.log("project:", project);
          this.fdata.push(response.data[project]);
        }
        this.subsite = this.fdata[0].category;
        this.done = true;
      })
      .catch((err) => console.log(err));
  },
  methods: {
    copyToClibboard(text, bool) {
      if (!bool) {
        return;
      }
      navigator.clipboard.writeText(text).then(
        function () {
          console.log("Async: Copying to clipboard was successful!");
        },
        function (err) {
          console.error("Async: Could not copy text: ", err);
        }
      );
    },
    reload() {
      window.location.reload();
    },
    async publishBlog(prjid, del) {
      this.synced = false;
      var nextid = "";
      if (!del) {
        if (!this.blogpublic) this.blogpublic = false;
        await axios
          .post(vars.url + "/service/" + prjid + "/post", {
            token: VueCookie.get("session_token"),
            title: this.blogtitle,
            text: this.blogtext,
            public: this.blogpublic,
          })
          .then((response) => {
            nextid = response.data;
            this.synced = true;
          });
      }
      if (this.blogid != "") {
        await axios
          .post(vars.url + "/service/" + prjid + "/delete/post", {
            token: VueCookie.get("session_token"),
            id: this.blogid,
          })
          .then((response) => {
            if (response.data == "success") {
              if (del) window.location.reload();
            }
          });
      }
      this.blogid = nextid;
    },
    async loadArticle(articles) {
      for (var art in articles) {
        if (this.blogid == articles[art].id) {
          this.blogtitle = articles[art].title;
          this.blogtext = articles[art].text;
          this.blogpublic = articles[art].public;
          console.log("set to:", articles[art].public);
          return;
        }
      }
      this.blogtitle = "";
      this.blogtext = "";
    },
  },
  components: {
    Dashboard,
    Saver,
  },
};
</script>

<style lang="scss">
$primary: #0f476f;

.project {
  margin: 30px 0 10px;
  background: #fff;
  box-shadow: 0px 0px 5px 0 #bbb;
  border-radius: 8px;
  padding: 30px 40px 20px 30px;

  h3 {
    margin-bottom: 30px;
  }
}
.blog.project {
  width: calc(100% - 130px);
  padding: 40px 30px 20px 50px !important;

  input,
  textarea {
    width: calc(100% - 30px);
  }
  select {
    width: calc(100% - 10px);
  }
  button {
    padding: 6px 0;
    width: calc(100% - 8px);
  }
  textarea {
    padding: 5px 10px;
  }
  /* The switch - the box around the slider */
  .switch {
    position: relative;
    display: inline-block;
    width: 56px;
    height: 28px;
  }

  /* Hide default HTML checkbox */
  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  /* The slider */
  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    -webkit-transition: 0.4s;
    transition: 0.4s;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 22px;
    width: 22px;
    left: 4px;
    bottom: 3px;
    background-color: white;
    -webkit-transition: 0.4s;
    transition: 0.4s;
  }

  input:checked + .slider {
    background-color: $primary;
  }

  input:focus + .slider {
    box-shadow: 0 0 1px $primary;
  }

  input:checked + .slider:before {
    -webkit-transform: translateX(26px);
    -ms-transform: translateX(26px);
    transform: translateX(26px);
  }

  /* Rounded sliders */
  .slider.round {
    border-radius: 28px;
  }

  .slider.round:before {
    border-radius: 50%;
  }
}
</style>
