<script setup lang="ts">
import type { SortOption } from '~/types/api'

const { searchQuery, activeSort } = useArticleFilter()

const sortOptions: { value: SortOption; label: string }[] = [
  { value: 'newest',         label: 'Terbaru' },
  { value: 'oldest',         label: 'Terlama' },
  { value: 'highest_rated',  label: 'Rating Tertinggi' },
  { value: 'most_commented', label: 'Paling Dikomentari' },
]
</script>

<template>
  <div class="controls">
    <div class="controls__search-wrap">
      <span class="controls__icon" aria-hidden="true">⌕</span>
      <input
        v-model="searchQuery"
        class="controls__search"
        type="search"
        placeholder="Cari artikel…"
        aria-label="Cari artikel"
      >
    </div>

    <select v-model="activeSort" class="controls__sort" aria-label="Urutan">
      <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.controls {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.controls__search-wrap {
  position: relative;
  flex: 1;
  min-width: 220px;
}

.controls__icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  color: var(--text-muted);
  pointer-events: none;
}

.controls__search {
  width: 100%;
  padding: 13px 14px 13px 42px;
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
  font-family: var(--font-base);
  font-size: 15px;
  outline: none;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  appearance: none;
  -webkit-appearance: none;
}

.controls__search::placeholder { color: var(--text-muted); }

.controls__search:focus {
  border-color: var(--primary-cyan);
  box-shadow: 0 0 0 3px rgba(106, 173, 168, 0.12);
}

.controls__sort {
  padding: 13px 40px 13px 14px;
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
  font-family: var(--font-base);
  font-size: 14px;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  appearance: none;
  -webkit-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%239A9895' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 14px center;
  transition: border-color 0.2s ease;
}

.controls__sort:focus { border-color: var(--primary-cyan); }

@media (max-width: 640px) {
  .controls { flex-direction: column; align-items: stretch; }
  .controls__search-wrap { min-width: 0; }
  .controls__sort { width: 100%; }
}
</style>
