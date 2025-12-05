<template>
  <div class="edit-component">
    <h2>Edit {{ resourceType }}</h2>
    
    <div class="search-section">
      <div class="form-group">
        <label for="search-id">Item ID:</label>
        <input
          id="search-id"
          v-model="searchId"
          type="text"
          placeholder="Enter ID to edit"
        />
      </div>
      <button class="search-button" @click="fetchItem">Search</button>
    </div>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <form v-if="item" @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="content">Content:</label>
        <textarea
          id="content"
          v-model="item.content"
          rows="4"
          required
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="author">Author:</label>
        <input
          id="author"
          v-model="item.author"
          type="text"
          required
        />
      </div>
      
      <div v-if="resourceType === 'trivia'" class="form-group">
        <label for="question">Question:</label>
        <input
          id="question"
          v-model="item.question"
          type="text"
        />
      </div>
      
      <div v-if="resourceType === 'trivia'" class="form-group">
        <label for="answer">Answer:</label>
        <input
          id="answer"
          v-model="item.answer"
          type="text"
        />
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" v-model="item.approved" />
          Approved
        </label>
      </div>
      
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
      
      <div class="button-group">
        <button type="submit" class="submit-button" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
        <button type="button" class="cancel-button" @click="cancelEdit">
          Cancel
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  resourceType: string
}

const props = defineProps<Props>()

const searchId = ref('')
const item = ref<any>(null)
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const success = ref('')

const fetchItem = async () => {
  if (!searchId.value) {
    error.value = 'Please enter an ID'
    return
  }
  
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    // TODO: Replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Mock data
    item.value = {
      _id: searchId.value,
      content: `Sample ${props.resourceType} content`,
      author: 'John Doe',
      approved: false
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to fetch item'
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  saving.value = true
  error.value = ''
  success.value = ''
  
  try {
    // TODO: Replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    success.value = 'Item updated successfully!'
  } catch (err: any) {
    error.value = err.message || 'Failed to update item'
  } finally {
    saving.value = false
  }
}

const cancelEdit = () => {
  item.value = null
  searchId.value = ''
  error.value = ''
  success.value = ''
}
</script>

<style scoped>
.edit-component {
  padding: 1rem;
}

h2 {
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  text-transform: capitalize;
}

.search-section {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  margin-bottom: 2rem;
  max-width: 600px;
}

.search-section .form-group {
  flex: 1;
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

[data-theme="dark"] label {
  color: white;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

input[type="checkbox"] {
  margin-right: 0.5rem;
  cursor: pointer;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.search-button {
  background-color: #007bff;
  color: white;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.search-button:hover {
  background-color: #0056b3;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #667eea;
  font-size: 1.2rem;
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
  background-color: #ffc107;
  color: #212529;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.submit-button:hover:not(:disabled) {
  background-color: #e0a800;
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.cancel-button {
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

.cancel-button:hover {
  background-color: #5a6268;
}
</style>
