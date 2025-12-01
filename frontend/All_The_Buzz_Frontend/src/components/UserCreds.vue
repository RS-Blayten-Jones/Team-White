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
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: left;
}

label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.submit-button {
  background-color: #667eea;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 0.5rem;
}

.submit-button:hover {
  background-color: #5568d3;
}

.error-message {
  color: #dc3545;
  font-size: 0.9rem;
  margin: 0;
  text-align: center;
}
</style>
