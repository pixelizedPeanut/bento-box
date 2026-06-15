<template>
  <div class="card">
    <h2>📦 Available Experiences & Inventory</h2>
    <p class="placeholder">
      Awaiting database sync parameters...
    </p>
  </div>
</template>

<style lang="scss" scoped>
.card {
    background: $bg-card;
    border: 1px solid $color-border;
    border-radius: $radius;
    padding: 1.5rem;
    min-height: 300px;

    h2 {
        margin-bottom: 1rem;
        font-size: 1.4rem;
        color: $color-dark;
    }

    .placeholder {
        color: $text-muted;
    }
}
</style>
