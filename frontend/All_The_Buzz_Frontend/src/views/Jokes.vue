
<template>
  <div class="jokes-page page-container">
    <AppHeader />

    <main class="content-wrapper" role="main">
      <div class="page-header">
        <h1 class="page-title">Jokes Management</h1>
      </div>

      <ResourceToggle v-model:activeComponent="activeComponent" />

      <div class="content-area card">
        <component
          v-if="ready"
          :is="currentComponent"
          :isManager="userIsManager"
          :jwt="jwtToken"
          :resourceType="resourceType"
        />
        <div v-else class="error">Loading auth/resourceType…</div>
      </div>
    </main>
  </div>
</template>


<script setup lang="ts">
import { ref, computed } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import ResourceToggle from '@/components/ResourceToggle.vue'
import Get from '@/components/Get.vue'
import Create from '@/components/Create.vue'
import Edit from '@/components/Edit.vue'
import Delete from '@/components/Delete.vue'
import ApproveAndDeny from '@/components/ApproveAndDeny.vue'

const activeComponent = ref('get')

const components = {
  get: Get,
  create: Create,
  edit: Edit,
  delete: Delete,
  approve: ApproveAndDeny
}

const resourceType = ref<string>('jokes')
const userIsManager = ref<boolean>(true)
const jwtToken = ref<string>('eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBdXRoIFNlcnZpY2UiLCJsYXN0X25hbWUiOiJUd2VlZCIsImxvY2F0aW9uIjoiVW5pdGVkIFN0YXRlcyIsImlkIjo1NzcsImRlcGFydG1lbnQiOiJTYWxlcyIsInRpdGxlIjoiTWFuYWdlciIsImZpcnN0X25hbWUiOiJBdWd1c3RlIiwic3ViIjoiQXVndXN0ZSBUd2VlZCIsImlhdCI6MTc2NDk1MjMwOCwiZXhwIjoxNzY0OTU1OTA4fQ.h1Pgao8br_9c_fpG9TBS9J_t6SiOszkd_oNDoF7fAXw')

const ready = computed(() => !!resourceType.value && !!jwtToken.value)

const currentComponent = computed(() => components[activeComponent.value as keyof typeof components])
</script>

<style scoped>
.jokes-page {
  background-color: var(--bg-primary);
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-title {
  color: var(--text-primary);
  font-size: var(--font-size-3xl);
  margin: 0;
  text-transform: capitalize;
}

.content-area {
  min-height: 500px;
}
</style>
