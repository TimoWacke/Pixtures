<template>
  <div class="hori highlvl">
    <Dashboard />
    <div id="content" class="site">
      <div id="visitor">
        <label>login as</label>
        <select
          @change="loginV()"
          class="bborder"
          name="customer"
          v-model="visit"
        >
          <option
            v-for="cust in allcustomers"
            :key="cust.forename"
            :value="cust._id"
          >
            {{ cust.edit.forename }} {{ cust.edit.surname }}
          </option>
        </select>
      </div>
      <div class="wrap">
        <div
          class="project fat"
          v-cloak
          @drop.prevent="addFile"
          @dragover.prevent="overlay()"
          @dragleave.prevent="dragleave()"
        >
          <h2>Register a customers email</h2>
          <div class="hori zontal mobile-compr">
            <input
              style="width: 100%"
              type="text"
              class="bborder"
              v-model="prereg.email"
              placeholder="john.doe@gmail.com"
            />
            <hr />
            <select name="empfohlen" class="bborder" v-model="prereg.empfohlen">
              <option value="" disabled selected>recommended by</option>
              <option
                v-for="cust in allcustomers"
                :value="cust._id"
                :key="cust.forename"
              >
                {{ cust.edit.forename }} {{ cust.edit.surname }}
              </option>
            </select>
          </div>
          <div class="hori zontal mobile-compr">
            <input
              type="text"
              class="bborder"
              v-model="prereg.forename"
              placeholder="John"
            />
            <hr />
            <input
              type="text"
              class="bborder"
              v-model="prereg.surname"
              placeholder="Doe"
            />

            <hr />
            <button class="send" id="send" @click="preReg()">
              start using this email
            </button>
          </div>
          <br />
          <h2>
            <a @click="toggle()">{{ prj.mode }}</a> a project with a customer
          </h2>
          <div class="column">
            <label>Customer</label>
            <select
              @change="exist()"
              class="bborder"
              name="customer"
              v-model="prj.user"
              placeholder="empfohlen von"
            >
              <option
                v-for="cust in allcustomers"
                :key="cust.forename"
                :value="cust._id"
              >
                {{ cust.edit.forename }} {{ cust.edit.surname }}
              </option>
            </select>
          </div>
          <div v-if="prj.mode == 'Manage'" id="manage">
            <div class="hori">
              <div class="column" style="width: 100%">
                <label>Choose Project</label>
                <select class="bborder" name="project" v-model="project">
                  <option
                    v-for="proj in existing"
                    :key="proj.name"
                    :value="proj"
                  >
                    {{ proj.name }} - {{ proj.category }}
                  </option>
                </select>
              </div>
              <hr />
              <div class="column">
                <label for="">Price (€)</label>
                <input class="bborder" type="number" v-model="prj.price" />
              </div>
            </div>
          </div>
          <div v-if="prj.mode == 'Create'" id="create">
            <div class="hori">
              <div class="column" style="width: 100%">
                <label>What kind of project?</label>
                <select class="bborder" name="category" v-model="prj.category">
                  <option value="Social Pictures">Social Pictures</option>
                  <option value="Transfered Files">Transfering Files</option>
                  <option value="Website">Website</option>
                  <option value="Fotoshootings">Fotoshootings</option>
                  <option value="Videoproduktionen">Videoproduktionen</option>
                </select>
              </div>
              <hr />
              <div class="column">
                <label for="">Price (€)</label>
                <input class="bborder" type="number" v-model="prj.price" />
              </div>
            </div>
            <label>Project Name</label>
            <input class="bborder" type="text" v-model="prj.name" />
          </div>
          <br />
          <label>Drop files for the customer here</label>

          <div id="dragdrop" class="dragdrop bborder">
            <ul>
              <li v-for="file in files" :key="file.name" class="hori spce">
                {{ file.name }} ({{ file.size }} kb)
                <button @click="removeFile(file)" title="Remove">X</button>
              </li>
            </ul>
          </div>
          <button style="width: 100%" @click="upload">Upload</button>
        </div>
        <BankingPlaid v-if="timeline" :timeline="timeline"></BankingPlaid>
        <div class="project fat">
          <h2>Add Content to project</h2>
          <div class="hori">
            <div class="column">
              <label>Customer</label>
              <select
                @change="exist()"
                class="bborder"
                name="customer"
                v-model="prj.user"
                placeholder="empfohlen von"
              >
                <option
                  v-for="cust in allcustomers"
                  :key="cust.forename"
                  :value="cust._id"
                >
                  {{ cust.edit.forename }} {{ cust.edit.surname }}
                </option>
              </select>
            </div>
            <hr />
            <div class="column" style="width: 100%">
              <label>Choose Project</label>
              <select class="bborder" name="project" v-model="project">
                <option v-for="proj in existing" :key="proj.name" :value="proj">
                  {{ proj.name }} - {{ proj.category }}
                </option>
              </select>
            </div>
          </div>
          <div class="column">
            <label for="">Content</label>
            <div class="hori zontal mobile-compr spce">
              <p>info.name</p>
              <hr />
              :
              <hr />
              <input
                class="bborder"
                type="text"
                placeholder="value"
                style="width: 69%"
                v-model="content.info['name']"
              />
            </div>
            <div class="hori zontal mobile-compr spce">
              <p>edit</p>
              <hr />
              :
              <hr />
              <input
                class="bborder"
                type="text"
                placeholder="value"
                style="width: 69%"
                v-model="content['edit']"
              />
            </div>
            <div class="hori zontal mobile-compr spce">
              <p>public</p>
              <hr />
              :
              <hr />
              <input
                class="bborder"
                type="text"
                placeholder="value"
                style="width: 69%"
                v-model="content['public']"
              />
            </div>
            <div class="hori zontal mobile-compr spce">
              <p>dynamicCopy</p>
              <hr />
              :
              <hr />
              <input
                class="bborder"
                type="text"
                placeholder="value"
                style="width: 69%"
                v-model="content['dynamicCopy']"
              />
            </div>
            <div class="hori zontal mobile-compr spce">
              <p>invisible?</p>
              <hr />
              :
              <hr />
              <input
                class="bborder"
                type="text"
                placeholder="value"
                style="width: 69%"
                v-model="content['invisible']"
              />
            </div>
          </div>
          <button style="width: 100%" @click="save">save</button>
        </div>
        <div class="project fat">
          <h2>Your webtracking analytics</h2>
          <TimelinePicker
            :default="30"
            @setTimeline="setTimeline"
          ></TimelinePicker>
          <div
            class="apikey"
            v-for="(apikey_data, key) in analyticsdata"
            :key="key"
          >
            <div
              class="domain"
              v-for="(domain, name) in apikey_data"
              :key="name"
            >
              <br />
              <label for="">{{ name }}</label>
              <div class="hori spce">
                <p>visits: {{ domain.visits }}</p>
                <br />
                <p>unique visitors: {{ domain.uniqueusers }}</p>
                <br />
                <p>signed in visitors: {{ domain.signedusers }}</p>
              </div>
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
import router from "@/router";
import BankingPlaid from "@/components/BankingPlaid.vue";
import TimelinePicker from "@/components/TimelinePicker.vue";

export default {
  name: "Admin-Site",
  data() {
    return {
      visit: "",
      prj: {
        mode: "",
        user: "", //selected user in dropdown
        price: 0,
        category: "", //selected category in dropdown
        name: "",
      },
      project: "", //selected prj in dropdown
      allcustomers: "",
      existing: [],
      files: [],
      prereg: {
        email: "",
        surname: "",
        forename: "",
        empfohlen: "",
      },
      content: { info: {} },
      nextTab: '" : "',
      nextEnter: '" : {\n"',
      apikeys: ["s9MsnRtgo1NzHEh0", "76EGqqlZjsIglFWQ", "kWACGVQxG46wcxJa"],
      analyticsdata: {},
      timeline: false,
    };
  },
  async mounted() {
    this.getCustomers();
    this.toggle();
    this.getAnalyticsData();
    this.setTimeline(30);
    //apikey analtycsdata
  },
  methods: {
    setTimeline(days) {
      console.log("setting timeline to", days);
      this.timeline = new Date(new Date().setDate(new Date().getDate() - days));
      this.getAnalyticsData();
    },
    async getAnalyticsData() {
      var me = this;
      for (var key of me.apikeys) {
        await axios
          .post(vars.url + "/analytics/data", {
            token: VueCookie.get("session_token"),
            apikey: key,
            timeline: me.timeline,
          })
          .then((response) => {
            me.analyticsdata[key] = response.data;
            Object.keys(response.data).forEach((domainname) => {
              console.log(
                "analyticsdata for",
                domainname + ":",
                response.data[domainname]
              );
            });
          });
      }
    },
    formatContent(event) {
      if (
        event.code == "Tab" ||
        (event.code == "Enter" && this.nextTab == '",\n"')
      ) {
        event.preventDefault();
        this.content += this.nextTab;
        if (this.nextTab == '",\n"') {
          this.nextTab = '" : "';
        } else {
          this.nextTab = '",\n"';
        }
      } else if (event.code == "Enter") {
        event.preventDefault();
        this.content += this.nextEnter;

        if (this.nextEnter == '"\n},\n"') {
          this.nextEnter = '" : {\n"';
        } else {
          this.nextEnter = '"\n},\n"';
        }
      }
    },
    async getCustomers() {
      await axios
        .post(vars.url + "/customers", {
          token: VueCookie.get("session_token"),
        })
        .then((response) => {
          this.allcustomers = response.data;
        });
    },
    addFile(e) {
      let droppedFiles = e.dataTransfer.files;
      if (!droppedFiles) return;
      // this tip, convert FileList to array, credit: https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
      [...droppedFiles].forEach((f) => {
        this.files.push(f);
      });
      this.dragleave();
    },
    overlay() {
      document.getElementById("dragdrop").style.background = "#cefb";
    },
    dragleave() {
      document.getElementById("dragdrop").style.background = "#fff0";
    },
    remove() {
      this.files = [];
    },
    removeFile(file) {
      this.files = this.files.filter((f) => {
        return f != file;
      });
    },
    save() {
      axios
        .post(vars.url + "/cms/addcontent/" + this.project._id, {
          token: VueCookie.get("session_token"),
          content: this.content,
        })
        .then((response) => {
          console.log(response.data);
        });
    },
    async upload() {
      this.prj["token"] = VueCookie.get("session_token");
      if (this.prj.mode == "Manage") {
        this.prj.category = this.project.category;
        this.prj.name = this.project.name;
      }

      var formData = new FormData();
      for (var elem in this.prj) {
        formData.append(elem, this.prj[elem]);
      }
      this.files.forEach(async (f, x) => {
        formData.append("file" + (x + 1), f);
      });

      axios
        .post(vars.url + "/cms/project", formData, {
          headers: {
            "Content-Type": "mulipart/form-data",
          },
        })
        .then((response) => {
          if (response.data == "success") {
            this.remove();
          }
        });
    },
    async toggle() {
      if (this.prj.mode == "Create") {
        this.prj.mode = "Manage";
        await this.exist();
        return;
      }
      this.prj.mode = "Create";
    },
    async exist() {
      if (this.prj.user) {
        await axios
          .post(vars.url + "/cms/existing", {
            user: this.prj.user,
            token: VueCookie.get("session_token"),
          })
          .then((response) => {
            this.existing = response.data;
          })
          .catch((err) => {
            console.log("exist err:", err);
          });
      }
    },
    async preReg() {
      await axios.post(vars.url + "/prereg", { user: this.prereg }).then(() => {
        this.prereg = {};
        this.getCustomers();
      });
    },
    async loginV() {
      var vToken;
      VueCookie.set("admin_token", VueCookie.get("session_token"));
      await axios
        .post(vars.url + "/super/token", {
          adminToken: VueCookie.get("session_token"),
          user: this.visit,
        })
        .then((response) => {
          vToken = response.data;
        });
      VueCookie.set("session_token", vToken);
      router.push("/");
    },
    async addApiKey(authorized = []) {
      await axios
        .post(vars.url + "/analytics/createApiKey", {
          token: VueCookie.get("session_token"),
          authorized: authorized,
        })
        .then((response) => {
          alert("created api key: " + JSON.stringify(response.data));
        });
    },
  },
  components: {
    Dashboard,
    BankingPlaid,
    TimelinePicker,
  },
};
</script>

<style lang="scss">
.dragdrop {
  min-height: 150px;
  padding: 0 20px;
  margin: 10px 0;
  min-width: calc(300px + 5vw);
}

.chart {
  canvas {
    width: 640px;
    height: 320px;
  }
}

ul {
  list-style: none;
}
h2 a {
  cursor: pointer;
  &:hover {
    opacity: 50%;
  }
}
hr {
  height: 45px;
}
#create,
#manage {
  display: flex;
  flex-direction: column;
}
#visitor {
  position: absolute;
  display: flex;
  top: 45px;
  align-items: center;

  select {
    margin-left: 20px;
    width: 15vw;
    min-width: 200px;
  }
  label {
    margin-top: 0;
  }
}

.project.fat {
  padding: 15px 40px 35px;
}
</style>
