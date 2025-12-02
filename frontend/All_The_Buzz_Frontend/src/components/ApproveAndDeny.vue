<template>
  <div class="approve-deny-component">
    <h2>Approve/Deny {{ resourceType }}</h2>
    
    <div class="info-box">
      <strong>ℹ️ Info:</strong> Review and approve or deny pending items.
    </div>
    
    <div class="filters">
      <button
        :class="['filter-button', { active: filter === 'pending' }]"
        @click="filter = 'pending'"
      >
        Pending
      </button>
      <button
        :class="['filter-button', { active: filter === 'approved' }]"
        @click="filter = 'approved'"
      >
        Approved
      </button>
      <button
        :class="['filter-button', { active: filter === 'all' }]"
        @click="filter = 'all'"
      >
        All
      </button>
      <button class="refresh-button" @click="fetchItems">
        🔄 Refresh
      </button>
    </div>
    
    <div v-if="loading" class="loading">Loading...</div>
    
    <div v-if="error" class="error">{{ error }}</div>
    
    <div v-if="filteredItems.length > 0" class="items-list">
      <div v-for="item in filteredItems" :key="item._id" class="item-card">
        <div class="item-header">
          <span class="item-id">ID: {{ item._id }}</span>
          <span :class="['item-status', item.approved ? 'approved' : 'pending']">
            {{ item.approved ? 'Approved' : 'Pending' }}
          </span>
        </div>
        
        <div class="item-content">
          <p v-if="item.content"><strong>Content:</strong> {{ item.content }}</p>
          <p v-if="item.author"><strong>Author:</strong> {{ item.author }}</p>
          <p v-if="item.question"><strong>Question:</strong> {{ item.question }}</p>
          <p v-if="item.answer"><strong>Answer:</strong> {{ item.answer }}</p>
        </div>
        
        <div class="item-actions">
          <button
            v-if="!item.approved"
            class="approve-button"
            @click="approveItem(item._id)"
          >
            ✓ Approve
          </button>
          <button
            v-if="item.approved"
            class="deny-button"
            @click="denyItem(item._id)"
          >
            ✗ Revoke
          </button>
        </div>
      </div>
    </div>
    
    <div v-else-if="!loading" class="no-results">
      No {{ filter }} items found.
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Props {
  resourceType: string
}

const props = defineProps<Props>()

const items = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const filter = ref('pending')

const filteredItems = computed(() => {
  if (filter.value === 'all') return items.value
  if (filter.value === 'approved') return items.value.filter(item => item.approved)
  return items.value.filter(item => !item.approved)
})

const fetchItems = async () => {
  loading.value = true
  error.value = ''
  
  try {
    // TODO: Replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // Mock data
    items.value = [
      {
        _id: '1',
        content: `Approved ${props.resourceType} content`,
        author: 'John Doe',
        approved: true
      },
      {
        _id: '2',
        content: `Pending ${props.resourceType} content`,
        author: 'Jane Smith',
        approved: false
      },
      {
        _id: '3',
        content: `Another pending ${props.resourceType}`,
        author: 'Bob Johnson',
        approved: false
      }
    ]
  } catch (err: any) {
    error.value = err.message || 'Failed to fetch items'
  } finally {
    loading.value = false
  }
}

const approveItem = async (id: string) => {
  try {
    // TODO: Replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 300))
    
    const item = items.value.find(i => i._id === id)
    if (item) {
      item.approved = true
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to approve item'
  }
}

const denyItem = async (id: string) => {
  if (!confirm('Are you sure you want to revoke approval for this item?')) {
    return
  }
  
  try {
    // TODO: Replace with actual API call
    await new Promise(resolve => setTimeout(resolve, 300))
    
    const item = items.value.find(i => i._id === id)
    if (item) {
      item.approved = false
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to deny item'
  }
}

onMounted(() => {
  fetchItems()
})
</script>

<style scoped>
.approve-deny-component {
  padding: 1rem;
}

h2 {
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  text-transform: capitalize;
}

.info-box {
  background-color: #d1ecf1;
  border: 1px solid #bee5eb;
  color: #0c5460;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 2rem;
}

.filters {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filter-button {
  padding: 0.5rem 1.5rem;
  background-color: #f8f9fa;
  color: #495057;
  border: 2px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s;
}

.filter-button:hover {
  background-color: #e9ecef;
}

.filter-button.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.refresh-button {
  padding: 0.5rem 1.5rem;
  background-color: #17a2b8;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.2s;
  margin-left: auto;
}

.refresh-button:hover {
  background-color: #138496;
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

.items-list {
  display: grid;
  gap: 1rem;
}

.item-card {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1.5rem;
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

.item-content {
  margin-bottom: 1rem;
}

.item-content p {
  margin: 0.5rem 0;
  color: #333;
  line-height: 1.6;
}

.item-actions {
  display: flex;
  gap: 0.5rem;
}

.approve-button {
  background-color: #28a745;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.approve-button:hover {
  background-color: #218838;
}

.deny-button {
  background-color: #dc3545;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background-color 0.2s;
}

.deny-button:hover {
  background-color: #c82333;
}
</style>
