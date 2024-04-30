<script setup lang="ts">
import {RouterView} from "vue-router";
import Navbar from "./components/Navbar.vue";
</script>

<template>
  <div class="flex flex-col min-h-screen bg-g-a3">
    <Navbar />
    <RouterView />
  </div>
</template>

<style scoped>
</style>