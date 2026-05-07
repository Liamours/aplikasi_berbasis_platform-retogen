<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

const route = useRoute()

const articleId = computed(() => {
  return String(route.query.id || '')
})

const isValidArticleId = computed(() => {
  return /^[a-fA-F0-9]{24}$/.test(articleId.value)
})

watch(
  articleId,
  async (id) => {
    if (!id || !/^[a-fA-F0-9]{24}$/.test(id)) {
      await navigateTo('/main')
    }
  },
  { immediate: true }
)
</script>

<template>
  <BasePageShell>
    <BaseGlassCard class="article-form-card">
      <DetailArticleForm
        v-if="isValidArticleId"
        mode="edit"
        :article-id="articleId"
      />

      <p v-else class="article-form-feedback">
        Mengalihkan ke halaman utama...
      </p>
    </BaseGlassCard>
  </BasePageShell>
</template>

<style scoped>
.article-form-card {
  width: min(100%, 1120px);
  margin: 0 auto;
}

.article-form-feedback {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}
</style>