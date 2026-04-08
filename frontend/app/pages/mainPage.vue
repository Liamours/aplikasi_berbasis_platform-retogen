<script setup lang="ts">
definePageMeta({ middleware: [] })
</script>

<template>
  <BasePageShell>
    <MainPageHeader />
    <MainArticleControls />
    <MainTagFilter />
    <MainArticleGrid />
  </BasePageShell>
</template>
