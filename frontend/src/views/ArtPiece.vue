<template>
  <div class="container">
    <h1>Art Piece</h1>
    <div class="carousel">
      <div class="main-image-container">
        <img :src="currentImageUrl" class="main-image" />
      </div>
      <div class="thumbnail-gallery" v-if="allImages.length > 1">
        <img
          v-for="(url, index) in allImages"
          :key="index"
          :src="url"
          :class="{ active: currentImageUrl === url }"
          class="thumbnail-image"
          @click="setCurrentImage(url)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ArtPiece",
  data() {
    return {
      additionalImages: [],
      mainImageUrl: "",
      currentImageUrl: ""
    };
  },
  computed: {
    allImages() {
      // Combine the main image with additional images for the carousel
      return [...this.additionalImages, this.mainImageUrl].filter((url) => url);
    },
  },
  mounted() {
    const imageId = this.$route.params.id; // Get the image ID from route params
    const endpoint = `${process.env.VUE_APP_BACKEND_URL}/api/v1/mockup/${imageId}`;

    // Initially show the normal image while mockups load
    this.mainImageUrl = `${process.env.VUE_APP_BACKEND_URL}/api/v1/artpiece/${imageId}`;
    this.currentImageUrl = this.mainImageUrl;

    // Fetch the mockup images
    axios
      .get(endpoint)
      .then((response) => {
        this.additionalImages = response.data
        this.currentImageUrl = this.additionalImages[0];
      })
      .catch((error) => {
        console.error(error);
      });
  },
  methods: {
    setCurrentImage(url) {
      // Change the large image based on user selection
      this.currentImageUrl = url;
    },
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.carousel {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.main-image-container {
  margin: 20px 0;
}

.main-image {
  max-height: 66vh;
  width: auto;
  border-radius: 10px;
  transition: transform 0.3s ease;
}

.thumbnail-gallery {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 10px;
}

.thumbnail-image {
  width: auto;
  height: 100px;
  border-radius: 5px;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.thumbnail-image.active {
  opacity: 1;
  transform: scale(1.1);
}

.thumbnail-image:hover {
  opacity: 1;
  transform: scale(1.1);
}
</style>
