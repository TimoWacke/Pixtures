<template>
  <div class="container">
    <br>
    <h1>CityCanvas</h1>
    <div class="cta container">
      <a href="/create">
        <button>Try it yourself</button>
      </a>
    </div>
    <div class="gallery">
      <div class="image-container" v-for="url in imageUrls" :key="url">
        <img :src="url" @click="goToArtPiece(url)" />
        <button class="delete-btn" @click="deleteImage(url)" v-if="this.$route.href.includes('delete')">
          Delete
        </button>
      </div>
    </div>
    <div class="cta container">
      <a href="/create">
        <button>Try it yourself</button>
      </a>
    </div>
  </div>
</template>

<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@1,900&display=swap");
</style>

<script>
import axios from "axios";

export default {
  name: "Landing-Site",
  data() {
    return {
      imageUrls: [],
    };
  },
  mounted() {
    axios
      .get(process.env.VUE_APP_BACKEND_URL + "/api/v1/artpiece/highlights")
      .then((response) => {
        this.imageUrls = response.data;
      })
      .catch((error) => {
        console.error(error);
      });
  },
  methods: {
    deleteImage(url) {
      if (confirm("Are you sure you want to delete this image?")) {
        axios.delete(url).then(() => {
          this.imageUrls = this.imageUrls.filter((item) => item !== url);
        });
      }
    },
    goToArtPiece(url) {
      const imageId = url.split("/").pop(); // Extract image ID from URL
      this.$router.push({ name: "ArtPiece", params: { id: imageId } });
    },
  },
};
</script>

<style lang="scss" scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@1,900&display=swap");

.gallery {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.cta.container {
  display: flex;
  flex-direction: column;
  align-items: center;

  button {
    padding: 10px 20px;
    font-size: 20px;
    font-family: "Poppins", sans-serif;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
}

img {
  border-radius: 5px;
  transition: ease-in-out 0.3s;
  height: 100%;
  width: auto;
}

.image-container {

  position: relative; /* Needed for the absolute positioning of the button */
  height: 300px;
}

img:hover {
  filter: brightness(0.8);
}

.delete-btn {

  position: absolute; /* Positions button relative to .image-container */
  top: 10px;
  right: 10px;
  padding: 5px 10px;
  font-size: 12px;
  color: white;
  background-color: rgba(255, 0, 0, 0.8);
  border: none;
  border-radius: 5px;
  cursor: pointer;
  display: none; /* Initially hidden */
}

.image-container:hover .delete-btn {
  display: block; /* Shows the button on hover of .image-container */
}
</style>
