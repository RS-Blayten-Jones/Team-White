<template>
  <div class="image-banner">
    <img :src="src" alt="Banner" class="banner-img" />
    <div class="overlay-text">
      <span>{{ text }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ImageBanner',
  props: {
    src: {
      type: String,
      required: true
    },
    text: {
      type: String,
      required: true
    },
    outlineColor: {
      type: String,
      default: '#007bff' // Default outline color
    }
  }
})
</script>

<style scoped>
.image-banner {
  position: relative;
  width: 100vw;
  aspect-ratio: 6 / 1.5;
  overflow: hidden;
}
.banner-img {
  width: 100vw;
  height: 100%;
  object-fit: cover;
  display: block;
}
.overlay-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 2;
}
.overlay-text span {
  color: white;
  font-weight: bold;
  font-size: 6vw;
  text-transform: uppercase;
  padding: 0.05em 0.05em;
  
  letter-spacing: 0.1em;
  
}

</style>
