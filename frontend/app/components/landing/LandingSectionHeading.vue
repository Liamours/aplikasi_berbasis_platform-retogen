<script setup lang="ts">
defineProps<{
  eyebrow?: string
  title: string
  description: string
}>()
</script>

<template>
  <div class="section-heading">
    <p v-if="eyebrow" class="section-heading__eyebrow">
      {{ eyebrow }}
    </p>

    <h2 class="section-heading__title">
      {{ title }}
    </h2>

    <p class="section-heading__description">
      {{ description }}
    </p>
  </div>
</template>

<style scoped>
.section-heading {
  max-width: 760px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-heading__eyebrow {
  margin: 0;
  color: var(--primary-red);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.section-heading__title {
  margin: 0;
  font-size: clamp(32px, 4vw, 36px);
  line-height: 1.15;
  font-weight: 700;
  color: var(--text-primary);
}

.section-heading__description {
  margin: 0;
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-secondary);
}
</style>