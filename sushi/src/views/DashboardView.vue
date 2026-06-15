<template>
  <main class="dashboard">
    <header class="dashboard-header">
      <h1>🍱 Bento Box Workspace</h1>
    </header>

    <!-- Global status banners controlled by our store -->
    <div v-if="store.isLoading" class="loading-bar">
      Updating active workbench...
    </div>
    <div v-if="store.errorMessage" class="error-bar">
      {{ store.errorMessage }}
    </div>

    <!-- Live Booking Success Alerts managed by the View -->
    <div v-if="bookingStatus.success" class="success-banner">
      🎉 {{ bookingStatus.message }}
    </div>

    <div class="dashboard-grid">
      <div class="sidebar-column">
        <!-- Listen for selection shifts; force value to null if reset by dashboard action -->
        <MemberProfile
          :members="store.members"
          :selected-id="selectedMemberId"
          @select="clearBannerAndSelectMember"
        />

        <!-- Listen for the successful booking event broadcast from inside the form -->
        <BookingForm
          :member-id="selectedMemberId"
          :inventory-id="selectedInventoryId"
          @success="handleBookingSubmission"
        />
      </div>

      <div class="main-column">
        <!-- Listen for selection shifts; force value to null if reset by dashboard action -->
        <InventoryList
          :inventory="store.inventory"
          :selected-id="selectedInventoryId"
          @select="clearBannerAndSelectInventory"
        />
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { useBentoStore } from '@/stores/bentoStore'

import MemberProfile from '@/components/MemberProfile.vue'
import BookingForm from '@/components/BookingForm.vue'
import InventoryList from '@/components/InventoryList.vue'

import { api } from '@/api'

const store = useBentoStore()

// State containers to hold our cross-component sync coordinates
let selectedMemberId = ref(null)
let selectedInventoryId = ref(null)

// Track temporary confirmation banner status locally at view layer
const bookingStatus = reactive({
  success: false,
  message: ''
})

// Fire off the master fetch payload to fill our store tables automatically on load
onMounted(() => {
  store.refreshDashboardData()
})

// Helper methods to clear confirmation messages immediately if user starts choosing new rows
const clearBannerAndSelectMember = (id) => {
  resetStatusBanner()
  selectedMemberId.value = id
}

const clearBannerAndSelectInventory = (id) => {
  resetStatusBanner()
  selectedInventoryId.value = id
}

const resetStatusBanner = () => {
  bookingStatus.success = false
  bookingStatus.message = ''
}

// Master execution pipeline for processing positive component booking requests
const handleBookingSubmission = async (payload) => {
  try {
    // 1. Hit your concrete store endpoint passing payload ids out to database layers
    // Adjust action name if your bentoStore mapping utilizes a different name
    await api.bookItem(payload.memberId, payload.inventoryId)

    // 2. Display the local validation success confirmation layer banner
    bookingStatus.success = true
    bookingStatus.message = 'Workspace reservation successfully logged! Grid values flushed.'

    // 3. Wipe selection variables out across columns to clear highlighted rows completely
    selectedMemberId = ref(null)
    selectedInventoryId = ref(null)

    // 4. Force state engine tables to pull fresh updated counts instantly from the servers
    await store.refreshDashboardData()

  } catch (error) {
    console.error('Failed processing dashboard workspace transaction:', error)
  }
}
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

.success-banner {
  background-color: #f0fff4;
  border: 1px solid #c6f6d5;
  color: #22543d;
  padding: 1rem;
  border-radius: $radius;
  margin-bottom: 1.5rem;
  font-weight: 500;
  font-size: 0.95rem;
}
</style>
