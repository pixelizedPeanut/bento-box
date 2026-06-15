<template>
  <div class="card">
    <h3>👤 Team Members</h3>

    <div class="table-container">
      <table class="members-table">
        <thead>
          <tr>
            <th>Member</th>
            <th>Joined</th>
            <th class="text-right">Bookings</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="member in members"
            :key="member.id"
            :class="{ 'is-selected': selectedId === member.id }"
            @click="selectMember(member.id)"
          >
            <!-- Combines Name + Surname -->
            <td class="member-name">
              {{ member.name }} {{ member.surname }}
            </td>
            <!-- Formatted Date Column -->
            <td class="text-muted">
              {{ formatDate(member.dateJoined) }}
            </td>
            <!-- Aligned Numeric Booking Count -->
            <td class="text-right">
              <span class="booking-badge">{{ member.bookingCount }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="selection-footer">
      <span v-if="selectedId">Active Selection ID: <strong>{{ selectedId }}</strong></span>
      <span v-else class="italic">Click a row to inspect a member</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  members: {
    type: Array,
    required: true,
    default: () => []
  }
})

const selectedId = ref(null)

const selectMember = (id) => {
  selectedId.value = selectedId.value === id ? null : id
}

// Drops the timestamps and outputs a clean 'Jan 15, 2026' format
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
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
  max-height: 280px;
  overflow-y: auto;
  border: 1px solid $color-border;
  border-radius: calc($radius - 2px);
  background: #ffffff;
}

.members-table {
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
      cursor: pointer;
      transition: background-color 0.15s ease;

      &:last-child {
        border-bottom: none;
      }

      &:hover {
        background-color: #f7fafc;
      }

      &.is-selected {
        background-color: #ebf8ff;
        color: #2b6cb0;

        .text-muted {
          color: #4299e1;
        }

        .booking-badge {
          background: #2b6cb0;
          color: white;
        }
      }

      td {
        padding: 0.75rem;
        vertical-align: middle;
      }
    }
  }

  // Layout alignment helpers
  .text-right {
    text-align: right;
  }

  .member-name {
    font-weight: 500;
  }

  .booking-badge {
    display: inline-block;
    background: #edf2f7;
    color: #4a5568;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.15rem 0.5rem;
    border-radius: 12px;
    min-width: 1.5rem;
    text-align: center;
    transition: all 0.15s ease;
  }
}

.selection-footer {
  margin-top: 0.75rem;
  font-size: 0.8rem;
  color: $text-muted;
}
</style>
