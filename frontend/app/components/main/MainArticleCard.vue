<script setup lang="ts">
import type { ArticleCard } from '~/types/api'

defineProps<{ article: ArticleCard }>()

/** Cycles tag color between red and cyan for visual variety. */
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
  <article class="article-card">
    <div class="article-card__accent" aria-hidden="true" />

    <!-- Image / placeholder -->
    <div class="article-card__image" aria-hidden="true">
      <span class="article-card__image-label">{{ article.article_tags[0] }}</span>
      <div class="article-card__image-glow" />
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
          <span title="Komentar">💬 {{ article.comment_count }}</span>
          <time :datetime="article.created_at">{{ formatDate(article.created_at) }}</time>
        </div>
      </footer>
    </div>
  </article>
</template>

<style scoped>
/* Glass surface — follows BaseGlassCard pattern, applied here because
   the article card has a unique image-then-body layout that requires
   overflow:hidden and no top padding on the image section. */
.article-card {
  position: relative;
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  box-shadow: var(--glass-shadow);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  cursor: pointer;
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
}

/* Edge highlight (light-catcher) */
.article-card::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 1px;
  border-radius: 24px;
  background: linear-gradient(135deg, var(--glass-edge), transparent 50%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  pointer-events: none;
  z-index: 1;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 48px 0 rgba(60, 55, 50, 0.14);
}

/* Gradient accent bar */
.article-card__accent {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 4px;
  background: linear-gradient(90deg, var(--primary-red), var(--primary-cyan));
  z-index: 2;
}

/* Image placeholder */
.article-card__image {
  position: relative;
  height: 140px;
  background: linear-gradient(135deg, rgba(181,107,82,0.12), rgba(106,173,168,0.10));
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  flex-shrink: 0;
}

.article-card__image-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--text-muted);
  position: relative;
  z-index: 1;
}

.article-card__image-glow {
  position: absolute;
  inset: auto -30px -40px auto;
  width: 160px; height: 160px;
  border-radius: 999px;
  background: rgba(106, 173, 168, 0.18);
  filter: blur(50px);
  pointer-events: none;
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
  padding: 4px 10px;
  border-radius: 20px;
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
