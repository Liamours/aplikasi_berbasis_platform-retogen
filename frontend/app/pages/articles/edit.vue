<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

const route = useRoute()

const articleId = computed(() => String(route.query.id || ''))

const isValidArticleId = computed(() => {
  return /^[a-fA-F0-9]{24}$/.test(articleId.value)
})

watch(
  articleId,
  async (id) => {
    if (!/^[a-fA-F0-9]{24}$/.test(id)) {
      await navigateTo('/main')
    }
  },
  { immediate: true }
)
</script>

<template>
  <BasePageShell>
    <section class="article-form-page">
      <div class="article-form-card">
        <DetailArticleForm
          v-if="isValidArticleId"
          mode="edit"
          :article-id="articleId"
        />

        <p v-else class="article-form-feedback">
          Mengalihkan ke halaman utama.
        </p>
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

.article-form-feedback {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

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