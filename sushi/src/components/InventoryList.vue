<template>
  <div class="card">
    <h2>📦 Available Experiences & Inventory</h2>

    <!-- Render the main table layout if items exist -->
    <div v-if="inventory.length" class="table-container">
      <table class="inventory-table">
        <thead>
          <tr>
            <th>Item Title</th>
            <th>Description</th>
            <th class="text-right">
              Stock
            </th>
            <th>Expires</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in inventory"
            :key="item.id"
            :class="{ 'is-selected': selectedId === item.id }"
            @click="selectItem(item.id)"
          >
            <!-- Core Text Columns -->
            <td class="item-title">
              {{ item.title }}
            </td>
            <td class="item-desc">
              {{ item.description }}
            </td>

            <!-- Dynamic Numeric Stock Column -->
            <td class="text-right">
              <span
                class="stock-badge"
                :class="{ 'low-stock': item.remainingCount <= 3 }"
              >
                {{ item.remainingCount }} left
              </span>
            </td>

            <!-- Safe Formatted Expiration Column -->
            <td class="text-muted">
              {{ formatDate(item.expirationDate) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Fallback Placeholder -->
    <p v-else class="placeholder">
      Awaiting database sync parameters...
    </p>

    <!-- Inspection tracking indicator -->
    <div class="selection-footer">
      <span v-if="selectedId">Selected Asset Context: <strong>{{ selectedId }}</strong></span>
      <span v-else class="italic">Click an experience layer to inspect stock lines</span>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  inventory: {
    type: Array,
    default: () => []
  }
})

// 1. Declare the outbound communication event channel
const emit = defineEmits(['select'])

// Track item highlights locally
const selectedId = ref(null)

const selectItem = (id) => {
  // Toggle local highlight tracking state
  selectedId.value = selectedId.value === id ? null : id

  // 2. Fire the active state out to the parent engine (returns the ID or null)
  emit('select', selectedId.value)
}

// Drops time layouts and cleans up formatting smoothly
const formatDate = (dateString) => {
  if (!dateString) return 'Never'
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
  padding: 1.5rem;
  min-height: 300px;
  display: flex;
  flex-direction: column;

  h2 {
    margin: 0 0 1.25rem 0;
    font-size: 1.3rem;
    color: $color-dark;
  }
}

.table-container {
  max-height: 400px; // Gives plenty of scroll room since this sits in your wider column
  overflow-y: auto;
  border: 1px solid $color-border;
  border-radius: calc($radius - 2px);
  background: #ffffff;
}

.inventory-table {
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
      padding: 0.75rem;
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

      // Selected row visual highlight configuration
      &.is-selected {
        background-color: #ebf8ff;
        color: #2b6cb0;

        .text-muted, .item-desc {
          color: #4299e1;
        }

        .stock-badge:not(.low-stock) {
          background: #2b6cb0;
          color: white;
        }
      }

      td {
        padding: 0.85rem 0.75rem;
        vertical-align: middle;
      }
    }
  }

  // Layout alignment & emphasis layers
  .text-right {
    text-align: right;
  }

  .item-title {
    font-weight: 600;
    color: $color-dark;
  }

  .item-desc {
    color: #718096;
    max-width: 250px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis; // Keeps descriptions from completely breaking row balance
  }

  .stock-badge {
    display: inline-block;
    background: #edf2f7;
    color: #4a5568;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    white-space: nowrap;

    // Changes context color instantly if numbers dip below critical thresholds
    &.low-stock {
      background: #fff5f5;
      color: #c53030;
      border: 1px solid #fed7d7;
    }
  }
}

.placeholder {
  color: $text-muted;
  font-style: italic;
  margin: 0;
}

.selection-footer {
  margin-top: auto; // Pins footer to the bottom of the card block
  padding-top: 1rem;
  font-size: 0.8rem;
  color: $text-muted;
}
</style>
