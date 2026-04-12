<script setup lang="ts">
import type { ArticleCard } from '~/types/api'

defineProps<{ article: ArticleCard }>()

const TAG_COLORS: Record<string, 'red' | 'cyan'> = {
  smartphone: 'red',  laptop: 'cyan',  audio: 'red',   display: 'cyan',
  gaming: 'red',      processor: 'cyan', kamera: 'red', tws: 'cyan',
  tv: 'red',          oled: 'cyan',    aksesoris: 'red', produktivitas: 'cyan',
  ultrabook: 'red',   budget: 'cyan',
}

function tagColor(tag: string): string {
  const color = TAG_COLORS[tag]
  return color ? `article-tag--${color}` : 'article-tag--neutral'
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('id-ID', {
    day: 'numeric', month: 'short', year: 'numeric',
  })
}
</script>

<template>
  <NuxtLink :to="`/articles/${article.article_id}`" class="article-card-link">
  <article class="article-card">
    <!-- Image placeholder frame -->
    <div class="article-card__image" aria-hidden="true">
      <span class="article-card__image-label">{{ article.article_tags[0] }}</span>
    </div>

    <!-- Body -->
    <div class="article-card__body">
      <div class="article-card__tags">
        <span
          v-for="tag in article.article_tags"
          :key="tag"
          class="article-tag"
          :class="tagColor(tag)"
        >{{ tag }}</span>
      </div>

      <h2 class="article-card__title">{{ article.article_title }}</h2>
      <p class="article-card__preview">{{ article.article_preview }}</p>

      <footer class="article-card__footer">
        <div class="article-card__rating">
          <span class="article-card__star" aria-hidden="true">★</span>
          <span class="article-card__rating-value">{{ article.rating_avg.toFixed(1) }}</span>
        </div>
        <div class="article-card__meta">
          <span>{{ article.comment_count }} komentar</span>
          <time :datetime="article.created_at">{{ formatDate(article.created_at) }}</time>
        </div>
      </footer>
    </div>
  </article>
  </NuxtLink>
</template>

<style scoped>
.article-card-link {
  display: contents;
  text-decoration: none;
  color: inherit;
}

.article-card {
  position: relative;
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--glass-shadow);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.article-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px 0 rgba(60, 55, 50, 0.12);
}

/* Image placeholder frame — dashed border signals "image goes here" */
.article-card__image {
  position: relative;
  height: 140px;
  background: var(--bg-surface);
  border-bottom: 1px dashed var(--glass-border);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.article-card__image-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--text-muted);
}

/* Body */
.article-card__body {
  padding: 20px 22px 22px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

/* Inline tags */
.article-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.article-tag {
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 600;
}

.article-tag--red     { background: rgba(181,107,82,0.1);  color: var(--primary-red); }
.article-tag--cyan    { background: rgba(106,173,168,0.1); color: var(--primary-cyan); }
.article-tag--neutral { background: rgba(100,100,100,0.08); color: var(--text-secondary); }

/* Title */
.article-card__title {
  margin: 0;
  font-size: 16px;
  font-weight: 700;
  line-height: 1.35;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Preview */
.article-card__preview {
  margin: 0;
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

/* Footer */
.article-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 10px;
  border-top: 1px solid var(--glass-border);
  margin-top: auto;
}

.article-card__rating {
  display: flex;
  align-items: center;
  gap: 4px;
}

.article-card__star         { color: var(--primary-red); font-size: 14px; }
.article-card__rating-value { font-size: 13px; font-weight: 700; color: var(--text-primary); }

.article-card__meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: var(--text-muted);
}
</style>
