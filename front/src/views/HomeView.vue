<script setup>
import TheMain from '@/components/TheMain.vue'

</script>

<template>
    <div class="home-view">
        <TheMain />
    </div>
</template>

<style>
.home-view {
    padding: 0 25px 0;
    height: 100%;
}

@media (max-width: 600px) {
    .home-view {
        padding: 10px;
    }
}
</style>
