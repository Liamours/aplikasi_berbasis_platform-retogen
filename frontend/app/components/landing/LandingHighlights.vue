<script setup lang="ts">
const highlights = [
  { title: 'Review terpercaya', description: 'Baca ulasan produk dengan lebih jelas dan lebih terarah.' },
  { title: 'Insight komunitas', description: 'Lihat rating dan komentar untuk menambah perspektif.' },
  { title: 'Pantau harga', description: 'Bandingkan harga produk tanpa pengalaman yang rumit.' },
]
</script>

<template>
  <section class="highlights">
    <div class="highlights__grid">
      <BaseGlassCard
        v-for="item in highlights"
        :key="item.title"
        variant="ghost"
        class="highlights__card"
      >
        <h3 class="highlights__title">{{ item.title }}</h3>
        <p class="highlights__description">{{ item.description }}</p>
      </BaseGlassCard>
    </div>
  </section>
</template>

<style scoped>
.highlights {
  padding: 12px 0;
}

.highlights__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.highlights__card {
  height: 100%;
}

.highlights__title {
  margin: 0 0 10px;
  font-size: 22px;
  line-height: 1.2;
  font-weight: 700;
  color: var(--text-primary);
}

.highlights__description {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.6;
}

@media (max-width: 1024px) {
  .highlights__grid {
    grid-template-columns: 1fr;
  }
}
</style>
