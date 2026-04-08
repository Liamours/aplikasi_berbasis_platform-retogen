<script setup lang="ts">
const { filteredArticles, searchQuery, activeTag } = useArticleFilter()
</script>

<template>
  <div>
    <!-- Result count -->
    <p class="grid-meta">
      Menampilkan <strong>{{ filteredArticles.length }}</strong> artikel
      <template v-if="activeTag">
        · tag: <span class="grid-meta__tag">{{ activeTag }}</span>
      </template>
      <template v-if="searchQuery.trim()">
        · pencarian: "<em>{{ searchQuery }}</em>"
      </template>
    </p>

    <!-- Article grid -->
    <TransitionGroup
      v-if="filteredArticles.length"
      name="glass-list"
      tag="div"
      class="article-grid"
    >
      <MainArticleCard
        v-for="article in filteredArticles"
        :key="article.article_id"
        :article="article"
      />
    </TransitionGroup>

    <!-- Empty state -->
    <MainArticleEmpty v-else />
  </div>
</template>

<style scoped>
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

/* TransitionGroup animations (matching global glass-list in main.css) */
.glass-list-enter-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.glass-list-enter-from { opacity: 0; transform: translateY(16px); }
.glass-list-move       { transition: transform 0.4s ease; }

@media (max-width: 1024px) { .article-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px)  { .article-grid { grid-template-columns: 1fr; } }
</style>
