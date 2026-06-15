import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api } from '@/api'

export const useBentoStore = defineStore('bento', () => {
  const members = ref([])
  const inventory = ref([]) // Added live inventory state container
  const isLoading = ref(false)
  const errorMessage = ref(null)

  const refreshDashboardData = async () => {
    isLoading.value = true
    errorMessage.value = null

    try {
      // Fire both network requests in parallel for maximum speed
      const [rawMembers, rawInventory] = await Promise.all([
        api.getMembers(),
        api.getInventory()
      ])

      // Map member rows using your exact key patterns
      members.value = rawMembers.map(member => ({
        id: member.id,
        name: member.name,
        surname: member.surname,
        dateJoined: member.date_joined,
        bookingCount: member.booking_count || 0
      }))

      // Map inventory columns and transform fields to camelCase
      inventory.value = rawInventory.map(item => ({
        id: item.id, // Maintained for unique v-for keys
        title: item.title,
        description: item.description,
        remainingCount: item.remaining_count || 0,
        expirationDate: item.expiration_date
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
    isLoading,
    errorMessage,
    refreshDashboardData
  }
})
