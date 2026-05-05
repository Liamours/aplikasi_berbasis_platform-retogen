<script setup lang="ts">
import type { DetailPriceEntry } from '~/types/api'

const props = defineProps<{
  prices: DetailPriceEntry[]
  tracked: boolean
}>()

defineEmits<{
  toggleTrack: []
}>()

const logoErrors = ref<Record<string, boolean>>({})

const topRatedPrices = computed(() =>
  [...props.prices]
    .sort((a, b) => {
      const ratingDiff = (b.rating ?? 0) - (a.rating ?? 0)
      if (ratingDiff !== 0) return ratingDiff
      return a.price - b.price
    })
    .slice(0, 3)
)

const bestPrice = computed(() =>
  [...props.prices].sort((a, b) => a.price - b.price)[0]
)

const formatPrice = (value: number) => {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0
  }).format(value)
}

const normalizeStoreName = (store: string) => {
  return store
    .toLowerCase()
    .trim()
    .replace(/\s+/g, '')
    .replace(/[^a-z0-9-]/g, '')
}

const getStoreLabel = (item: DetailPriceEntry) => {
  return item.store || 'Tokopedia'
}

const getStoreInitial = (item: DetailPriceEntry) => {
  const source = item.store || 'T'
  return source.slice(0, 1).toUpperCase()
}

const resolveStoreLogo = (item: DetailPriceEntry) => {
  if (item.logo) return item.logo
  // Always use Tokopedia logo for now as it's the only source
  return '/tokopedia.png'
}

const markLogoAsBroken = (id: string) => {
  logoErrors.value = {
    ...logoErrors.value,
    [id]: true
  }
}

const formatRating = (value: number | null) => {
  if (typeof value !== 'number') return 'Belum ada'
  return value.toFixed(1)
}
</script>

<template>
  <section class="price-tracker">
    <div class="price-tracker__head">
      <div class="price-tracker__heading">
        <p class="price-tracker__eyebrow">Monitor harga</p>
        <h2 class="price-tracker__title">Pantau harga</h2>
        <p class="price-tracker__subtitle">
          Top 3 toko berdasarkan rating
        </p>
      </div>

      <button
        type="button"
        class="price-tracker__follow"
        :class="{ 'is-active': tracked }"
        @click="$emit('toggleTrack')"
      >
        {{ tracked ? 'Dipantau' : 'Pantau' }}
      </button>
    </div>

    <div v-if="bestPrice" class="price-tracker__summary">
      <span>Harga terbaik</span>
      <strong>{{ formatPrice(bestPrice.price) }}</strong>
    </div>

    <p class="price-tracker__track-note">
      {{ tracked
        ? 'Produk ini masuk daftar pantauan.'
        : 'Aktifkan pantauan untuk menandai produk ini.' }}
    </p>

    <div v-if="topRatedPrices.length" class="price-tracker__list">
      <article
        v-for="item in topRatedPrices"
        :key="item.id"
        class="price-tracker__row"
      >
        <div class="price-tracker__logo" aria-hidden="true">
          <img
            v-if="!logoErrors[item.id]"
            :src="resolveStoreLogo(item)"
            :alt="getStoreLabel(item)"
            @error="markLogoAsBroken(item.id)"
          >
          <span v-else>{{ getStoreInitial(item) }}</span>
        </div>

        <div class="price-tracker__content">
          <div class="price-tracker__topline">
            <strong class="price-tracker__store">{{ getStoreLabel(item) }}</strong>

            <span class="price-tracker__rating">
              {{ formatRating(item.rating) }}/5
            </span>
          </div>

          <p class="price-tracker__product">
            {{ item.product }}
          </p>

          <div class="price-tracker__price">
            {{ formatPrice(item.price) }}
          </div>
        </div>
      </article>
    </div>

    <div v-else class="price-tracker__empty">
      Belum ada data harga.
    </div>
  </section>
</template>

<style scoped>
.price-tracker {
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.14);
  padding: 22px;
  display: flex;
  flex-direction: column;
}

.price-tracker__head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.price-tracker__heading {
  min-width: 0;
}

.price-tracker__eyebrow {
  font-size: 12px;
  letter-spacing: 0.6px;
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

.price-tracker__subtitle {
  margin-top: 6px;
  font-size: 13px;
  line-height: 1.5;
  color: var(--text-secondary);
}

.price-tracker__follow {
  border: 1px solid rgba(106, 173, 168, 0.24);
  background: rgba(106, 173, 168, 0.08);
  color: var(--primary-cyan);
  border-radius: 12px;
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
  border-color: rgba(106, 173, 168, 0.36);
}

.price-tracker__summary {
  margin-top: 16px;
  padding: 10px 0 14px;
  border-bottom: 1px solid var(--glass-border);
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.price-tracker__summary span {
  color: var(--text-secondary);
  font-size: 13px;
}

.price-tracker__summary strong {
  color: var(--text-primary);
  font-size: 18px;
  line-height: 1.2;
}

.price-tracker__track-note {
  margin-top: 12px;
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.5;
}

.price-tracker__list {
  margin-top: 6px;
}

.price-tracker__row {
  display: flex;
  gap: 12px;
  padding: 14px 0;
  border-bottom: 1px solid var(--glass-border);
}

.price-tracker__row:last-child {
  padding-bottom: 0;
  border-bottom: none;
}

.price-tracker__logo {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.18);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
  color: var(--text-primary);
  font-weight: 700;
  font-size: 13px;
}

.price-tracker__logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 7px;
}

.price-tracker__content {
  min-width: 0;
  flex: 1;
}

.price-tracker__topline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.price-tracker__store {
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.3;
}

.price-tracker__rating {
  color: var(--primary-cyan);
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
}

.price-tracker__product {
  margin-top: 4px;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.5;
}

.price-tracker__price {
  margin-top: 6px;
  color: var(--text-primary);
  font-size: 17px;
  font-weight: 800;
  line-height: 1.25;
}

.price-tracker__empty {
  margin-top: 16px;
  padding: 12px 0 0;
  border-top: 1px solid var(--glass-border);
  color: var(--text-secondary);
  font-size: 13px;
}

@media (max-width: 640px) {
  .price-tracker {
    padding: 18px;
  }
}

@media (max-width: 480px) {
  .price-tracker__head {
    flex-direction: column;
    align-items: stretch;
  }

  .price-tracker__follow {
    width: 100%;
  }

  .price-tracker__summary {
    align-items: flex-start;
    flex-direction: column;
    gap: 4px;
  }

  .price-tracker__topline {
    align-items: flex-start;
    flex-direction: column;
    gap: 4px;
  }
}
</style>