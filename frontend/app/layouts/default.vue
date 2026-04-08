<script setup lang="ts">
const { isDark } = useTheme()
</script>

<template>
  <div class="app-shell" :class="{ 'dark-mode': isDark }">
    <div class="app-shell__grid" />
    <div class="app-shell__blob app-shell__blob--red" />
    <div class="app-shell__blob app-shell__blob--cyan" />

    <BaseNavbar />

    <main class="app-shell__content">
      <slot />
    </main>
  </div>
</template>