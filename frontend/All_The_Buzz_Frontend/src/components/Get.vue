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
  padding: var(--spacing-md);
}

h2 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
  text-transform: capitalize;
  font-size: var(--font-size-2xl);
}

.filters {
  display: flex;
  gap: var(--spacing-md);
  align-items: flex-end;
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
}

.filters select,
.filters input {
  padding: 0.5rem 0.75rem;
}

.fetch-button {
  background-color: var(--color-success);
  color: var(--text-on-primary);
  padding: 0.5rem 1.5rem;
  border: none;
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-base);
  white-space: nowrap;
}

.fetch-button:hover {
  background-color: #047857;
  transform: translateY(-1px);
}

.fetch-button:focus {
  outline: 3px solid var(--color-primary-orange);
  outline-offset: 2px;
}

.error {
  background-color: var(--color-error-light);
  color: var(--color-error);
  border: 1px solid var(--color-error);
  padding: var(--spacing-md);
  border-radius: var(--border-radius-md);
  margin-bottom: var(--spacing-md);
  font-weight: var(--font-weight-medium);
}

.results h3 {
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
  font-size: var(--font-size-xl);
}

.items-grid {
  display: grid;
  gap: var(--spacing-md);
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.item-card {
  background-color: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
  transition: box-shadow var(--transition-base), background-color var(--transition-base);
}

.item-card:hover {
  box-shadow: var(--shadow-md);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid var(--border-color);
}

.item-id {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  font-weight: var(--font-weight-semibold);
}

.item-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: var(--font-size-xs);
  font-weight: var(--font-weight-semibold);
  text-transform: uppercase;
}

.item-status.approved {
  background-color: var(--color-success-light);
  color: var(--color-success);
}

.item-status.pending {
  background-color: var(--color-warning-light);
  color: var(--color-warning);
}

.item-content p {
  margin: var(--spacing-sm) 0;
  color: var(--text-primary);
  line-height: 1.6;
}
</style>
