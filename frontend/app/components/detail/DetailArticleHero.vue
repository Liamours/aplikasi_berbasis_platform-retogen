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

      <DetailReportMenu
        report-label="Laporkan artikel"
        @report="openReport('article', article.article_id)"
      />
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

        <h1 class="hero__title">
          {{ article.article_title }}
        </h1>

        <p class="hero__preview">
          {{ article.article_preview }}
        </p>

        <div class="hero__tags">
          <span
            v-for="tag in article.article_tags"
            :key="tag"
            class="hero__tag"
          >
            {{ tag }}
          </span>
        </div>

        <div class="hero__meta" aria-label="Ringkasan artikel">
          <span class="hero__meta-item">
            <strong>{{ averageRating }}/5</strong>
            Rating
          </span>

          <span class="hero__meta-separator" aria-hidden="true">·</span>

          <span class="hero__meta-item">
            <strong>{{ totalComments }}</strong>
            Komentar
          </span>

          <span
            v-if="lowestPrice"
            class="hero__meta-separator"
            aria-hidden="true"
          >
            ·
          </span>

          <span v-if="lowestPrice" class="hero__meta-item">
            <strong>{{ formatPrice(lowestPrice.price) }}</strong>
            Harga terbaik
          </span>
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

.hero__crumb {
  color: var(--text-secondary);
}

.hero__crumb:hover {
  color: var(--primary-cyan);
}

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

.hero__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero__summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

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

.hero__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hero__tag {
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  background: rgba(181, 107, 82, 0.1);
  color: var(--primary-red);
}

.hero__meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 10px;
  padding-top: 2px;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.5;
}

.hero__meta-item {
  display: inline-flex;
  align-items: baseline;
  gap: 5px;
  min-width: 0;
}

.hero__meta-item strong {
  color: var(--text-primary);
  font-weight: 700;
}

.hero__meta-separator {
  color: var(--text-muted);
}

@media (max-width: 850px) {
  .hero__headline {
    grid-template-columns: 1fr;
  }

  .hero__image-wrap {
    min-height: 220px;
  }
}

@media (max-width: 480px) {
  .hero {
    gap: 20px;
  }

  .hero__topbar {
    align-items: flex-start;
  }

  .hero__headline {
    gap: 22px;
  }

  .hero__summary {
    gap: 14px;
  }

  .hero__meta {
    align-items: flex-start;
    flex-direction: column;
    gap: 4px;
  }

  .hero__meta-separator {
    display: none;
  }
}
</style>