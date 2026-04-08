<script setup lang="ts">
defineProps<{
  title: string
}>()
</script>

<template>
  <BaseGlassCard variant="ghost" class="sidebar-card">
    <h3 class="sidebar-card__title">
      {{ title }}
    </h3>
    <div class="sidebar-card__content">
      <slot />
    </div>
  </BaseGlassCard>
</template>

<style scoped>
.sidebar-card {
  padding: 24px;
}

.sidebar-card__title {
  margin: 0 0 14px;
  font-size: 18px;
  line-height: 1.2;
  font-weight: 700;
  color: var(--text-primary);
}

.sidebar-card__content {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
</style>