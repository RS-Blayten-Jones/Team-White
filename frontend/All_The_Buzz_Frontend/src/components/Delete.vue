<template>
  <div class="delete-component">
    <h2>Delete {{ resourceType }}</h2>
    
    <div class="warning-box">
      <strong>⚠️ Warning:</strong> Deletion is permanent and cannot be undone.
    </div>
    
    <div class="search-section">
      <div class="form-group">
        <label for="delete-id">Item ID:</label>
        <input
          id="delete-id"
          v-model="searchId"
          type="text"
          placeholder="Enter ID to delete"
        />
      </div>
      <button class="search-button" @click="fetchItem">Search</button>
    </div>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-if="item" class="item-preview">
      <h3>Item Preview</h3>
      <div class="item-details">
        <p><strong>ID:</strong> {{ item._id }}</p>
        <p><strong>Content:</strong> {{ item.content }}</p>
        <p><strong>Author:</strong> {{ item.author }}</p>
        <p><strong>Status:</strong> {{ item.approved ? 'Approved' : 'Pending' }}</p>
      </div>
      
      <div v-if="error" class="error">{{ error }}</div>
      <div v-if="success" class="success">{{ success }}</div>
      
      <div class="button-group">
        <button class="delete-button" @click="handleDelete" :disabled="deleting">
          {{ deleting ? 'Deleting...' : 'Delete Item' }}
        </button>
        <button class="cancel-button" @click="cancelDelete">
          Cancel
        </button>
      </div>
    </div>
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
const deleting = ref(false)
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
      approved: true
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to fetch item'
  } finally {
    loading.value = false
  }
}

const handleDelete = async () => {
  if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
    return
  }
  
  deleting.value = true
  error.value = ''
  success.value = ''
  
  try {
    // TODO: Replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    success.value = 'Item deleted successfully!'
    setTimeout(() => {
      cancelDelete()
    }, 2000)
  } catch (err: any) {
    error.value = err.message || 'Failed to delete item'
  } finally {
    deleting.value = false
  }
}

const cancelDelete = () => {
  item.value = null
  searchId.value = ''
  error.value = ''
  success.value = ''
}
</script>

<style scoped>
.delete-component {
  padding: 1rem;
}

h2 {
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  text-transform: capitalize;
}

.warning-box {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  color: #856404;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 2rem;
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

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus {
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

.item-preview {
  max-width: 600px;
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #dee2e6;
}

.item-preview h3 {
  color: #333;
  margin-bottom: 1rem;
}

.item-details p {
  margin: 0.5rem 0;
  color: #333;
  line-height: 1.6;
}

.error {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.success {
  background-color: #d4edda;
  color: #155724;
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.delete-button {
  background-color: #dc3545;
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.delete-button:hover:not(:disabled) {
  background-color: #c82333;
}

.delete-button:disabled {
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
