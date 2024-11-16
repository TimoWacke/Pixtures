<template>
  <div>
    <img v-for="url in imageUrls" :src="url" />
  </div>
  <button href="/create">Try it yourself</button>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@1,900&display=swap");
</style>

<script>
import axios from "axios";
import vars from "../assets/vars";

export default {
  name: "Landing",
  data() {
    return {
      imageUrls: []
    }
  },
  mounted() {
    try {
      me = this;
      axios
        .get(vars.pixtures + "/artpiece/list")
        .then((response) => {
          me.imageUrls = response.data;
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
      formData.append("userId", this.userId);
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
      body["userId"] = this.userId;
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
          me.mockupUrls = response.data;
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