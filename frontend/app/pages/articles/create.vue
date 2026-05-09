<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: 'auth'
})
</script>

<template>
  <BasePageShell>
    <section class="article-form-page">
      <div class="article-form-card">
        <DetailArticleForm mode="create" />
      </div>
    </section>
  </BasePageShell>
</template>

<style scoped>
.article-form-page {
  display: flex;
  justify-content: center;
  padding: 8px 0 40px;
}

.article-form-card {
  width: min(100%, 1120px);
  margin: 0 auto;
  padding: 36px;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: 0 8px 22px rgba(60, 55, 50, 0.06);
  contain: layout paint style;
}

/*
  Override ringan untuk field di DetailArticleForm
  tanpa perlu ubah component-nya.
*/
.article-form-card :deep(.article-form__input),
.article-form-card :deep(.article-form__textarea) {
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
}

.article-form-card :deep(.article-form__field),
.article-form-card :deep(.article-form__image-card),
.article-form-card :deep(.article-form__note) {
  background: rgba(255, 255, 255, 0.08);
}

@media (max-width: 640px) {
  .article-form-card {
    padding: 28px 20px;
  }
}
</style>