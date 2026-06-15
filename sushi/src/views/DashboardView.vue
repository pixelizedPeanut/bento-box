<template>
  <main class="dashboard">
    <header class="dashboard-header">
      <h1>🍱 Bento Box Workspace</h1>
    </header>

    <!-- Optional global status banners controlled by our store -->
    <div v-if="store.isLoading" class="loading-bar">
      Updating active workbench...
    </div>
    <div v-if="store.errorMessage" class="error-bar">
      {{ store.errorMessage }}
    </div>

    <div class="dashboard-grid">
      <div class="sidebar-column">
        <!-- Pass the store data straight down through the props channel -->
        <MemberProfile :members="store.members" />
        <BookingForm />
      </div>

      <div class="main-column">
        <!-- Inventory will go here next -->
        <InventoryList />
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useBentoStore } from '@/stores/bentoStore'

import MemberProfile from '@/components/MemberProfile.vue'
import BookingForm from '@/components/BookingForm.vue'
import InventoryList from '@/components/InventoryList.vue'

const store = useBentoStore()

// Fire off the master fetch payload to fill our store tables automatically on load
onMounted(() => {
  store.refreshDashboardData()
})
</script>

<style lang="scss" scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;

  &-header {
    margin-bottom: 2rem;
    h1 {
      font-size: 1.8rem;
      color: $color-dark;
    }
  }
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 1.5rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.sidebar-column {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.loading-bar {
  color: #3182ce;
  padding-bottom: 1rem;
  font-weight: 500;
}
.error-bar {
  color: #e53e3e;
  padding-bottom: 1rem;
  font-weight: 500;
}
</style>
