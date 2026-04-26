<script setup lang="ts">
defineProps<{
  totalUsers: number
  adminCount: number
  userCount: number
  search: string
  isLoading: boolean
}>()

const emit = defineEmits<{
  'update:search': [value: string]
  refresh: []
}>()
</script>

<template>
  <header class="management-header">
    <div class="header-left">
      <div>
        <p class="eyebrow">Admin Control</p>
        <h1 class="card-title">User Management</h1>
        <p class="management-description">Kelola role dan akses user RetoGen.</p>
      </div>

      <!-- Statistik dalam bentuk Metadata (tetap minimalis) -->
      <div class="header-meta">
        <span class="meta-item">
          <strong>{{ totalUsers }}</strong> Total User
        </span>
        <span class="meta-dot">•</span>
        <span class="meta-item">
          <strong>{{ adminCount }}</strong> Admin
        </span>
        <span class="meta-dot">•</span>
        <span class="meta-item">
          <strong>{{ userCount }}</strong> User
        </span>
      </div>
    </div>

    <!-- Toolbar dikembalikan ke kanan dengan tata letak semula -->
    <div class="header-right">
      <div class="toolbar">
        <div class="search-wrapper">
          <BaseInput
            :model-value="search"
            placeholder="Cari nama, email..."
            label="Cari user"
            @update:model-value="emit('update:search', $event)"
          />
        </div>
        <BaseButton variant="ghost" :disabled="isLoading" @click="emit('refresh')">
          Refresh
        </BaseButton>
      </div>
    </div>
  </header>
</template>

<style scoped>
.management-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; /* Aligment kembali seperti semula */
  gap: 24px;
  margin-bottom: 32px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Style Metadata yang lebih bersih */
.header-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 13.5px;
}

.meta-item strong {
  color: var(--text-primary);
  font-weight: 700;
}

.meta-dot {
  color: var(--glass-border);
  font-size: 18px;
}

/* Toolbar dikembalikan ke grid horizontal agar tidak bertumpuk */
.toolbar {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.search-wrapper {
  width: 260px;
}

@media (max-width: 860px) {
  .management-header {
    flex-direction: column;
  }
  
  .header-right, .search-wrapper {
    width: 100%;
  }
}
</style>
