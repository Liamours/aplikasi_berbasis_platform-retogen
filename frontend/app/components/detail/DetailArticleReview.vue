<script setup lang="ts">
const { articleParagraphs } = useArticleDetail()
</script>

<template>
  <div class="content-block">
    <h2 class="content-block__title">Review</h2>
    <div class="content-block__body">
      <p v-for="(paragraph, index) in articleParagraphs" :key="index">{{ paragraph }}</p>
    </div>
  </div>
</template>

<style scoped>
.content-block {
  border-radius: 20px;
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.14);
  padding: 22px;
}

.content-block__title {
  font-size: 20px;
  line-height: 1.1;
  font-weight: 700;
  color: var(--text-primary);
}

.content-block__body {
  margin-top: 14px;
  display: grid;
  gap: 14px;
  color: var(--text-secondary);
}

.content-block__body p { line-height: 1.75; }

@media (max-width: 640px) {
  .content-block { padding: 18px; }
}
</style>
