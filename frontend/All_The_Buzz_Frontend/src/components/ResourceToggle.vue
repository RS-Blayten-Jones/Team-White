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
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xl);
  flex-wrap: wrap;
}

.toggle-button {
  padding: 0.75rem 1.5rem;
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  transition: all var(--transition-base);
}

.toggle-button:hover {
  background-color: var(--bg-tertiary);
  border-color: var(--color-gray-400);
}

.toggle-button:focus {
  outline: 3px solid var(--color-primary-orange);
  outline-offset: 2px;
}

.toggle-button.active {
  background-color: var(--color-primary-purple);
  color: var(--text-on-primary);
  border-color: var(--color-primary-purple);
}

.toggle-button.active:hover {
  background-color: #3a2e63;
  border-color: #3a2e63;
}
</style>
