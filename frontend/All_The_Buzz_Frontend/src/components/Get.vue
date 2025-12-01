<template>
  <div class="get-component">
    <h2>Get {{ resourceType }}</h2>
    
    <div class="filters">
      <div class="form-group">
        <label for="filter-type">Filter By:</label>
        <select id="filter-type" v-model="filterType">
          <option value="all">All</option>
          <option value="id">By ID</option>
          <option value="random">Random</option>
        </select>
      </div>
      
      <div v-if="filterType === 'id'" class="form-group">
        <label for="item-id">Item ID:</label>
        <input
          id="item-id"
          v-model="itemId"
          type="text"
          placeholder="Enter ID"
        />
      </div>
      
      <button class="fetch-button" @click="fetchData">
        {{ filterType === 'random' ? 'Get Random' : 'Fetch' }}
      </button>
    </div>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-if="error" class="error">{{ error }}</div>
    
    <div v-if="items.length > 0" class="results">
      <h3>Results ({{ items.length }})</h3>
      <div class="items-grid">
        <div v-for="item in items" :key="item._id" class="item-card">
          <div class="item-header">
            <span class="item-id">ID: {{ item._id }}</span>
            <span :class="['item-status', item.approved ? 'approved' : 'pending']">
              {{ item.approved ? 'Approved' : 'Pending' }}
            </span>
          </div>
          <div class="item-content">
            <p v-if="item.content">{{ item.content }}</p>
            <p v-if="item.name"><strong>Name:</strong> {{ item.name }}</p>
            <p v-if="item.author"><strong>Author:</strong> {{ item.author }}</p>
            <p v-if="item.question"><strong>Question:</strong> {{ item.question }}</p>
            <p v-if="item.answer"><strong>Answer:</strong> {{ item.answer }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="!loading && !error" class="no-results">
      No items to display. Click "Fetch" to load data.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  resourceType: string
}

const props = defineProps<Props>()

const filterType = ref('all')
const itemId = ref('')
const items = ref<any[]>([])
const loading = ref(false)
const error = ref('')

const fetchData = async () => {
  loading.value = true
  error.value = ''
  items.value = []
  
  try {
    // TODO: Replace with actual API calls
    await new Promise(resolve => setTimeout(resolve, 500)) // Simulate API delay
    
    // Mock data for demonstration
    items.value = [
      {
        _id: '1',
        content: `Sample ${props.resourceType} content`,
        approved: true,
        author: 'John Doe'
      },
      {
        _id: '2',
        content: `Another ${props.resourceType} example`,
        approved: false,
        author: 'Jane Smith'
      }
    ]
  } catch (err: any) {
    error.value = err.message || 'Failed to fetch data'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.get-component {
  padding: 1rem;
}

h2 {
  color: #333;
  margin-bottom: 1.5rem;
  text-transform: capitalize;
}

.filters {
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  color: #555;
  font-size: 0.9rem;
}

select,
input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.fetch-button {
  background-color: #28a745;
  color: white;
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.fetch-button:hover {
  background-color: #218838;
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

.no-results {
  text-align: center;
  padding: 3rem;
  color: #6c757d;
  font-size: 1.1rem;
}

.results h3 {
  color: #333;
  margin-bottom: 1rem;
}

.items-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.item-card {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1rem;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #dee2e6;
}

.item-id {
  font-size: 0.85rem;
  color: #6c757d;
  font-weight: 600;
}

.item-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.item-status.approved {
  background-color: #d4edda;
  color: #155724;
}

.item-status.pending {
  background-color: #fff3cd;
  color: #856404;
}

.item-content p {
  margin: 0.5rem 0;
  color: #333;
  line-height: 1.5;
}
</style>
