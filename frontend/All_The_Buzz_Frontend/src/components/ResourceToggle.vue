<template>
  <div class="resource-toggle">
    <button
      v-for="option in options"
      :key="option.value"
      :class="['toggle-button', { active: activeComponent === option.value }]"
      @click="selectComponent(option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  activeComponent: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:activeComponent': [value: string]
}>()

const options = [
  { label: 'Get', value: 'get' },
  { label: 'Create', value: 'create' },
  { label: 'Edit', value: 'edit' },
  { label: 'Delete', value: 'delete' },
  { label: 'Approve/Deny', value: 'approve' }
]

const selectComponent = (value: string) => {
  emit('update:activeComponent', value)
}
</script>

<style scoped>
.resource-toggle {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.toggle-button {
  padding: 0.75rem 1.5rem;
  background-color: #f8f9fa;
  color: #495057;
  border: 2px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.2s;
}

.toggle-button:hover {
  background-color: #e9ecef;
  border-color: #adb5bd;
}

.toggle-button.active {
  background-color: #667eea;
  color: white;
  border-color: #667eea;
}

.toggle-button.active:hover {
  background-color: #5568d3;
  border-color: #5568d3;
}
</style>
