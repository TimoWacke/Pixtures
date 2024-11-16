<template>
  <div id="iframe" class="container wide">
    <div class="hori spce wrapflow">
      <div class="column">
        <h1>Create your custom design</h1>
        <br />
        <p id="error">{{ errormsg }}</p>
        <input id="file" class="custom-file-input" type="file" accept="image/*" v-on:change="onFileChange" />
        <br />
        <label for="">Jump to city:</label>
        <br />
        <div class="cityQuicklinks">
          <div v-for="city in suggestedCities" :key="city" class="cityBtn">
            <a @click="moveTo(city)"> {{ city.name }}</a>
          </div>
        </div>
      </div>
      <div>
        <h4 class="label">level of detail</h4>
        <input id="rs-range-line" class="rs-range" type="range" min="1" max="4" step="0.01" v-model="scale"
          @input="reloadScale" />
        <div id="background" red="bg">
          <GMap id="gmap" :key="coordinates.lat" :coordinates="coordinates" />
        </div>
        <button id="preview-btn" class="submit-btn" :disabled="!uploadDone || !file" @click="getPreview" :data-item-id="imageId +
          '_lat' +
          coordinates.lat +
          '_lng' +
          coordinates.lng +
          '_zm' +
          coordinates.zm +
          '_scale' +
          scale +
          '_ratio' +
          24 / 18
          ">
          {{
            !uploadDone || !file
              ? "Uploading your image"
              : "Submit for a free preview"
          }}
        </button>
      </div>
    </div>
    <div id="cnWrapper" class="hori">
      <span class="cityname special" id="cnbefore">{{
        this.previewLocation
      }}</span>
      <span class="cityname">
        {{ this.previewLocation }}
      </span>
      <span class="cityname special" id="cnafter">{{
        this.previewLocation
      }}</span>
    </div>
    <div id="mockupContainer">
      <img v-for="mockup in mockupUrls" :key="mockup" :src="mockup" />
      <img v-if="previewUrl" :src="previewUrl" />
      <div v-if="!uploadDone || !mockUpDone" id="loadingwrapper">
        <div id="loadingbox">
          <div id="before"><br /></div>
          <div id="after">
            {{ status }}
          </div>
        </div>
      </div>
    </div>
    <button v-if="identifier" class="submit-btn snipcart-add-item" :data-item-id="identifier"
      :data-item-url="'/pictures-map?' + identifier" :data-item-price="120.0" :data-item-image="mockupUrls[0]"
      :data-item-name="previewLocation">
      add to cart
    </button>
    <a class="snipcart-checkout">
      <svg height="1em" width="1em" focusable="false" fill="currentColor" viewBox="0 0 24 24"
        aria-labelledby="your-bag-12731763" role="img" aria-hidden="false">
        <title>Your shopping cart</title>
        <path
          d="M21.193 8.712a2.984 2.984 0 0 0-2.986-2.726h-.952v-.751a5.255 5.255 0 0 0-10.51 0v.75h-.951a2.983 2.983 0 0 0-2.986 2.727L1.715 20.73A2.999 2.999 0 0 0 4.7 24h.005l14.599-.027a2.998 2.998 0 0 0 2.98-3.27L21.193 8.712zM8.246 5.235a3.754 3.754 0 0 1 7.508 0v.75H8.246v-.75zm11.056 17.238-14.599.025h-.002a1.496 1.496 0 0 1-1.49-1.631l1.093-12.02a1.488 1.488 0 0 1 1.49-1.36h.95V9.74a.75.75 0 0 0 1.502 0V7.487h7.508V9.74c0 .415.336.75.75.75h.002a.75.75 0 0 0 .75-.75V7.487h.951a1.49 1.49 0 0 1 1.49 1.361l1.092 11.993a1.496 1.496 0 0 1-1.488 1.632z">
        </path>
      </svg>
    </a>
    <span class="snipcart-items-count"></span>
    <span class="snipcart-total-price"></span>
  </div>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@1,900&display=swap");
</style>

<script>
import axios from "axios";
import VueCookie from "vue-cookies";
import vars from "../assets/vars";
import GMap from "../components/myMap.vue";
import App from "@/App.vue";

export default {
  name: "Map-Site",
  data() {
    return {
      status: "",
      scale: 2.5,
      identifier: false,
      uploadDone: true,
      mockUpDone: true,
      file: false,
      coordinates: { lat: 53.55, lng: 10, zm: 12 },
      imageId: "",
      shopifyToken: ((Date.now() % (4 * 366 * 24 * 60 * 60 * 1000)) * 7)
        .toString(36)
        .toUpperCase(),
      mockupUrls: [],
      uploadPercentage: 0,
      errormsg: "",
      previewLocation: "",
      previewUrl: "",
      suggestedCities: [
        { name: "Amsterdam", lat: 52.365, lng: 4.88, zm: 14.9 },
        { name: "London", lat: 51.5, lng: -0.09, zm: 13.8 },
        { name: "Paris", lat: 48.8566, lng: 2.33, zm: 14.8 },
        { name: "Stockholm", lat: 59.335, lng: 18.0686, zm: 14.3 },
        { name: "Cape Town", lat: -34, lng: 18.48, zm: 14 },
        { name: "Rio d Janeiro", lat: -22.93, lng: -43.2, zm: 14.4 },
        { name: "Tokyo", lat: 35.7, lng: 139.8, zm: 12 },
        { name: "Bejing", lat: 39.9, lng: 116.4, zm: 13 },
        { name: "Shanghai", lat: 31.1, lng: 121.55, zm: 11.75 },
        { name: "Guangzhou", lat: 22.8, lng: 113.3, zm: 11.4 },
        { name: "Hong Kong", lat: 22.31, lng: 114.17, zm: 14.9 },
        { name: "New York", lat: 40.733, lng: -73.99, zm: 14.6 },
        { name: "Los Angeles", lat: 33.93, lng: -118.2, zm: 12.3 },
        { name: "Chicago", lat: 41.8781, lng: -87.67, zm: 14.6 },
      ],
    };
  },
  mounted() {
    // identifier format:
    try {
      var me = this;
      this.identifier = window.location.href.match(/\?(\S+)/)[1];
      console.log(this.identifier);
      axios
        .get(vars.pixtures + "/printful/identifier/" + this.identifier)
        .then((response) => {
          me.previewUrl = response.data.previewUrl;
          me.previewLocation = response.data.region;
          me.coordinates.lat = response.data.lat;
          me.coordinates.lng = response.data.lng;
          me.coordinates.zm = response.data.zm;
          me.scale =
            response.data.width /
            document.getElementById("background").offsetWidth;
          me.status = "Loading Mockups";
          me.getMockUps();
        });
    } catch {
      this.coordinates = this.suggestedCities[0];
    }
    setTimeout(() => this.reloadScale(), 2500);
  },
  methods: {
    moveTo(cityDict) {
      this.coordinates = cityDict;
      this.scale = 3;
      setTimeout(() => this.reloadScale(false), 0);
    },
    reloadScale(updatecords = true) {
      if (updatecords) {
        var loc = document.querySelector(
          "#gmap > div > div.vue-map > div > div > div:nth-child(15) > div > a"
        ).href;
        var match = loc.match(/\?ll=(-?[.\d]+),(-?[.\d]+)&z=([\d.]+)&/);
        this.coordinates = {
          lat: parseFloat(match[1]),
          lng: parseFloat(match[2]),
          zm: parseFloat(match[3]),
        };
      }
      var ow = document.getElementById("background").offsetWidth;
      var oh = document.getElementById("background").offsetHeight;
      var nw = ow * this.scale;
      var nh = oh * this.scale;
      //the downsizing is not centered, but the scaling after is. that's why it's offset.
      var tx = (ow - nw) / (2 / this.scale);
      var ty = (oh - nh) / (2 / this.scale);

      document.getElementById("gmap").style.width = Math.round(nw) + "px";
      document.getElementById("gmap").style.height = Math.round(nh) + "px";
      document.getElementById("gmap").style.transform = `scale(${1 / this.scale
        }) translate(${tx}px, ${ty}px)`;
    },
    async onFileChange(e) {
      this.uploadDone = false;
      this.status = "uploading file";
      this.errormsg = "";
      this.file = e.target.files[0];
      if (this.file.size > 10000000) {
        this.errormsg =
          "File too large. Don't worry we don't need the details for the design";
        return;
      }
      this.uploadFile();
      const photoUrl = URL.createObjectURL(this.file);
      const image = new Image();
      const imageDimensions = await new Promise((resolve) => {
        image.onload = () => {
          const dimensions = {
            height: image.height,
            width: image.width,
          };

          resolve(dimensions);
        };
        image.src = photoUrl;
        document.getElementById(
          "background"
        ).style.backgroundImage = `url(${photoUrl})`;
      });
      console.log(imageDimensions);
      if (imageDimensions.height > imageDimensions.width) {
        document.getElementById("background").style.width =
          "calc(90vw / 24 * 18)";
        document.getElementById("background").style.maxWidth =
          "calc(900px / 24 * 18)";
        document.getElementById("background").style.height = "90vw";
        document.getElementById("background").style.maxHeight = "900px";
      }
      setTimeout(() => this.reloadScale(false), 0);
    },
    uploadFile() {
      var formData = new FormData();
      formData.append("shopifyToken", this.shopifyToken);
      formData.append("file", document.getElementById("file").files[0]);
      formData.append("userId", App.store["user"]._id);
      var me = this;
      axios
        .post(vars.pixtures + "/api/v1/portrait", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          onUploadProgress: function (progressEvent) {
            this.uploadPercentage = parseInt(
              Math.round((progressEvent.loaded / progressEvent.total) * 100)
            );
            document.getElementById("preview-btn").style.backgroundImage =
              "linear-gradient(90deg, #0f476fbb " +
              (this.uploadPercentage - 1) +
              "%, #0f476f " +
              this.uploadPercentage +
              "%)";
          }.bind(this),
        })
        .then(function (response) {
          me.uploadDone = true;
          me.imageId = response.data._id;
        })
        .catch(function (error) {
          console.log(error);
          me.errormsg = error;
        });
    },
    getPreview() {
      this.previewUrl = "";
      this.mockupUrls = [];
      this.identifier = false;
      this.status = "Connecting with Google Maps";
      this.uploadPercentage = "";
      var me = this;
      setTimeout(function () {
        window.scrollBy({
          top: window.innerHeight * 0.7,
          left: 0,
          behavior: "smooth",
        });
      }, 50);
      setTimeout(function () {
        if (!me.mockUpDone) {
          me.status = "Preparing your custom map";
        }
      }, 4000);
      setTimeout(function () {
        if (!me.mockUpDone) {
          me.status = "Comparing both images";
        }
      }, 8000);
      setTimeout(function () {
        if (!me.mockUpDone) {
          me.status = "Calculating design estimate";
        }
      }, 12000);
      setTimeout(function () {
        if (!me.mockUpDone) {
          me.status = "Color grading";
        }
      }, 16000);

      console.log("starts render");
      let mapDiv = document.querySelector('div.vue-map');
      let a_tag = mapDiv.querySelectorAll('a[href*="google.com"]');
      var loc = a_tag[0].href;
      var match = loc.match(/\?ll=(-?[.\d]+),(-?[.\d]+)&z=([\d.]+)&/);
      console.log(match);
      let coordinates = {
        lat: match[1],
        lng: match[2],
        zm: match[3],
      };
      let body = coordinates;
      body["userId"] = App.store["user"]._id;
      body["imageId"] = this.imageId

      let ow = document.getElementById("background").offsetWidth;
      let oh = document.getElementById("background").offsetHeight;
      body["width"] = ow * this.scale;
      body["height"] = oh * this.scale;
      console.log(body);
      this.mockUpDone = false;
      axios
        .post(vars.pixtures + "/api/v1/generate", body,
          {
            headers: {
              "Content-Type": "application/json",
            },
          })
        .then((response) => {
          /*const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "render.png"); //or any other extension
          document.body.appendChild(link);
          link.click();*/
          me.identifier = response.data.id;
          me.previewUrl = response.data.preview;
          me.previewLocation = response.data.location;
          this.getMockUps();
        })
        .catch((error) => console.log(error));
    },
    getMockUps() {
      this.status = "Generating Mockups";
      var me = this;
      axios
        .get(vars.pixtures + "/api/v1/mockup/" + this.identifier)
        .then((response) => {
          me.mockupUrls = response.data.mockup;
          me.mockUpDone = true;
        })
        .catch((error) => console.log(error));
      setTimeout(function () {
        if (!me.mockUpDone) {
          me.status = "Finishing up";
        }
      }, 4000);
    },
    checkOut() {
      axios
        .post(vars.pixtures + "/printful/checkout", {
          token: VueCookie.get("session_token"),
          imageToken: this.imageId,
        })
        .then(alert("order created"));
    },
  },
  components: { GMap },
};
</script>


<style lang="scss" scoped>
#mockupContainer {
  width: calc(100% + 20px);
  margin-left: -10px;
  display: flex;
  flex-wrap: wrap;

  * {
    width: 100%;
    max-width: 500px;
    height: 100%;
    margin: 10px;
    background-size: contain;
    background-repeat: no-repeat;
  }
}

button {
  border-radius: 5px;
}

#loadingwrapper {
  width: 100%;
  height: 60vh;
  position: relative;
  margin: auto;
  display: flex;
}

#loadingbox {
  margin: auto;
  max-width: 300px;
  width: 60vw;
  max-height: 300px;
  height: 60vw;
  box-shadow: 0px 0px 18px #000b;
  border: none;
  position: relative;
  background: #0f476f;
  border-radius: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;

  #before {
    content: "";
    background-image: conic-gradient(rgb(255, 255, 255) 20deg,
        transparent 120deg);
    position: absolute;
    width: 150%;
    height: 150%;
    animation: rotate 3s linear infinite;
  }

  #after {
    width: 385px;
    background: #0f476fbb;
    height: 385px;
    border-radius: 12px;
    color: rgb(255, 255, 255);
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: inset 20px #0f476f;
    text-align: center;
  }

  @keyframes rotate {
    0% {
      transform: rotate(0deg);
    }

    100% {
      transform: rotate(-360deg);
    }
  }
}

.hori div.column {
  width: 100%;
  max-width: 700px;
}

.wrap {
  display: flex;
  flex-wrap: wrap;
}

.label {
  margin-bottom: 0px;
}

input#file {
  padding: 10px 0;
  width: 100%;
}

.cityQuicklinks {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  margin: 0 -3px;
}

.cityBtn {
  font-size: 0.9em;
  font-weight: 500;
  margin: 3px;
  border-radius: 30px;
  white-space: nowrap;
  width: min-content;
  padding: 5px 15px;
  background: #0f476f;

  a {
    color: #fff;
  }
}

#preview-btn {
  &:disabled {
    background: none;
    background-image: linear-gradient(#0f476fbb, #0f476fbb);
  }
}

.submit-btn {
  margin: 20px 0;
  font-size: 1.2em;
  padding: 10px;
  width: 100%;
}

#error {
  color: #ff0000;
}

.custom-file-input::-webkit-file-upload-button {
  visibility: hidden;
}

.custom-file-input::before {
  animation: MoveUpDown 1.5s ease-in-out infinite;
  content: "Select Image";
  display: inline-block;
  border: 3px solid #0f476f;
  border-radius: 8px;
  padding: 15px 25px;
  outline: none;
  white-space: nowrap;
  -webkit-user-select: none;
  cursor: pointer;
  text-shadow: 1px 1px #fff;
  font-weight: 700;
  font-size: 14pt;
}

.custom-file-input:hover::before {
  border-color: black;
}

.custom-file-input:active::before {
  background: -webkit-linear-gradient(top, #e3e3e3, #f9f9f9);
}

@keyframes MoveUpDown {

  0%,
  100% {
    transform: translateX(0);
  }

  33% {
    transform: translateX(5px);
  }
}

#background {
  width: 90vw;
  max-width: 900px;
  height: calc(90vw * 18 / 24);
  max-height: calc(900px * 18 / 24);
  display: block;
  background-size: cover;
  background-position: center center;
}

.wrapflow {
  margin-top: 150px;
}

#gmap {
  width: 100%;
  height: 100%;
  opacity: 0.65;
}

.rs-range {
  margin: 35px 0;
  padding: 0;
  width: 100%;
  -webkit-appearance: none;

  &:focus {
    outline: none;
  }

  &::-webkit-slider-runnable-track {
    width: 100%;
    height: 1px;
    cursor: pointer;
    box-shadow: none;
    background: #bbb;
    border-radius: 0px;
    border: 0px solid #010101;
  }

  &::-moz-range-track {
    width: 100%;
    height: 1px;
    cursor: pointer;
    box-shadow: none;
    background: #ddd;
    border-radius: 0px;
    border: 0px solid #010101;
  }

  &::-webkit-slider-thumb {
    box-shadow: none;
    border: 0px solid #0f476f;
    box-shadow: 0px 10px 10px rgba(0, 0, 0, 0.25);
    height: 32px;
    width: 14px;
    border-radius: 14px;
    background: #0f476f;
    cursor: pointer;
    -webkit-appearance: none;
    margin-top: -15px;
  }

  &::-moz-range-thumb {
    box-shadow: none;
    border: 0px solid #0f476f;
    box-shadow: 0px 10px 10px rgba(0, 0, 0, 0.25);
    height: 42px;
    width: 22px;
    border-radius: 22px;
    background: #0f476f;
    cursor: pointer;
    -webkit-appearance: none;
    margin-top: -20px;
  }

  &::-moz-focus-outer {
    border: 0;
  }
}

.cityname {
  display: block;
  color: #0f476f;

  font-size: calc(3vw + 50px);
  letter-spacing: 8px;
  font-family: "Poppins", sans-;
  position: absolute;
  top: 0px;
  left: 0px;

  &.special {
    background-image: repeating-linear-gradient(45deg,
        transparent 0,
        transparent 2.828px,
        #ccc 2.828px,
        #ccc 5.656px);
    -webkit-background-clip: text;
    color: transparent;
    transition: 0.5s;
  }
}

#cnbefore {
  z-index: 2;

  &:hover {
    transform: translate(-15px, -15px);
  }
}

#cnafter {
  z-index: -1;
}

#cnWrapper {
  margin-top: 100px;
  position: relative;
  height: 200px;
  width: 100%;

  &:hover #cnafter {
    transform: translate(15px, 15px);
  }
}
</style>