<script setup lang="ts">
definePageMeta({ middleware: ['auth'] })

const { fetchArticles } = useArticleFilter()

onMounted(fetchArticles)
</script>

<template>
  <BasePageShell>
    <MainPageHeader />
    <MainArticleControls />
    <MainTagFilter />
    <MainArticleGrid />
  </BasePageShell>
</template>
