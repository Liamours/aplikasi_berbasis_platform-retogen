<script setup lang="ts">
import { isDark } from './composables/useTheme'
</script>

<template>
  <div :class="{ 'dark-mode': isDark }">
    <router-view />
  </div>
</template>