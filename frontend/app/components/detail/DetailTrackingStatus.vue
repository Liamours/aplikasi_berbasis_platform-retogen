<script setup lang="ts">
const { article } = useArticleDetail()
</script>

<template>
  <aside class="article-detail-side">
    <DetailPriceTracker
      :prices="article.prices ?? []"
    />
  </aside>
</template>

<style scoped>
.article-detail-side {
  display: block;
}
</style>