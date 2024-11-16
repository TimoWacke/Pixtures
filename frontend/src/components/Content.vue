<template>
  <div :class="'node ' + (item.file ? 'file' : '')">
    <div class="content-icon" v-if="item.file" style="width: 30px">
      <img v-if="item.file.endsWith('.pdf')" src="../assets/icon_pdf.svg" />
      <img v-else src="../assets/icon_else.svg" alt="" />
    </div>
    <div id="details" class="box" style="width: 100%">
      <div v-for="(child, name) in item" :key="name">
        <div
          :class="Array.isArray(item) ? 'shadow' : ''"
          :style="Array.isArray(item) ? 'margin: 5px 0' : ''"
          v-if="
            typeof child === 'object' &&
            (name == 'edit' ||
              name == 'info' ||
              path.includes('info') ||
              path.includes('edit'))
          "
        >
          <label
            v-if="path.includes('edit') && !Array.isArray(item)"
            for=""
            style="margin-left: 10px"
            >{{ name }}</label
          >
          <Content
            :item="child"
            :id="id"
            :prjid="prjid"
            @refresh="forceUpdate()"
            :path="path == '' ? name : path + '.' + name"
          />
          <div v-if="Array.isArray(child)" class="box">
            <button
              @click="pushToLinkTree(child)"
              style="width: 25px; margin: 5px 10px"
            >
              +
            </button>
            <button
              @click="child.pop()"
              style="width: 25px; margin: 5px 10px 5px 0"
              title="deletes last"
            >
              -
            </button>
            <button @click="build(id, child)">publish</button>
          </div>
        </div>
        <div v-else-if="path.includes('info') || path.includes('edit')">
          <div v-if="path.includes('info')">
            <div v-if="name.endsWith('-copylink')" class="field">
              <label for=""> {{ name.slice(0, name.length - 9) }}</label>
              <button class="" @click="copyToClibboard(child)">
                copy link
              </button>
            </div>
            <div v-else class="field">
              <label for="">{{ name }}</label>
              <p
                :class="
                  name == 'value' || name == 'balance' ? 'text-right' : ''
                "
              >
                {{ child }}
              </p>
            </div>
          </div>
          <div class="field" v-if="path.includes('edit')">
            <label for="">{{ name }}</label>
            <div class="draft" v-if="name == 'draft'">
              <textarea v-bind:value="item[name]" @input="valChg(name, id)" :id="id + name" />
              <button @click="publish(id, child)">publish</button>
            </div>
            <input
              v-else
              v-bind:value="item[name]"
              @input="valChg(name, id)"
              :id="id + name" 
              :type="['color, checkbox'].includes(name) ? name : 'text'"
              
            />
          </div>
        </div>
        <div class="pushdown" v-if="name == 'file'">
          <button class="open-file" @click="open(child)">open file</button>
        </div>

        <div
          class="public-layout"
          v-if="name == 'public' && !Array.isArray(item['edit'])"
        >
          <label
            @click="publiclink(id)"
            title="copy link"
            class="pointer"
            for=""
            >public</label
          >
          <p>{{ child.length > 140 ? child.slice(0, 140) + "..." : child }}</p>
        </div>
      </div>
    </div>
    <div v-if="item.dynamicCopy">
      <button class="copy-btn" @click="dynamicCopy(item.dynamicCopy)">
        click to copy
      </button>
    </div>
  </div>
</template>

<script>
import VueCookie from "vue-cookies";
import axios from "axios";
import vars from "@/assets/vars";

export default {
  name: "content-item",
  props: {
    item: {
      type: Object,
      required: true,
    },
    id: { type: String, required: true },
    prjid: { type: String },
    path: { type: String },
  },

  mounted() {
    if (this.id) {
      var elem = document.getElementById(this.id + "draft");
      if (elem) {
        elem.style.height = elem.scrollHeight + "px";
      }
    }
  },
  methods: {
    valChg(name, id) {
      // eslint-disable-next-line
      this.item[name] = document.getElementById(id + name).value;
    },
    publish(id, value) {
      axios
        .post(vars.url + "/cms/publish/", {
          token: VueCookie.get("session_token"),
          cid: id,
          value: value,
          prjid: this.prjid,
        })
        .then((response) => {
          if (response.data == "success") {
            this.$emit("refresh");
          }
        });
    },
    build(id, item) {
      var html = "";
      for (var i in item) {
        if (!item[i].link.startsWith("https://")) {
          item[i].link = "https://" + item[i].link;
        }
        html +=
          '<a href="' +
          item[i].link +
          '" style="background:' +
          item[i].color +
          ';">' +
          item[i].name +
          "</a>";
      }
      this.publish(id, html);
    },
    open(url) {
      window.open(vars.url + "/cms" + url);
    },
    async publiclink(id) {
      await axios
        .post(vars.url + "/cms/link/" + id, {
          token: VueCookie.get("session_token"),
          cid: id,
        })
        .then((response) => this.copyToClibboard(vars.url + response.data));
    },
    async dynamicCopy(url) {
      await axios
        .get(
          (url.startsWith("https://") ? "" : vars.url) +
            url +
            "/" +
            VueCookie.get("session_token")
        )
        .then((response) => this.copyToClibboard(response.data));
    },
    forceUpdate() {
      this.$emit("refresh");
    },
    copyToClibboard(text) {
      {
        navigator.clipboard.writeText(text).then(
          function () {
            console.log("Async: Copying to clipboard was successful!");
          },
          function (err) {
            console.error("Async: Could not copy text: ", err);
          }
        );
      }
    },
    pushToLinkTree(child) {
      child.push({
        color: "#000000",
        link: "https://example.com",
        name: "name",
      });
    },
  },
};
</script>

<style lang="scss" >
.copy-btn {
  width: 150px;
  margin-top: 25%;
}
</style>