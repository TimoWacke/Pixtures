<template>
  <div class="container">
    <br />
    <h1>CityCanvas</h1>
    <div class="cta container">
      <a href="/create">
        <button>Try it yourself</button>
      </a>
    </div>
    <div class="gallery">
      <div class="image-container" v-for="url in imageUrls" :key="url">
        <img :src="`${url}?y=300`" @click="goToArtPiece(url)" />

        <!-- Action buttons container -->
        <div class="action-buttons">

          <!-- Like button with Heart Icon -->
          <button class="like-btn" @click="likeImage(url)">
            <i class="fa fa-heart"></i>
          </button>

          <!-- Delete button with Trash Icon -->
          <button class="delete-btn" @click="deleteImage(url)" v-if="this.$route.href.includes('delete')">
            <i class="fa fa-trash"></i>
          </button>

        </div>
      </div>
    </div>
    <div class="cta container">
      <a href="/create">
        <button>Try it yourself</button>
      </a>
    </div>
  </div>
</template>


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
      const imageId = url.split("/").pop(); // Extract image ID from URL
      if (confirm("Are you sure you want to delete this image?")) {
        axios.delete(`${process.env.VUE_APP_BACKEND_URL}/api/v1/artpiece/like/${imageId}`).then(() => {
          this.imageUrls = this.imageUrls.filter((item) => item !== url);
        });
      }
    },
    likeImage(url) {
      const imageId = url.split("/").pop(); // Extract image ID from URL
      axios.post(`${process.env.VUE_APP_BACKEND_URL}/api/v1/artpiece/like/${imageId}`)
        .then(response => {
          // Handle successful like action, e.g., show a notification or update state
          console.log("Image liked:", response.data);
        })
        .catch(error => {
          console.error("Error liking image:", error);
        });
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

$primary: #0f476f;
$secondary: #ff049b;

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
  position: relative;
  height: 300px;
}

img:hover {
  filter: brightness(0.8);
}

/* Center the action buttons inside the image */
.action-buttons {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: none;
  gap: 15px;
}

.image-container:hover {
  .action-buttons {
    display: flex;
  }
}

/* Style for the delete button */
.delete-btn,
.like-btn {
  background: rgba(67, 67, 67, 0.4);
  /* Semi-transparent background */
  border: none;
  border-radius: 50%;
  /* Circular buttons */
  padding: 15px;
  font-size: 20px;
  color: rgba(230, 230, 230, 0.7);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease
}

.delete-btn:hover {
  background: $primary;
}


.like-btn:hover {
  background: $primary;
}

/* Font Awesome icons */
.delete-btn i,
.like-btn i {
  font-size: 20px;
}

/* Optional: Add hover effect to buttons */
.action-buttons button:hover {
  transform: scale(1.1);


  color: white;


  /* Slight zoom effect on hover */
}
</style>
