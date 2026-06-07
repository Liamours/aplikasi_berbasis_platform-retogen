<script setup lang="ts">
const { allTags, activeTag, setTag, fetchArticles } = useArticleFilter()

function clearTag() {
  activeTag.value = ''
  fetchArticles()
}
</script>

<template>
  <div class="tag-filter" role="group" aria-label="Filter kategori">

    <button
      class="tag-filter__pill"
      :class="{ 'tag-filter__pill--active': activeTag === '' }"
      @click="clearTag"
    >
      Semua
    </button>

    <button
      v-for="tag in allTags"
      :key="tag"
      class="tag-filter__pill"
      :class="{ 'tag-filter__pill--active': activeTag === tag }"
      @click="setTag(tag)"
    >
      {{ tag }}
    </button>

  </div>
</template>

<style scoped>
.tag-filter {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.tag-filter__pill {
  padding: 5px 12px;
  border: 1px solid var(--glass-border);
  border-radius: 10px;
  background: var(--glass-bg);
  color: var(--text-secondary);
  font-family: var(--font-base);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.tag-filter__pill:hover {
  background: rgba(106, 173, 168, 0.1);
  color: var(--primary-cyan);
  border-color: var(--primary-cyan);
}

.tag-filter__pill--active {
  background: var(--primary-cyan);
  color: white;
  border-color: var(--primary-cyan);
}

.tag-filter__pill--active:hover {
  background: var(--hover-cyan);
}
</style>
