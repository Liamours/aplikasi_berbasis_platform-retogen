<script setup lang="ts">
const { article, averageRating, totalComments, lowestPrice, formatPrice, openReport } = useArticleDetail()
</script>

<template>
  <div class="hero">
    <div class="hero__topbar">
      <div class="hero__breadcrumbs">
        <NuxtLink to="/" class="hero__crumb">Home</NuxtLink>
        <span>/</span>
        <span>Article</span>
      </div>
      <DetailReportMenu @report="openReport('article', article.article_id)" />
    </div>

    <div class="hero__headline">
      <div class="hero__image-wrap">
        <img
          :src="article.article_image || '/logo.jpg'"
          :alt="article.article_title"
          class="hero__image"
        >
      </div>

      <div class="hero__summary">
        <p class="hero__eyebrow">Electronic review</p>
        <h1 class="hero__title">{{ article.article_title }}</h1>
        <p class="hero__preview">{{ article.article_preview }}</p>

        <div class="hero__tags">
          <span v-for="tag in article.article_tags" :key="tag" class="hero__tag">{{ tag }}</span>
        </div>

        <div class="hero__stats">
          <div class="hero__stat">
            <span class="hero__stat-label">Rating</span>
            <strong class="hero__stat-value">{{ averageRating }}/5</strong>
          </div>
          <div class="hero__stat">
            <span class="hero__stat-label">Komentar</span>
            <strong class="hero__stat-value">{{ totalComments }}</strong>
          </div>
          <div class="hero__stat">
            <span class="hero__stat-label">Harga terbaik</span>
            <strong class="hero__stat-value">{{ lowestPrice ? formatPrice(lowestPrice.price) : '-' }}</strong>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 32px;
}

.hero__topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.hero__breadcrumbs {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 13px;
}

.hero__crumb { color: var(--text-secondary); }

.hero__headline {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 28px;
  align-items: center;
}

.hero__image-wrap {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  border: 1px dashed var(--glass-border);
  background: var(--bg-surface);
  min-height: 260px;
}

.hero__image { width: 100%; height: 100%; object-fit: cover; }

.hero__summary { display: flex; flex-direction: column; gap: 16px; }

.hero__eyebrow {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
}

.hero__title {
  font-size: clamp(30px, 4vw, 44px);
  line-height: 1.08;
  font-weight: 800;
  letter-spacing: -1px;
  color: var(--text-primary);
}

.hero__preview {
  max-width: 64ch;
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.7;
}

.hero__tags { display: flex; flex-wrap: wrap; gap: 10px; }

.hero__tag {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  background: rgba(181, 107, 82, 0.1);
  color: var(--primary-red);
}

.hero__stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.hero__stat {
  padding: 16px;
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid var(--glass-border);
}

.hero__stat-label {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.hero__stat-value {
  font-size: 18px;
  color: var(--text-primary);
  font-weight: 700;
}

@media (max-width: 850px) {
  .hero__headline { grid-template-columns: 1fr; }
  .hero__image-wrap { min-height: 220px; }
  .hero__stats { grid-template-columns: 1fr; }
}
</style>
