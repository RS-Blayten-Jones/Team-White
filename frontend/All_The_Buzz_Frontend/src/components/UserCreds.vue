<template>
  <form class="user-creds" @submit.prevent="handleSubmit">
    <div class="form-group">
      <label for="username">Username</label>
      <input
        id="username"
        v-model="username"
        type="text"
        placeholder="Enter username"
        required
      />
    </div>
    
    <div class="form-group">
      <label for="password">Password</label>
      <input
        id="password"
        v-model="password"
        type="password"
        placeholder="Enter password"
        required
      />
    </div>
    
    <button type="submit" class="submit-button">
      {{ submitLabel }}
    </button>
    
    <p v-if="error" class="error-message">{{ error }}</p>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  submitLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  submitLabel: 'Login'
})

const emit = defineEmits<{
  login: [credentials: { username: string; password: string }]
}>()

const username = ref('')
const password = ref('')
const error = ref('')

// function setCookie(name: string, value: string, maxAgeSeconds?: number){
//   const parts = [`${name}=${encodeURIComponent(value)}`, 'path=/']
//   if (maxAgeSeconds) {
//     parts.push(`max-age=${maxAgeSeconds}`) //max age is how long it takes the cookie to expire
//   }
//   document.cookie = parts.join('; ')
// }

const handleSubmit = () => {
  error.value = ''
  
  if (!username.value || !password.value) {
    error.value = 'Please enter both username and password'
    return
  }
  
  emit('login', {
    username: username.value,
    password: password.value
  })

}
</script>

<style scoped>
.user-creds {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-group {
  text-align: left;
}

label {
  display: block;
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
  font-size: var(--font-size-sm);
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  color: var(--text-primary);
  background-color: var(--bg-secondary);
  transition: border-color var(--transition-base), background-color var(--transition-base), color var(--transition-base);
}

input:hover {
  border-color: var(--color-gray-400);
}

input:focus {
  border-color: var(--color-primary-purple);
  outline: 3px solid rgba(71, 57, 124, 0.2);
  outline-offset: 0;
}

.submit-button {
  background-color: var(--color-primary-purple);
  color: var(--text-on-primary);
  padding: 0.75rem;
  border: none;
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  cursor: pointer;
  transition: all var(--transition-base);
  margin-top: var(--spacing-sm);
  width: 100%;
}

.submit-button:hover {
  background-color: #3a2e63;
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.submit-button:focus {
  outline: 3px solid var(--color-primary-orange);
  outline-offset: 2px;
}

.error-message {
  color: var(--color-error);
  font-size: var(--font-size-sm);
  margin: 0;
  text-align: center;
  font-weight: var(--font-weight-medium);
}
</style>
