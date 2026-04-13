<script setup lang="ts">
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value: string) => ['primary', 'ghost', 'account'].includes(value)
  }
})
</script>

<template>
  <div class="glass-card" :class="`glass-card--${variant}`">
    <slot />
  </div>
</template>

<style scoped>
.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 40px;
  box-shadow: var(--glass-shadow);
  position: relative;
  overflow: hidden;
}

.glass-card--account {
  padding: 56px;
}

.glass-card--ghost {
  box-shadow: none;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
</style>
