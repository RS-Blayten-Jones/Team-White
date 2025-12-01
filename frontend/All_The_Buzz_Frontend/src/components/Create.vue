<template>
  <div class="create-component">
    <h2>Create New {{ resourceType }}</h2>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea
          id="content"
          v-model="formData.content"
          rows="4"
          placeholder="Enter content..."
          required
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="author">Author:</label>
        <input
          id="author"
          v-model="formData.author"
          type="text"
          placeholder="Enter author name"
          required
        />
      </div>
      
      <div v-if="resourceType === 'trivia'" class="form-group">
        <label for="question">Question:</label>
        <input
          id="question"
          v-model="formData.question"
          type="text"
          placeholder="Enter question"
        />
      </div>
      
      <div v-if="resourceType === 'trivia'" class="form-group">
        <label for="answer">Answer:</label>
        <input
          id="answer"
          v-model="formData.answer"
          type="text"
          placeholder="Enter answer"
        />
      </div>
      
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
      
      <div class="button-group">
        <button type="submit" class="submit-button" :disabled="loading">
          {{ loading ? 'Creating...' : 'Create' }}
        </button>
        <button type="button" class="reset-button" @click="resetForm">
          Reset
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

interface Props {
  resourceType: string
}

const props = defineProps<Props>()

const formData = reactive({
  content: '',
  author: '',
  question: '',
  answer: ''
})

const loading = ref(false)
const error = ref('')
const success = ref('')

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    // TODO: Replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    success.value = `${props.resourceType} created successfully!`
    resetForm()
  } catch (err: any) {
    error.value = err.message || 'Failed to create item'
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  formData.content = ''
  formData.author = ''
  formData.question = ''
  formData.answer = ''
  error.value = ''
  success.value = ''
}
</script>

<style scoped>
.create-component {
  padding: 1rem;
}

h2 {
  color: #333;
  margin-bottom: 1.5rem;
  text-transform: capitalize;
}

form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-weight: 600;
  color: #555;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

input,
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.success {
  background-color: #d4edda;
  color: #155724;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.button-group {
  display: flex;
  gap: 1rem;
}

.submit-button {
  background-color: #28a745;
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.submit-button:hover:not(:disabled) {
  background-color: #218838;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.reset-button {
  background-color: #6c757d;
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.reset-button:hover {
  background-color: #5a6268;
}
</style>
