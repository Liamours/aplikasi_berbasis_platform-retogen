<script setup lang="ts">
import DetailDeleteArticleModal from '~/components/detail/DetailDeleteArticleModal.vue'
import DetailDeleteCommentModal from '~/components/detail/DetailDeleteCommentModal.vue'
import DetailReportLogModal from '~/components/detail/DetailReportLogModal.vue'

definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

const route = useRoute()

const {
  resetPageState,
  isLoading,
  error
} = useArticleDetail()

const { isDark } = useTheme()

useHead({
  htmlAttrs: {
    class: computed(() => isDark.value ? 'dark-mode' : '')
  }
})

watch(
  () => route.params.id,
  async (id) => {
    const articleId = Array.isArray(id) ? id[0] : String(id || '')

    if (!articleId) {
      await navigateTo('/main')
      return
    }

    await resetPageState(articleId)
  },
  { immediate: true }
)
</script>

<template>
  <BasePageShell>
    <div class="detail-page">
      <BaseGlassCard v-if="isLoading" class="detail-card">
        <p class="detail-feedback">
          Memuat artikel...
        </p>
      </BaseGlassCard>

      <BaseGlassCard v-else-if="error" class="detail-card">
        <p class="detail-feedback detail-feedback--error">
          {{ error }}
        </p>
      </BaseGlassCard>

      <BaseGlassCard v-else class="detail-card">
        <DetailArticleHero />

        <div class="detail-card__grid">
          <section class="detail-card__main">
            <DetailArticleReview />
            <DetailArticleRating />
          </section>

          <DetailTrackingStatus />
        </div>

        <DetailArticleDiscussion />
      </BaseGlassCard>

      <DetailReportModal />

      <ClientOnly>
        <DetailReportLogModal />
        <DetailDeleteCommentModal />
        <DetailDeleteArticleModal />
      </ClientOnly>
    </div>
  </BasePageShell>
</template>

<style scoped>
.detail-page {
  display: flex;
  justify-content: center;
  padding: 8px 0 40px;
  background: var(--bg-page);
  min-height: calc(100vh - var(--navbar-height));
}

.detail-card {
  width: min(100%, 1080px);
  margin: 0 auto;
  isolation: isolate;
  backdrop-filter: blur(16px) saturate(140%) !important;
  contain: layout;
}

.detail-feedback {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.detail-feedback--error {
  color: var(--primary-red);
}

.detail-card__grid {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(300px, 0.8fr);
  gap: 24px;
  align-items: start;
}

.detail-card__grid > * {
  min-width: 0;
}

.detail-card__main {
  display: grid;
  gap: 18px;
  min-width: 0;
}

@media (max-width: 1024px) {
  .detail-card__grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .detail-card {
    padding: 28px 20px;
  }
}
</style>