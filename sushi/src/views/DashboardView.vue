<template>
    <main class="dashboard">
        <header class="dashboard-header">
            <h1>🍱 Bento Box Workspace</h1>
        </header>

        <div class="dashboard-grid">
            <div class="sidebar-column">
                <MemberProfile />
                <BookingForm />
            </div>

            <div class="main-column">
                <InventoryList />
            </div>
        </div>
    </main>
</template>

<script setup>
import MemberProfile from "../components/MemberProfile.vue";
import BookingForm from "../components/BookingForm.vue";
import InventoryList from "../components/InventoryList.vue";
</script>

<style lang="scss" scoped>
.dashboard {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;

    &-header {
        margin-bottom: 2rem;
        h1 {
            font-size: 1.8rem;
            color: $color-dark;
        }
    }
}

.dashboard-grid {
    display: grid;
    grid-template-columns: 350px 1fr;
    gap: 1.5rem;

    @media (max-width: 768px) {
        grid-template-columns: 1fr;
    }
}

.sidebar-column {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}
</style>
