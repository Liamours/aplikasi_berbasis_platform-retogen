<script setup lang="ts">
const { article, tracked, lowestPrice, toggleTrackPrice } = useArticleDetail()
</script>

<template>
  <aside class="article-detail-side">
    <div class="side-block">
      <DetailPriceTracker
        :prices="article.prices ?? []"
        :tracked="tracked"
        @toggle-track="toggleTrackPrice"
      />
    </div>

    <div class="side-block">
      <h2 class="side-block__title">Status tracking</h2>
      <p class="side-block__description">
        {{ tracked
          ? 'Harga sedang dipantau. Anda bisa lanjutkan integrasi notifikasi di tahap berikutnya.'
          : 'Aktifkan tracking untuk menandai artikel ini ke daftar pantauan harga.' }}
      </p>

      <div class="side-block__status-row">
        <span class="side-block__status-chip" :class="{ 'is-active': tracked }">
          {{ tracked ? 'Tracking aktif' : 'Belum aktif' }}
        </span>
        <span v-if="lowestPrice" class="side-block__status-note">
          Update terakhir: {{ lowestPrice.updatedAt }}
        </span>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.article-detail-side {
  display: grid;
  gap: 18px;
}

.side-block {
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.14);
  padding: 22px;
}

.side-block__title {
  font-size: 20px;
  line-height: 1.1;
  font-weight: 700;
  color: var(--text-primary);
}

.side-block__description {
  margin-top: 10px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.side-block__status-row {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.side-block__status-chip {
  align-self: flex-start;
  padding: 6px 10px;
  border-radius: var(--radius-sm);
  background: rgba(99, 99, 96, 0.12);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 700;
}

.side-block__status-chip.is-active {
  background: rgba(106, 173, 168, 0.14);
  color: var(--primary-cyan);
}

.side-block__status-note {
  font-size: 12px;
  color: var(--text-secondary);
}

@media (max-width: 640px) {
  .side-block { padding: 18px; }
}
</style>
