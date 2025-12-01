<template>
  <div class="quotes-view">
    <header class="view-header">
      <button class="back-button" @click="goBack">← Back to Menu</button>
      <h1>Quotes Management</h1>
    </header>
    
    <ResourceToggle v-model:activeComponent="activeComponent" />
    
    <div class="content-area">
      <component :is="currentComponent" resource-type="quotes" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import ResourceToggle from '@/components/ResourceToggle.vue'
import Get from '@/components/Get.vue'
import Create from '@/components/Create.vue'
import Edit from '@/components/Edit.vue'
import Delete from '@/components/Delete.vue'
import ApproveAndDeny from '@/components/ApproveAndDeny.vue'

const router = useRouter()
const activeComponent = ref('get')

const components = {
  get: Get,
  create: Create,
  edit: Edit,
  delete: Delete,
  approve: ApproveAndDeny
}

const currentComponent = computed(() => components[activeComponent.value as keyof typeof components])

const goBack = () => {
  router.push({ name: 'resource-menu' })
}
</script>

<style scoped>
.quotes-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.view-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  gap: 1rem;
}

.back-button {
  background-color: #6c757d;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #5a6268;
}

h1 {
  color: #667eea;
  font-size: 2rem;
  margin: 0;
}

.content-area {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-height: 400px;
}
</style>
