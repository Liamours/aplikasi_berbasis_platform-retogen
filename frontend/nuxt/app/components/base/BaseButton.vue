<script setup lang="ts">
type Variant = 'primary' | 'destructive' | 'ghost' | 'icon'

withDefaults(defineProps<{
  variant?: Variant
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  block?: boolean
}>(), {
  variant: 'primary',
  type: 'button',
  disabled: false,
  block: false
})
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="base-button"
    :class="[
      `base-button--${variant}`,
      { 'base-button--block': block }
    ]"
  >
    <slot />
  </button>
</template>

<style scoped>
.base-button {
  border: none;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-standard);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.base-button--block {
  width: 100%;
}

.base-button--primary {
  padding: 14px 32px;
  background: var(--primary-cyan);
  color: white;
  box-shadow: 0 4px 20px rgba(0, 206, 209, 0.3);
}

.base-button--primary:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 206, 209, 0.4);
}

.base-button--destructive {
  padding: 14px 32px;
  background: var(--primary-red);
  color: white;
}

.base-button--destructive:hover:not(:disabled) {
  transform: translateY(-2px);
}

.base-button--ghost {
  padding: 14px 24px;
  background: rgba(255,255,255,0.05);
  color: var(--text-primary);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.base-button--icon {
  width: 40px;
  height: 40px;
  border-radius: 999px;
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--glass-border);
}

.base-button--icon:hover:not(:disabled) {
  transform: scale(1.05);
  background: rgba(0, 206, 209, 0.12);
}

.base-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}
</style>