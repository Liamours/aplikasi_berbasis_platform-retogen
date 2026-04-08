<script setup lang="ts">
const { resetFilters } = useArticleFilter()
</script>

<template>
  <div class="empty-state">
    <BaseGlassCard class="empty-state__card">
      <p class="empty-state__icon" aria-hidden="true">🔍</p>
      <h3 class="empty-state__title">Artikel tidak ditemukan</h3>
      <p class="empty-state__sub">Coba ubah kata kunci pencarian atau pilih tag lain.</p>
      <BaseButton variant="primary" class="empty-state__btn" @click="resetFilters">
        Reset Filter
      </BaseButton>
    </BaseGlassCard>
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.empty-state__card {
  max-width: 400px;
  width: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.empty-state__icon  { font-size: 40px; margin-bottom: 4px; }
.empty-state__title { font-size: 20px; font-weight: 700; color: var(--text-primary); }
.empty-state__sub   { font-size: 14px; color: var(--text-secondary); line-height: 1.6; }
.empty-state__btn   { margin-top: 8px; }
</style>
