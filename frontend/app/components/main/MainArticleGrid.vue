<script setup lang="ts">
const { articles, isLoading, fetchError, searchQuery, activeTag } = useArticleFilter()
</script>

<template>
  <div>
    <!-- Loading skeleton -->
    <div v-if="isLoading" class="skeleton-grid">
      <div v-for="n in 6" :key="n" class="skeleton-card" />
    </div>

    <!-- Error state -->
    <div v-else-if="fetchError" class="error-banner fetch-error">
      ⚠ {{ fetchError }}
    </div>

    <!-- Results -->
    <template v-else>
      <!-- Result count -->
      <p class="grid-meta">
        Menampilkan <strong>{{ articles.length }}</strong> artikel
        <template v-if="activeTag">
          · tag: <span class="grid-meta__tag">{{ activeTag }}</span>
        </template>
        <template v-if="searchQuery.trim()">
          · pencarian: "<em>{{ searchQuery }}</em>"
        </template>
      </p>

      <TransitionGroup
        v-if="articles.length"
        name="glass-list"
        tag="div"
        class="article-grid"
      >
        <MainArticleCard
          v-for="article in articles"
          :key="article.article_id"
          :article="article"
        />
      </TransitionGroup>

      <MainArticleEmpty v-else />
    </template>
  </div>
</template>

<style scoped>
/* ── Loading skeleton ────────────────────── */
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.skeleton-card {
  height: 280px;
  border-radius: var(--radius-lg);
  background: linear-gradient(
    90deg,
    var(--bg-surface) 25%,
    rgba(160,155,145,0.1) 50%,
    var(--bg-surface) 75%
  );
  background-size: 400% 100%;
  animation: skeleton-shimmer 1.4s ease infinite;
  border: 1px solid var(--glass-border);
}

@keyframes skeleton-shimmer {
  0%   { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

/* ── Error ───────────────────────────────── */
.fetch-error {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 20px;
  font-size: 14px;
}

/* ── Meta + Grid ─────────────────────────── */
.grid-meta {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 20px;
}

.grid-meta strong { color: var(--text-primary); font-weight: 700; }
.grid-meta__tag   { color: var(--primary-red); font-weight: 600; }

.article-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.glass-list-enter-active { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.glass-list-enter-from   { opacity: 0; transform: translateY(16px); }
.glass-list-move         { transition: transform 0.4s ease; }

@media (max-width: 1024px) {
  .article-grid,
  .skeleton-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .article-grid,
  .skeleton-grid { grid-template-columns: 1fr; }
}
</style>
