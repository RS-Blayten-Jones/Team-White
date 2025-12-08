
<template>
  <!-- Only visible if user is a manager -->
  <button
    v-if="isManager"
    class="delete-btn"
    :title="tooltip"
    :aria-label="tooltip"
    @click="onDeleteClick"
    :disabled="deleting"
  >
    <!-- Red X icon (inline SVG) -->
    <svg
      class="icon"
      viewBox="0 0 24 24"
      aria-hidden="true"
      focusable="false"
    >
      <path
        d="M18.3 5.71a1 1 0 0 0-1.41 0L12 10.59 7.11 5.71a1 1 0 0 0-1.41 1.41L10.59 12l-4.89 4.88a1 1 0 1 0 1.41 1.41L12 13.41l4.88 4.89a1 1 0 0 0 1.41-1.41L13.41 12l4.89-4.88a1 1 0 0 0 0-1.41z"
        fill="currentColor"
      />
    </svg>
  </button>
</template>

<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'

interface Props {
  /** Item id to delete */
  id: string
  /** Category segment used in your endpoint */
  category: string
  /** JWT used in header (kept as 'Bearer' per your original) */
  jwt: string
  /** Controls visibility: only show for managers */
  isManager: boolean
  /** Optional tooltip (default: "Delete") */
  tooltip?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'deleted', payload: { id: string }): void
  (e: 'error', message: string): void
}>()

const deleting = ref(false)
const tooltip = props.tooltip ?? 'Delete'


async function onDeleteClick() {
  if (deleting.value) return

  const confirmed = window.confirm(
    'Are you sure you want to permanently delete this item?\nThis action cannot be undone.'
  )
  if (!confirmed) return

  deleting.value = true
  try {
    const url = `http://localhost:8080/${props.category}/${props.id}`

    const headers = { 'Bearer': `${props.jwt}` } // MOD

    await axios.delete(url, { headers }) // MOD

    emit('deleted', { id: props.id })
  } catch (error: any) {
    const status = error?.response?.status ?? 'Unknown'
    const message = `Error: Status Code = ${status}`
    emit('error', message)
    console.error(message, error)
  } finally {
    deleting.value = false
  }
}

</script>

<style scoped>
/* Small, table-friendly button */
.delete-btn {
  width: 24px;
  height: 24px;
  min-width: 24px;
  min-height: 24px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dc3545; /* red border */
  border-radius: 4px;
  background-color: #f8d7da; /* light red bg */
  color: #dc3545;             /* red icon color */
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

.delete-btn:hover:not(:disabled) {
  background-color: #dc3545; /* red */
  color: white;
  border-color: #dc3545;
}

.delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon {
  width: 14px;
  height: 14px;
}
</style>
