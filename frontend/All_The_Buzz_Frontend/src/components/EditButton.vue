<template>
  <!-- Always visible for both managers and employees -->
  <button
    class="edit-btn"
    :title="tooltip"
    :aria-label="tooltip"
    @click="onEditClick"
    :disabled="saving || !isEditMode"
  >
    <!-- Pencil/Edit icon (inline SVG) -->
    <svg
      class="icon"
      viewBox="0 0 24 24"
      aria-hidden="true"
      focusable="false"
    >
      <path
        d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a.996.996 0 0 0 0-1.41l-2.34-2.34a.996.996 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"
        fill="currentColor"
      />
    </svg>
  </button>
</template>

<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'

interface Props {
  /** Item id to edit */
  id: string
  /** Category segment used in your endpoint */
  category: string
  /** JWT used in header (kept as 'Bearer' per your original) */
  jwt: string
  /** The body/data of the entry to edit */
  body: any
  /** Whether edit mode is enabled */
  isEditMode: boolean
  /** Optional tooltip (default: "Save Changes") */
  tooltip?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'updated', payload: { id: string }): void
  (e: 'error', message: string): void
}>()

const saving = ref(false)
const tooltip = props.tooltip ?? 'Save Changes'

async function onEditClick() {
  if (saving.value || !props.isEditMode) return

  const confirmed = window.confirm(
    'Are you sure you want to save these changes?'
  )
  if (!confirmed) return

  saving.value = true
  try {
    const url = `http://localhost:8080/${props.category}/${props.id}`

    const headers = { 'Bearer': `${props.jwt}` }

    await axios.put(url, props.body, { headers })

    emit('updated', { id: props.id })
  } catch (error: any) {
    const status = error?.response?.status ?? 'Unknown'
    const message = `Error: Status Code = ${status}`
    emit('error', message)
    console.error(message, error)
  } finally {
    saving.value = false
  }
}

</script>

<style scoped>
/* Small, table-friendly button */
.edit-btn {
  width: 24px;
  height: 24px;
  min-width: 24px;
  min-height: 24px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #ffc107; /* yellow border */
  border-radius: 4px;
  background-color: #fff3cd; /* light yellow bg */
  color: #856404;             /* dark yellow icon color */
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, border-color 0.15s ease;
}

.edit-btn:hover:not(:disabled) {
  background-color: #ffc107; /* yellow */
  color: white;
  border-color: #ffc107;
}

.edit-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.icon {
  width: 14px;
  height: 14px;
}
</style>
