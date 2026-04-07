<script setup lang="ts">
defineProps<{
  title: string
  description: string
  badge?: string
}>()
</script>

<template>
  <BaseGlassCard class="feature-card">
    <div v-if="badge" class="feature-card__badge">
      {{ badge }}
    </div>

    <h3 class="feature-card__title">
      {{ title }}
    </h3>

    <p class="feature-card__description">
      {{ description }}
    </p>
  </BaseGlassCard>
</template>

<style scoped>
.feature-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.feature-card__badge {
  width: fit-content;
  padding: 6px 14px;
  border-radius: 20px;
  background: rgba(227, 66, 52, 0.1);
  color: var(--primary-red);
  font-size: 12px;
  font-weight: 600;
}

.feature-card__title {
  margin: 0;
  font-size: 22px;
  line-height: 1.2;
  font-weight: 700;
  color: var(--text-primary);
}

.feature-card__description {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>