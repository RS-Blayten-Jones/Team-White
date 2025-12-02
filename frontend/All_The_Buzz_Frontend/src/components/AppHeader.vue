<template>
  <header class="app-header" role="banner">
    <div class="app-header-content">
      <h1 class="app-header-title">{{ displayTitle }}</h1>
      <nav class="app-header-nav" role="navigation" aria-label="Main navigation">
        <button 
          class="btn btn-neutral btn-sm theme-toggle" 
          @click="toggleTheme"
          :aria-label="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'"
        >
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
        <button 
          v-if="showMenuButton"
          class="btn btn-neutral btn-sm back-button" 
          @click="goToMenu"
          aria-label="Back to menu"
        >
          ← Menu
        </button>
        <button 
          class="btn btn-danger btn-sm logout-button" 
          @click="logout"
          aria-label="Logout"
        >
          Logout
        </button>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { computed, ref, onMounted } from 'vue'

interface Props {
  title?: string
}

const props = defineProps<Props>()

const router = useRouter()
const route = useRoute()
const isDarkMode = ref(false)

const displayTitle = computed(() => props.title || 'All The Buzz')

const showMenuButton = computed(() => route.name !== 'resource-menu')

onMounted(() => {
  // Check for saved theme preference or default to light mode
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkMode.value = true
    document.documentElement.setAttribute('data-theme', 'dark')
  }
})

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  const theme = isDarkMode.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

const goToMenu = () => {
  router.push({ name: 'resource-menu' })
}

const logout = () => {
  // TODO: Implement logout logic
  router.push({ name: 'login' })
}
</script>

<style scoped>
.app-header {
  background-color: var(--color-primary-orange);
  color: var(--text-on-dark);
  padding: var(--spacing-lg) var(--spacing-xl);
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 100;
}

.app-header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--spacing-md);
}

.app-header-title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-on-dark);
  margin: 0;
}

.app-header-nav {
  display: flex;
  gap: var(--spacing-md);
  align-items: center;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: var(--font-size-sm);
}

.theme-toggle {
  font-size: 1.2rem;
  padding: 0.5rem 0.75rem;
  min-width: unset;
}

.back-button,
.logout-button {
  white-space: nowrap;
}

@media (max-width: 768px) {
  .app-header {
    padding: var(--spacing-md);
  }
  
  .app-header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .app-header-title {
    font-size: var(--font-size-xl);
  }
  
  .app-header-nav {
    width: 100%;
    justify-content: center;
  }
}
</style>
