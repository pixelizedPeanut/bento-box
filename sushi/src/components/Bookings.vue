<template>
  <div class="card">
    <h3>📅 Bookings</h3>

    <div class="table-container">
      <table class="bookings-table">
        <thead>
          <tr>
            <th>Reference</th>
            <th>Member ID</th>
            <th>Inventory ID</th>
            <th>Status</th>
            <th class="text-right">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in bookings" :key="booking.bookingRef">
            <td class="booking-ref font-mono">
              {{ booking.bookingRef }}
            </td>
            <td class="text-muted">
              Member #{{ booking.memberId }}
            </td>
            <td class="text-muted">
              Item #{{ booking.inventoryId }}
            </td>
            <td>
              <span :class="['status-badge', booking.status === 'CANCELLED' ? 'is-cancelled' : 'is-active']">
                {{ booking.status }}
              </span>
            </td>
            <td class="text-right">
              <button
                v-if="booking.status !== 'CANCELLED'"
                class="btn-cancel"
                @click="triggerCancellation(booking.bookingRef)"
              >
                Cancel
              </button>
              <span v-else class="terminated-text">Terminated</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  bookings: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['cancel'])

// Pass the reference directly into the click event handler
const triggerCancellation = (bookingRef) => {
  if (window.confirm(`Are you sure you want to cancel booking ${bookingRef}?`)) {
    emit('cancel', bookingRef)
  }
}
</script>

<style lang="scss" scoped>
.card {
  background: $bg-card;
  border: 1px solid $color-border;
  border-radius: $radius;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;

  h3 {
    margin: 0 0 1rem 0;
    color: $color-dark;
    font-size: 1.1rem;
  }
}

.table-container {
  max-height: 320px;
  overflow-y: auto;
  border: 1px solid $color-border;
  border-radius: calc($radius - 2px);
  background: #ffffff;
}

.bookings-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.9rem;

  thead {
    background: #f7fafc;
    position: sticky;
    top: 0;
    z-index: 1;
    border-bottom: 2px solid $color-border;

    th {
      padding: 0.6rem 0.75rem;
      font-weight: 600;
      color: $color-dark;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
  }

  tbody {
    tr {
      border-bottom: 1px solid #edf2f7;

      &:last-child {
        border-bottom: none;
      }

      &:hover {
        background-color: #f8fafc;
      }

      td {
        padding: 0.75rem;
        vertical-align: middle;
      }
    }
  }

  .text-right {
    text-align: right;
  }

  .font-mono {
    font-family: monospace;
  }

  .booking-ref {
    font-weight: 600;
    color: #4a5568;
  }

  .status-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.15rem 0.5rem;
    border-radius: 6px;
    text-align: center;

    &.is-active {
      background: #e6fffa;
      color: #234e52;
      border: 1px solid #b2f5ea;
    }

    &.is-cancelled {
      background: #fff5f5;
      color: #742a2a;
      border: 1px solid #fed7d7;
    }
  }

  .btn-cancel {
    background: #e53e3e;
    color: white;
    border: none;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.1s ease;

    &:hover {
      background: #c53030;
    }
  }

  .terminated-text {
    color: #a0aec0;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.7rem;
    letter-spacing: 0.05em;
  }
}
</style>
