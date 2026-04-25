<script setup lang="ts">
const {
  article,
  averageRating,
  visibleStars,
  ratingSummaryLabel,
  ratingDraft,
  hoverRating,
  setRating
} = useArticleDetail()
</script>

<template>
  <div class="content-block">
    <div class="content-block__header">
      <div>
        <h2 class="content-block__title">Rating pengguna</h2>
        <p class="content-block__helper">{{ ratingSummaryLabel }}</p>
      </div>

      <div class="content-block__score">
        <span class="content-block__score-value">{{ averageRating }}</span>
        <span class="content-block__score-meta">dari {{ article.ratings?.length ?? 0 }} rating</span>
      </div>
    </div>

    <div class="content-block__rating-row">
      <DetailRatingStars
        :model-value="visibleStars"
        size="lg"
        @update:model-value="setRating"
        @hover="hoverRating = $event"
        @leave="hoverRating = 0"
      />

      <span v-if="ratingDraft" class="content-block__chosen-rating">
        Rating Anda: {{ ratingDraft }}/5
      </span>
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

.content-block__header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 14px;
}

.content-block__helper {
  margin-top: 6px;
  color: var(--text-secondary);
  font-size: 13px;
}

.content-block__score {
  text-align: right;
}

.content-block__score-value {
  display: block;
  font-size: 28px;
  font-weight: 800;
  line-height: 1;
  color: var(--text-primary);
}

.content-block__score-meta {
  font-size: 12px;
  color: var(--text-secondary);
}

.content-block__rating-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.content-block__chosen-rating {
  border-radius: 12px;
  padding: 7px 12px;
  background: rgba(106, 173, 168, 0.1);
  color: var(--primary-cyan);
  font-size: 12px;
  font-weight: 700;
}

@media (max-width: 640px) {
  .content-block {
    padding: 18px;
  }

  .content-block__header {
    flex-direction: column;
    align-items: stretch;
  }

  .content-block__score {
    text-align: left;
  }
}
</style>