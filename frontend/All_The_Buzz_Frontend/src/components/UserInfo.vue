<template>
  <div class="user-info-card">
    <img :src="image" alt="User Image" class="user-image" />
    <div class="user-details">
      <div class="user-text">{{ text }}</div>
      <div class="user-name">{{ name }}</div>
      <div class="user-position">{{ position }} Bee</div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'UserInfo',
  props: {
    image: {
      type: String,
      required: true
    },
    text: {
      type: String,
      required: true
    },
    name: {
      type: String,
      required: true
    },
    position: {
      type: String,
      required: true
    }
  }
})
</script>

<style scoped>

.user-info-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #EE9500;
  padding: 1.5em 2em;
  box-shadow: 0 2px 12px rgba(0,0,0,0.12);
  color: #fff;
  min-width: 500px;
}
.user-image {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 2em;
  border: 3px solid #fff;
}
.user-details {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5em;
}
.user-text {
  font-size: 1.5em;
  opacity: 0.85;
  text-align: center;
}
.user-name {
  font-size: 2.0em;
  font-weight: bold;
  letter-spacing: 0.03em;
}
.user-position {
  font-size: 1.5em;
  font-style: italic;
  opacity: 0.8;
}
</style>
