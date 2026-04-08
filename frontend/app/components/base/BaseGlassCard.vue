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
    <div class="glass-card__accent" />
    <slot />
  </div>
</template>

<style scoped>
.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 40px;
  box-shadow: var(--glass-shadow);
  position: relative;
  overflow: hidden;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 1px;
  border-radius: 24px;
  background: linear-gradient(135deg, var(--glass-edge), transparent 50%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.glass-card:hover {
  transform: translateY(-4px);
}

.glass-card__accent {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-red), var(--primary-cyan));
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