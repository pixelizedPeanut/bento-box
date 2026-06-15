import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/api'

export const useBentoStore = defineStore('bento', () => {
  const members = ref([])
  const inventory = ref([])
  const bookings = ref([])
  const isLoading = ref(false)
  const errorMessage = ref(null)

  const refreshDashboardData = async () => {
    isLoading.value = true
    errorMessage.value = null

    try {
      // Fire both network requests in parallel for maximum speed
      const [rawMembers, rawInventory, rawBookings] = await Promise.all([
        api.getMembers(),
        api.getInventory(),
        api.getBookings()
      ])

      // Map member rows using your exact key patterns
      members.value = rawMembers.map(member => ({
        id: member.id.toString(),
        name: member.name,
        surname: member.surname,
        dateJoined: member.date_joined,
        bookingCount: member.booking_count || 0
      }))

      // Map inventory columns and transform fields to camelCase
      inventory.value = rawInventory.map(item => ({
        id: item.id.toString(), // Maintained for unique v-for keys
        title: item.title,
        description: item.description,
        remainingCount: item.remaining_count || 0,
        expirationDate: item.expiration_date
      }))

      // Map bookings to camelCase
      bookings.value = rawBookings.map(booking => ({
        bookingRef: booking.booking_ref,
        memberId: booking.member_id.toString(),
        inventoryId: booking.inventory_id.toString(),
        createdAt: booking.created_at,
        status: booking.status.toUpperCase()
      }))
    } catch (error) {
      errorMessage.value = error.message || 'Failed to sync with workspace engine.'
      console.error(error)
    } finally {
      isLoading.value = false
    }
  }

  return {
    members,
    inventory, // Exposed inventory state to layout components
    bookings,
    isLoading,
    errorMessage,
    refreshDashboardData
  }
})
