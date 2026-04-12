<script setup lang="ts">
const { commentDraft, submitComment } = useArticleDetail()
</script>

<template>
  <div class="content-block">
    <h2 class="content-block__title">Tulis komentar</h2>

    <textarea
      v-model="commentDraft"
      class="article-textarea"
      rows="5"
      placeholder="Bagikan pengalaman, pendapat, atau insight singkat Anda..."
    />

    <div class="content-block__composer-actions">
      <span class="content-block__hint">Komentar singkat dan jelas akan lebih mudah dibaca.</span>
      <BaseButton @click="submitComment()">Kirim komentar</BaseButton>
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

.article-textarea {
  width: 100%;
  resize: vertical;
  min-height: 120px;
  margin-top: 14px;
  border-radius: 14px;
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
  padding: 14px;
  outline: none;
  font: inherit;
  line-height: 1.65;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.content-block__composer-actions {
  margin-top: 14px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

.content-block__hint { color: var(--text-secondary); font-size: 13px; }

@media (max-width: 640px) {
  .content-block { padding: 18px; }
  .content-block__composer-actions { flex-direction: column; align-items: stretch; }
}
</style>
