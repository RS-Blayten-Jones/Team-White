<template>
  <div class="resource-menu-page page-container">
    <AppHeader title="All The Buzz - Resource Menu" />
    
    <div class="resource-menu-content content-wrapper">
      <div class="menu-header">
      </div>
      
      <div class="resource-grid">
        <div 
          class="resource-card card card-jokes" 
          @click="navigateTo('jokes')"
          tabindex="0"
          role="button"
          @keydown.enter="navigateTo('jokes')"
          @keydown.space.prevent="navigateTo('jokes')"
        >
          <div class="resource-icon" aria-hidden="true">😂</div>
          <h2>Jokes</h2>
          <p>Manage jokes database</p>
        </div>
        
        <div 
          class="resource-card card card-bios" 
          @click="navigateTo('bios')"
          tabindex="0"
          role="button"
          @keydown.enter="navigateTo('bios')"
          @keydown.space.prevent="navigateTo('bios')"
        >
          <div class="resource-icon" aria-hidden="true">👤</div>
          <h2>Bios</h2>
          <p>Manage bios database</p>
        </div>
        
        <div 
          class="resource-card card card-trivia" 
          @click="navigateTo('trivia')"
          tabindex="0"
          role="button"
          @keydown.enter="navigateTo('trivia')"
          @keydown.space.prevent="navigateTo('trivia')"
        >
          <div class="resource-icon" aria-hidden="true">🎯</div>
          <h2>Trivia</h2>
          <p>Manage trivia database</p>
        </div>
        
        <div 
          class="resource-card card card-quotes" 
          @click="navigateTo('quotes')"
          tabindex="0"
          role="button"
          @keydown.enter="navigateTo('quotes')"
          @keydown.space.prevent="navigateTo('quotes')"
        >
          <div class="resource-icon" aria-hidden="true">💬</div>
          <h2>Quotes</h2>
          <p>Manage quotes database</p>
        </div>
      </div>
      
      <div class="menu-footer">
        <button class="btn btn-danger logout-button" @click="logout">Logout</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'

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
.resource-menu-page {
  background-color: var(--bg-primary);
  min-height: 100vh;
}

.resource-menu-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: var(--spacing-xl);
}

.menu-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.menu-subtitle {
  color: var(--text-secondary);
  font-size: var(--font-size-xl);
  margin: 0;
}

.resource-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-xl);
  margin-bottom: var(--spacing-2xl);
  max-width: 1200px;
  width: 100%;
}

.resource-card {
  text-align: center;
  cursor: pointer;
  transition: transform var(--transition-base), box-shadow var(--transition-base);
  padding: var(--spacing-xl);
  min-height: 220px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-top: 4px solid transparent;
  position: relative;
}

.resource-card:hover,
.resource-card:focus {
  transform: translateY(-8px);
  box-shadow: var(--shadow-xl);
  outline: none;
}

.resource-card:focus {
  outline: 3px solid var(--color-primary-orange);
  outline-offset: 2px;
}

/* Individual card colors */
.card-jokes {
  border-top-color: var(--color-primary-orange);
}

.card-jokes:hover,
.card-jokes:focus,
.card-jokes:active {
  background-color: rgba(238, 149, 0, 0.1);
  border-top-width: 6px;
}

.card-jokes:hover h2,
.card-jokes:focus h2,
.card-jokes:active h2 {
  color: var(--color-primary-orange);
}

.card-bios {
  border-top-color: var(--color-primary-purple);
}

.card-bios:hover,
.card-bios:focus,
.card-bios:active {
  background-color: rgba(71, 57, 124, 0.1);
  border-top-width: 6px;
}

.card-bios:hover h2,
.card-bios:focus h2,
.card-bios:active h2 {
  color: var(--color-primary-purple);
}

.card-trivia {
  border-top-color: var(--color-primary-magenta);
}

.card-trivia:hover,
.card-trivia:focus,
.card-trivia:active {
  background-color: rgba(171, 57, 121, 0.1);
  border-top-width: 6px;
}

.card-trivia:hover h2,
.card-trivia:focus h2,
.card-trivia:active h2 {
  color: var(--color-primary-magenta);
}

.card-quotes {
  border-top-color: var(--color-primary-dark);
}

.card-quotes:hover,
.card-quotes:focus,
.card-quotes:active {
  background-color: rgba(0, 46, 75, 0.1);
  border-top-width: 6px;
}

.card-quotes:hover h2,
.card-quotes:focus h2,
.card-quotes:active h2 {
  color: var(--color-primary-dark);
}

.resource-icon {
  font-size: 5rem;
  margin-bottom: var(--spacing-md);
  line-height: 1;
}

.resource-card h2 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-2xl);
  transition: color var(--transition-base);
}

.resource-card p {
  color: var(--text-secondary);
  font-size: var(--font-size-base);
  margin: 0;
}

.menu-footer {
  text-align: center;
}

.logout-button {
  padding: var(--spacing-md) var(--spacing-2xl);
  font-size: var(--font-size-lg);
}

/* Responsive Design */
@media (max-width: 1200px) {
  .resource-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .resource-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .menu-title {
    font-size: var(--font-size-3xl);
  }
  
  .menu-subtitle {
    font-size: var(--font-size-lg);
  }
  
  .resource-card {
    min-height: 180px;
  }
  
  .resource-icon {
    font-size: 4rem;
  }
}
</style>
