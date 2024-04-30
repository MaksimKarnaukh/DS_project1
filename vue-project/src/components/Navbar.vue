<script setup lang="ts">
import {RouterLink} from "vue-router"
</script>

<template>
  <header class="sticky top-0 bg-g-a1 shadow-lg z-50">
    <nav class="container flex flex-col sm:flex-row items-center gap-4 text-white py-6 px-28">
      <RouterLink :to="{name: 'home'}">
        <div class="flex items-center gap-3">
          <i class="fa-solid fa-film"></i>
          <p class="text-2xl">Cinema Central</p>
        </div>
      </RouterLink>

      <div class="flex gap-3 flex-1 justify-end">
        <p>API</p>
      </div>
    </nav>
  </header>
</template>
