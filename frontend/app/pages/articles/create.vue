<script setup lang="ts">
definePageMeta({ layout: 'default' })
</script>

<template>
  <BasePageShell>
    <BaseGlassCard class="article-form-card">
      <DetailArticleForm mode="create" />
    </BaseGlassCard>
  </BasePageShell>
</template>

<style scoped>
.article-form-card {
  width: min(100%, 1120px);
  margin: 0 auto;
}
</style>