<script setup lang="ts">
defineProps<{
  to?: string      // if set → renders NuxtLink, else → button
  danger?: boolean
}>()

defineEmits<{ click: [] }>()
</script>

<template>
  <NuxtLink
    v-if="to"
    :to="to"
    class="dropdown-item"
    :class="{ 'dropdown-item--danger': danger }"
    @click="$emit('click')"
  >
    <slot />
  </NuxtLink>

  <button
    v-else
    class="dropdown-item"
    :class="{ 'dropdown-item--danger': danger }"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<style scoped>
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 9px 10px;
  border-radius: 10px;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-family: var(--font-base);
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: var(--transition-fast);
  text-align: left;
}

.dropdown-item:hover {
  background: rgba(106, 173, 168, 0.08);
  color: var(--primary-cyan);
}

.dropdown-item--danger:hover {
  background: rgba(181, 107, 82, 0.08);
  color: var(--primary-red);
}
</style>
