<script setup lang="ts">
defineProps<{
  author: string
  publishedAt: string
  readingTime: string
}>()
</script>

<template>
  <div class="article-meta">
    <span class="article-meta__item">
      By <strong>{{ author }}</strong>
    </span>
    <span class="article-meta__dot" />
    <span class="article-meta__item">{{ publishedAt }}</span>
    <span class="article-meta__dot" />
    <span class="article-meta__item">{{ readingTime }}</span>
  </div>
</template>

<style scoped>
.article-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  color: var(--text-secondary);
  font-size: 13px;
}

.article-meta__item strong {
  color: var(--text-primary);
  font-weight: 600;
}

.article-meta__dot {
  width: 4px;
  height: 4px;
  border-radius: 999px;
  background: var(--text-muted);
}
</style>