<script setup lang="ts">
import type { DetailPriceEntry } from '~/types/api'

defineProps<{
  prices: DetailPriceEntry[]
  tracked: boolean
}>()

defineEmits<{
  toggleTrack: []
}>()

const formatPrice = (value: number) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0
  }).format(value)
}

const trendLabelMap: Record<DetailPriceEntry['trend'], string> = {
  down: 'Turun',
  up: 'Naik',
  stable: 'Stabil'
}
</script>

<template>
  <section class="price-tracker">
    <div class="price-tracker__head">
      <div>
        <p class="price-tracker__eyebrow">Price tracking</p>
        <h2 class="price-tracker__title">Pantau harga</h2>
      </div>

      <button type="button" class="price-tracker__follow" :class="{ 'is-active': tracked }" @click="$emit('toggleTrack')">
        {{ tracked ? 'Tracked' : 'Track price' }}
      </button>
    </div>

    <div class="price-tracker__list">
      <article v-for="item in prices" :key="item.id" class="price-tracker__item">
        <div class="price-tracker__store-row">
          <strong class="price-tracker__store">{{ item.store }}</strong>
          <span class="price-tracker__trend" :class="`is-${item.trend}`">
            {{ trendLabelMap[item.trend] }}
          </span>
        </div>

        <div class="price-tracker__price">
          {{ formatPrice(item.price) }}
        </div>

        <div class="price-tracker__meta">
          <span>{{ item.updatedAt }}</span>
        </div>
      </article>
    </div>
  </section>
</template>

<style scoped>
.price-tracker {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.price-tracker__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.price-tracker__eyebrow {
  font-size: 12px;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.price-tracker__title {
  font-size: 20px;
  line-height: 1.1;
  font-weight: 700;
  color: var(--text-primary);
}

.price-tracker__follow {
  border: 1px solid rgba(106, 173, 168, 0.24);
  background: rgba(106, 173, 168, 0.08);
  color: var(--primary-cyan);
  border-radius: 999px;
  padding: 10px 14px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: var(--transition-fast);
  white-space: nowrap;
}

.price-tracker__follow:hover,
.price-tracker__follow.is-active {
  background: rgba(106, 173, 168, 0.16);
}

.price-tracker__list {
  display: grid;
  gap: 12px;
}

.price-tracker__item {
  padding: 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid var(--glass-border);
}

.price-tracker__store-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.price-tracker__store {
  font-size: 14px;
  color: var(--text-primary);
}

.price-tracker__trend {
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 11px;
  font-weight: 700;
}

.price-tracker__trend.is-down {
  background: rgba(106, 173, 168, 0.14);
  color: var(--primary-cyan);
}

.price-tracker__trend.is-up {
  background: rgba(181, 107, 82, 0.12);
  color: var(--primary-red);
}

.price-tracker__trend.is-stable {
  background: rgba(99, 99, 96, 0.12);
  color: var(--text-secondary);
}

.price-tracker__price {
  font-size: 22px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.price-tracker__meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 14px;
  font-size: 12px;
  color: var(--text-secondary);
}

@media (max-width: 480px) {
  .price-tracker__head {
    flex-direction: column;
    align-items: stretch;
  }

  .price-tracker__follow {
    width: 100%;
  }
}
</style>