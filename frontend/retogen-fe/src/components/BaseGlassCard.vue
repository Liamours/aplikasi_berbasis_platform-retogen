<template>
  <div class="glass-card" :class="variantClass">
    <div class="glass-card__accent" />
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  variant?: 'primary' | 'ghost' | 'account'
}>()

const variantClass = computed(() => `glass-card--${props.variant ?? 'primary'}`)
</script>

<style scoped>
.glass-card {
  position: relative;
  overflow: hidden;
  border-radius: 24px;
  border: 1px solid var(--glass-border);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.45), rgba(255, 255, 255, 0.15));
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  padding: 40px;
}

.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 1px;
  border-radius: 24px;
  background: linear-gradient(135deg, var(--glass-edge), transparent 50%);
  -webkit-mask:
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.glass-card__accent {
  position: absolute;
  top: 0;
  left: 0;
  height: 4px;
  width: 100%;
  background: linear-gradient(90deg, var(--primary-red), var(--primary-cyan));
}

.glass-card--ghost {
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: none;
}

.glass-card--account {
  padding: 56px;
}
</style>

