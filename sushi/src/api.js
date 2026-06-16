const BASE_URL = 'http://localhost:8000'

// Helper to handle standard JSON requests and parse the response directly
async function request (path, options = {}) {
  const url = `${BASE_URL}${path}`
  const headers = { 'Content-Type': 'application/json', ...options.headers }

  const response = await fetch(url, { ...options, headers })

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}))
    throw new Error(errorBody.detail || `HTTP Error: ${response.status}`)
  }

  return response.json()
}

export const api = {
  // --- Inventory ---
  getInventory () {
    return request('/inventory/')
  },

  // --- Members ---
  getMembers () {
    return request('/members/')
  },

  // --- Bookings ---
  getBookings () {
    return request('/bookings/')
  },

  bookItem (memberId, inventoryId) {
    return request('/book', {
      method: 'POST',
      body: JSON.stringify({
        member_id: memberId,
        inventory_id: inventoryId
      })
    })
  },

  cancelBooking (bookingRef) {
    return request('/cancel', {
      method: 'POST',
      body: JSON.stringify({
        booking_ref: bookingRef
      })
    })
  }
}
