<script setup lang="ts">
definePageMeta({ layout: 'default' })

const route = useRoute()

const articleId = computed(() => {
  return String(route.query.id || '')
})
</script>

<template>
  <BasePageShell>
    <BaseGlassCard class="article-form-card">
      <DetailArticleForm mode="edit" :article-id="articleId" />
    </BaseGlassCard>
  </BasePageShell>
</template>

<style scoped>
.article-form-card {
  width: min(100%, 1120px);
  margin: 0 auto;
}
</style>