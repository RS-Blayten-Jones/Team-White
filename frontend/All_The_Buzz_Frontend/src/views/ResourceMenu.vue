<template>
  <div class="resource-menu">
    <h1>All The Buzz - Resource Menu</h1>
    <p class="subtitle">Select a resource to manage</p>
    
    <div class="resource-grid">
      <div class="resource-card" @click="navigateTo('jokes')">
        <div class="resource-icon">😂</div>
        <h2>Jokes</h2>
        <p>Manage jokes database</p>
      </div>
      
      <div class="resource-card" @click="navigateTo('bios')">
        <div class="resource-icon">👤</div>
        <h2>Bios</h2>
        <p>Manage bios database</p>
      </div>
      
      <div class="resource-card" @click="navigateTo('trivia')">
        <div class="resource-icon">🎯</div>
        <h2>Trivia</h2>
        <p>Manage trivia database</p>
      </div>
      
      <div class="resource-card" @click="navigateTo('quotes')">
        <div class="resource-icon">💬</div>
        <h2>Quotes</h2>
        <p>Manage quotes database</p>
      </div>
    </div>
    
    <button class="logout-button" @click="logout">Logout</button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateTo = (resource: string) => {
  router.push({ name: resource })
}

const logout = () => {
  // TODO: Implement logout logic
  router.push({ name: 'login' })
}
</script>

<style scoped>
.resource-menu {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

h1 {
  color: #667eea;
  margin-bottom: 0.5rem;
  font-size: 2.5rem;
}

.subtitle {
  color: #666;
  margin-bottom: 3rem;
  font-size: 1.2rem;
}

.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.resource-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.resource-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.resource-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.resource-card h2 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.5rem;
}

.resource-card p {
  color: #666;
  font-size: 1rem;
}

.logout-button {
  background-color: #dc3545;
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.logout-button:hover {
  background-color: #c82333;
}
</style>
