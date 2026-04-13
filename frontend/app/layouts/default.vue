<script setup lang="ts">
const { isDark } = useTheme()
</script>

<template>
  <div class="app-shell" :class="{ 'dark-mode': isDark }">
    <BaseBackground />
    <BaseNavbar />
    <main class="app-shell__content">
      <slot />
    </main>
  </div>
</template>
