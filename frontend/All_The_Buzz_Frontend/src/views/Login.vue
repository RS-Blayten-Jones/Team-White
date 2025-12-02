<template>
  <div class="login-container">
    <div class="login-card">
      <h1>All The Buzz</h1>
      <h2>Login</h2>
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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 350px;
  text-align: center;
}

h1 {
  color: #667eea;
  margin-bottom: 0.5rem;
  font-size: 2rem;
}

h2 {
  color: #333;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}
</style>
