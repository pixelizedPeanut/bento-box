<template>
    <div class="card">
        <h3>👤 Member Profile</h3>
        <p class="placeholder">Awaiting member profile data...</p>
    </div>
</template>

<style lang="scss" scoped>
.card {
    background: $bg-card;
    border: 1px solid $color-border;
    border-radius: $radius;
    padding: 1.5rem;

    h3 {
        margin-bottom: 0.5rem;
        color: $color-dark;
    }

    .placeholder {
        color: $text-muted;
        font-size: 0.9rem;
    }
}
</style>
