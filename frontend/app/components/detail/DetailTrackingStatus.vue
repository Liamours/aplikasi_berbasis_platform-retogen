<script setup lang="ts">
const { article, tracked, toggleTrackPrice } = useArticleDetail()
</script>

<template>
  <aside class="article-detail-side">
    <DetailPriceTracker
      :prices="article.prices ?? []"
      :tracked="tracked"
      @toggle-track="toggleTrackPrice"
    />
  </aside>
</template>

<style scoped>
.article-detail-side {
  display: block;
}
</style>