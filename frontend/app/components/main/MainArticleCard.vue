<script setup lang="ts">
import type { ArticleListItem } from '~/types/api'

defineProps<{ article: ArticleListItem }>()

/** Hash tag string → consistent red/cyan, no hardcoded dictionary. */
function tagColor(tag: string): string {
  const hash = tag.split('').reduce((acc, c) => acc + c.charCodeAt(0), 0)
  return hash % 2 === 0 ? 'article-tag--cyan' : 'article-tag--red'
}

/** Detect PNG vs JPEG from base64 header, return valid data URL. */
function toDataUrl(b64: string): string {
  const mime = b64.startsWith('iVBOR') ? 'image/png' : 'image/jpeg'
  return `data:${mime};base64,${b64}`
}
</script>

<template>
  <NuxtLink :to="`/articles/${article.article_id}`" class="article-card-link">
    <article class="article-card">

      <!-- Image: real base64 when available, placeholder when null -->
      <div class="article-card__thumb">
        <img
          v-if="article.article_image"
          :src="toDataUrl(article.article_image)"
          :alt="article.article_title"
          class="article-card__img"
        >
        <span v-else class="article-card__placeholder-label">
          {{ article.article_tags?.[0] ?? 'artikel' }}
        </span>
      </div>

      <!-- Body -->
      <div class="article-card__body">
        <div v-if="article.article_tags?.length" class="article-card__tags">
          <span
            v-for="tag in article.article_tags"
            :key="tag"
            class="article-tag"
            :class="tagColor(tag)"
          >{{ tag }}</span>
        </div>

        <h2 class="article-card__title">{{ article.article_title }}</h2>
        <p class="article-card__preview">{{ article.article_preview }}</p>
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

/* ── Thumbnail ───────────────────────────── */
.article-card__thumb {
  position: relative;
  height: 160px;
  flex-shrink: 0;
  overflow: hidden;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--glass-border);
  display: flex;
  align-items: center;
  justify-content: center;
}

.article-card__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* Placeholder shown when no image */
.article-card__placeholder-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--text-muted);
}

/* ── Body ────────────────────────────────── */
.article-card__body {
  padding: 18px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}

.article-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.article-tag {
  padding: 3px 8px;
  border-radius: var(--radius-sm);
  font-size: 11px;
  font-weight: 600;
}

.article-tag--red  { background: rgba(181,107,82,0.1);  color: var(--primary-red); }
.article-tag--cyan { background: rgba(106,173,168,0.1); color: var(--primary-cyan); }

.article-card__title {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
  line-height: 1.35;
  color: var(--text-primary);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-card__preview {
  margin: 0;
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
