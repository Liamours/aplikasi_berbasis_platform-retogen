<script setup lang="ts">
defineProps<{
  totalUsers: number
  adminCount: number
  userCount: number
  reportedCount: number
  totalReports: number
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
    <div class="header-main">
      <div class="header-left">
        <div class="header-info">
          <div class="breadcrumbs">
            <NuxtLink to="/main" class="breadcrumb-link">home</NuxtLink>
            <span class="breadcrumb-separator">/</span>
            <span class="breadcrumb-current">admin-menu</span>
          </div>
          <h1 class="card-title">User Management</h1>
          <p class="management-description">Kelola role dan akses user RetoGen.</p>
        </div>

        <!-- Statistik dalam bentuk Metadata -->
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
          <span class="meta-dot">•</span>
          <span class="meta-item">
            <strong :class="{ 'text-danger': reportedCount > 0 }">{{ reportedCount }}</strong> Total Report
          </span>
        </div>
      </div>

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
    </div>
  </header>
</template>

<style scoped>
.management-header {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 32px;
}

.header-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 4px;
}

.breadcrumb-link {
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 0.2s ease;
}

.breadcrumb-link:hover {
  color: var(--primary-cyan);
}

.breadcrumb-separator {
  color: var(--glass-border);
}

.breadcrumb-current {
  color: var(--primary-cyan);
  text-transform: lowercase;
}

.header-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
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

.text-danger {
  color: var(--primary-red) !important;
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
  .header-main {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-right, .search-wrapper {
    width: 100%;
  }
}
</style>
