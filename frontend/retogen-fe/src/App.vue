<script setup lang="ts">
import { RouterView } from 'vue-router'
import ModeToggle from '@/components/ModeToggle.vue'
</script>

<template>
  <div class="min-h-screen">
    <header class="flex justify-end p-4">
      <ModeToggle />
    </header>

    <RouterView />
  </div>
</template>