<script setup lang="ts">
const { allTags, activeTag, setTag } = useArticleFilter()
</script>

<template>
  <div class="tag-filter" role="group" aria-label="Filter kategori">
    <button
      class="tag-filter__pill"
      :class="{ 'tag-filter__pill--active': activeTag === '' }"
      @click="activeTag = ''"
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
  flex-wrap: wrap;
  gap: 8px;
}

.tag-filter__pill {
  padding: 5px 10px;
  border-radius: 10px;
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  color: var(--text-secondary);
  font-family: var(--font-base);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: all 0.2s ease;
  white-space: nowrap;
}

.tag-filter__pill:hover {
  background: rgba(106, 173, 168, 0.1);
  border-color: var(--primary-cyan);
  color: var(--primary-cyan);
  transform: translateY(-1px);
}

.tag-filter__pill--active {
  background: var(--primary-cyan);
  border-color: var(--primary-cyan);
  color: white;
}

.tag-filter__pill--active:hover {
  background: var(--hover-cyan);
  border-color: var(--hover-cyan);
  color: white;
}
</style>
