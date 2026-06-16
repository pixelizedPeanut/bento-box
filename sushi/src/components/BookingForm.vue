<template>
  <div class="card">
    <h3>🎟️ Quick Booking</h3>

    <!-- State 1: Awaiting selections -->
    <div v-if="!selectedMember || !selectedItem" class="state-message info-box">
      <p>💡 <strong>Ready to book?</strong> Please select a member and an experience layer from the tables above to populate this panel.</p>
    </div>

    <!-- State 2: Invalid Selection (Fails Business Logic Rules) -->
    <div v-else-if="!isValidSelection" class="state-message error-box">
      <h4>⚠️ Invalid Selection Configuration</h4>
      <p class="error-detail">
        A new selection has to be made due to the following system constraints:
      </p>

      <ul class="error-list">
        <!-- Rule: Less than 2 bookings check -->
        <li v-if="selectedMember.bookingCount >= 2" class="fail">
          ❌ <strong>{{ selectedMember.name }}</strong> already has {{ selectedMember.bookingCount }} active bookings (Limit is 2).
        </li>
        <!-- Rule: More than 0 stock check -->
        <li v-if="selectedItem.remainingCount <= 0" class="fail">
          ❌ <strong>{{ selectedItem.title }}</strong> is completely out of stock.
        </li>
      </ul>
      <p class="instruction">
        Please click different rows in the dashboard grids to correct this.
      </p>
    </div>

    <!-- State 3: Valid Selection (Passes all checks) -->
    <div v-else class="booking-workspace">
      <div class="summary-line">
        <label>Booking For</label>
        <p class="value">
          {{ selectedMember.name }} {{ selectedMember.surname }}
        </p>
        <span class="subtext">Current bookings: {{ selectedMember.bookingCount }}</span>
      </div>

      <div class="summary-line">
        <label>Selected Asset</label>
        <p class="value">
          {{ selectedItem.title }}
        </p>
        <span class="subtext">Stock remaining: {{ selectedItem.remainingCount }} units</span>
      </div>

      <button
        class="submit-btn"
        @click="processBooking"
      >
        Confirm Booking
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useBentoStore } from '@/stores/bentoStore'

const props = defineProps({
  memberId: {
    type: String,
    default: null
  },
  inventoryId: {
    type: String,
    default: null
  }
})

// 1. Declare the success emit channel to update the dashboard later
const emit = defineEmits(['success'])

const store = useBentoStore()

// Look up full data records from the store array tables based on passed ID props
const selectedMember = computed(() => {
  return store.members.find(m => m.id === props.memberId)
})

const selectedItem = computed(() => {
  return store.inventory.find(i => i.id === props.inventoryId)
})

// Validation Guard Engines
const isMemberValid = computed(() => {
  return selectedMember.value && selectedMember.value.bookingCount < 2
})

const isItemValid = computed(() => {
  return selectedItem.value && selectedItem.value.remainingCount > 0
})

const isValidSelection = computed(() => {
  return isMemberValid.value && isItemValid.value
})

const processBooking = () => {
  if (!isValidSelection.value) return

  emit('success', {
    memberId: props.memberId,
    inventoryId: props.inventoryId
  })
}
</script>

<style lang="scss" scoped>
.card {
  background: $bg-card;
  border: 1px solid $color-border;
  border-radius: $radius;
  padding: 1.5rem;

  h3 {
    margin: 0 0 1rem 0;
    color: $color-dark;
    font-size: 1.1rem;
  }
}

.state-message {
  padding: 1rem;
  border-radius: $radius;
  font-size: 0.9rem;
  line-height: 1.4;

  p {
    margin: 0;
  }
}

.info-box {
  background: #f7fafc;
  color: $text-muted;
  border: 1px dashed $color-border;
}

.error-box {
  background: #fff5f5;
  color: #9b2c2c;
  border: 1px solid #fed7d7;

  h4 {
    margin: 0 0 0.5rem 0;
    color: #9b2c2c;
  }

  .error-detail {
    margin-bottom: 0.75rem;
    font-size: 0.85rem;
  }

  .error-list {
    margin: 0 0 1rem 0;
    padding-left: 1.25rem;
    font-size: 0.85rem;

    li {
      margin-bottom: 0.4rem;
    }
  }

  .instruction {
    font-size: 0.8rem;
    font-weight: 500;
    color: #c53030;
    font-style: italic;
  }
}

.booking-workspace {
  display: flex;
  flex-direction: column;
  gap: 1rem;

  .summary-line {
    border-bottom: 1px dashed #edf2f7;
    padding-bottom: 0.5rem;

    label {
      font-size: 0.75rem;
      text-transform: uppercase;
      color: $text-muted;
      display: block;
      letter-spacing: 0.05em;
      margin-bottom: 0.2rem;
    }

    .value {
      margin: 0;
      font-weight: 600;
      color: $color-dark;
      font-size: 0.95rem;
    }

    .subtext {
      font-size: 0.75rem;
      color: $text-muted;
    }
  }

  .submit-btn {
    margin-top: 0.5rem;
    background: #3182ce;
    color: white;
    border: none;
    padding: 0.75rem;
    border-radius: $radius;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.15s ease;

    &:hover:not(:disabled) {
      background: #2b6cb0;
    }

    &:disabled {
      background: #cbd5e0;
      cursor: not-allowed;
    }
  }
}
</style>
