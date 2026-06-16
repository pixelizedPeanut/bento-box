<template>
  <main class="dashboard">
    <header class="dashboard-header">
      <h1>🍱 Bento Box Bookings</h1>
    </header>

    <!-- Global status banners controlled by our store -->
    <div v-if="store.isLoading" class="loading-bar">
      Updating active workbench...
    </div>
    <div v-if="store.errorMessage" class="error-bar">
      ⚠️ {{ store.errorMessage }}
    </div>

    <!-- Live Booking Success Alerts managed by the View -->
    <div v-if="bookingStatus.success" class="success-banner">
      🎉 {{ bookingStatus.message }}
    </div>

    <div class="dashboard-grid">
      <div class="sidebar-column">
        <!-- Toggles member context selections cleanly -->
        <MemberProfile
          :members="store.members"
          :selected-id="selectedMemberId"
          @select="handleMemberSelect"
        />

        <!-- Forms can safely submit; double-click protection lives here via store state -->
        <BookingForm
          :member-id="selectedMemberId"
          :inventory-id="selectedInventoryId"
          @success="handleBookingSubmission"
        />
      </div>

      <div class="main-column">
        <!-- Toggles inventory choices cleanly -->
        <InventoryList
          :inventory="store.inventory"
          :selected-id="selectedInventoryId"
          @select="handleInventorySelect"
        />

        <Bookings
          :bookings="store.bookings"
          @cancel="handleBookingCancellation"
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
import Bookings from '@/components/Bookings.vue'

import { api } from '@/api'

const store = useBentoStore()

// Master selection coordinate states
const selectedMemberId = ref(null)
const selectedInventoryId = ref(null)

// Local view confirmations
const bookingStatus = reactive({
  success: false,
  message: ''
})

// Safely await initial data loads on setup
onMounted(async () => {
  try {
    store.isLoading = true
    await store.refreshDashboardData()
  } catch (err) {
    store.errorMessage = 'Failed to initialize concierge dashboard data pipelines.'
    console.error(err)
  } finally {
    store.isLoading = false
  }
})

// Clean matching logic to support on/off row toggles
const handleMemberSelect = (id) => {
  resetStatusBanner()
  store.errorMessage = null // Flush stale errors on fresh interaction
  selectedMemberId.value = selectedMemberId.value === id ? null : id
}

const handleInventorySelect = (id) => {
  resetStatusBanner()
  store.errorMessage = null
  selectedInventoryId.value = selectedInventoryId.value === id ? null : id
}

const resetStatusBanner = () => {
  bookingStatus.success = false
  bookingStatus.message = ''
}

// Master execution processing pipeline
const handleBookingSubmission = async (payload) => {
  try {
    resetStatusBanner()
    store.errorMessage = null
    store.isLoading = true

    // Fire actual business transaction out to servers
    await api.bookItem(payload.memberId, payload.inventoryId)

    bookingStatus.success = true
    bookingStatus.message = 'Workspace reservation successfully logged! Grid values flushed.'

    // Flush selections on complete success
    selectedMemberId.value = null
    selectedInventoryId.value = null

    // Sync state layout tables instantly
    await store.refreshDashboardData()

  } catch (error) {
    console.error('Failed processing dashboard workspace transaction:', error)
    // CAPTURE CONCIERGE GHOST RACE CONDITIONS HERE:
    store.errorMessage = error.response?.data?.message || 'Transaction rejected. This asset may have just been claimed by another desk.'
  } finally {
    store.isLoading = false
  }
}

const handleBookingCancellation = async (bookingRef) => {
  try {
    resetStatusBanner()
    store.errorMessage = null
    store.isLoading = true

    const result = await api.cancelBooking(bookingRef)

    bookingStatus.success = true
    bookingStatus.message = result.message || `Booking ${bookingRef} successfully cancelled.`

    await store.refreshDashboardData()

  } catch (error) {
    console.error('Failed processing cancellation pipeline cascade:', error)
    store.errorMessage = error.response?.data?.message || 'Failed to cancel the requested allocation.'
  } finally {
    store.isLoading = false
  }
}
</script>
