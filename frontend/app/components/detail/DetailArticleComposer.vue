<script setup lang="ts">
const { commentDraft, submitComment } = useArticleDetail()
</script>

<template>
  <div class="comment-composer">
    <div class="comment-composer__head">
      <h3 class="comment-composer__title">Tulis komentar</h3>
      <span class="comment-composer__hint">Singkat dan jelas lebih mudah dibaca.</span>
    </div>

    <textarea
      v-model="commentDraft"
      class="comment-composer__textarea"
      rows="4"
      placeholder="Bagikan pengalaman, pendapat, atau insight Anda..."
    />

    <div class="comment-composer__actions">
      <BaseButton @click="submitComment()">
        Kirim komentar
      </BaseButton>
    </div>
  </div>
</template>

<style scoped>
.comment-composer {
  padding: 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.12);
}

.comment-composer__head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 12px;
}

.comment-composer__title {
  font-size: 16px;
  line-height: 1.2;
  font-weight: 700;
  color: var(--text-primary);
}

.comment-composer__hint {
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.5;
}

.comment-composer__textarea {
  width: 100%;
  resize: vertical;
  min-height: 110px;
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

.comment-composer__textarea:focus {
  border-color: rgba(106, 173, 168, 0.34);
}

.comment-composer__actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 640px) {
  .comment-composer {
    padding: 14px;
  }

  .comment-composer__head {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .comment-composer__actions {
    justify-content: stretch;
  }
}
</style>