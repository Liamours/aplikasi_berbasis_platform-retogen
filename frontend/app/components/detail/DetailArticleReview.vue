<script setup lang="ts">
const { articleParagraphs } = useArticleDetail()
</script>

<template>
  <div class="content-block">
    <h2 class="content-block__title">Review</h2>

    <div class="content-block__body">
      <p
        v-for="(paragraph, index) in articleParagraphs"
        :key="index"
        class="content-block__paragraph"
      >
        {{ paragraph }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.content-block {
  min-width: 0;
  overflow: hidden;
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
  min-width: 0;
  margin-top: 14px;
  display: grid;
  gap: 14px;
  color: var(--text-secondary);
}

.content-block__paragraph {
  max-width: 100%;
  min-width: 0;
  line-height: 1.75;
  white-space: pre-line;
  overflow-wrap: anywhere;
  word-break: break-word;
}

@media (max-width: 640px) {
  .content-block {
    padding: 18px;
  }
}
</style>