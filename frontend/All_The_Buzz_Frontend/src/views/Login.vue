<template>
  <div class="login-page">
    <div class="login-card card">
      <h1 class="login-title">All The Buzz</h1>
      <h2 class="login-subtitle">Login</h2>
      <UserCreds @login="handleLogin" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import UserCreds from '@/components/UserCreds.vue'

const router = useRouter()

const handleLogin = (credentials: { username: string; password: string }) => {
  // TODO: Implement actual authentication logic
  console.log('Login attempt:', credentials)
  
  // For now, navigate to ResourceMenu on any login attempt
  router.push({ name: 'resource-menu' })
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: var(--color-primary-purple);
  padding: var(--spacing-md);
}

.login-card {
  min-width: 400px;
  max-width: 450px;
  width: 100%;
  text-align: center;
}

.login-title {
  color: var(--color-primary-purple);
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-4xl);
}

.login-subtitle {
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xl);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
}

@media (max-width: 768px) {
  .login-card {
    min-width: unset;
  }
  
  .login-title {
    font-size: var(--font-size-3xl);
  }
  
  .login-subtitle {
    font-size: var(--font-size-xl);
  }
}
</style>
