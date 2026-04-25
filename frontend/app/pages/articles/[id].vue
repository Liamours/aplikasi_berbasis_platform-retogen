<script setup lang="ts">
definePageMeta({ layout: 'default' })

const route = useRoute()
const { resetPageState } = useArticleDetail()

watch(() => route.params.id, (id) => {
  resetPageState(String(id || 'demo-article'))
}, { immediate: true })
</script>

<template>
  <BasePageShell>
    <div class="detail-page">
      <BaseGlassCard class="detail-card">
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
      <DetailDeleteCommentModal />
    </div>
  </BasePageShell>
</template>

<style scoped>
.detail-page {
  display: flex;
  justify-content: center;
  padding: 8px 0 40px;
}

.detail-card {
  width: min(100%, 1080px);
  margin: 0 auto;
}

.detail-card__grid {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(300px, 0.8fr);
  gap: 24px;
  align-items: start;
}

.detail-card__main {
  display: grid;
  gap: 18px;
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