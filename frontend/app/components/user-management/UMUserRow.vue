<script setup lang="ts">
import type { ManagedUser } from '~/composables/useUserManagement'

defineProps<{
  user: ManagedUser
  actionLoadingId: string | null
  formatDate: (value: string) => string
}>()

const emit = defineEmits<{
  makeAdmin: [user: ManagedUser]
  openBanConfirm: [user: ManagedUser]
}>()
</script>

<template>
  <article class="user-row">
    <div class="user-main">
      <div class="avatar">
        {{ user.username.slice(0, 1).toUpperCase() }}
      </div>

      <div>
        <div class="user-name-line">
          <h2>{{ user.username }}</h2>
          <span class="role-pill" :class="{ 'role-pill--admin': user.role === 'admin' }">
            {{ user.role }}
          </span>
        </div>
        <p>{{ user.fullname }}</p>
        <span>{{ user.email }}</span>
      </div>
    </div>

    <div class="user-meta">
      <span>{{ user.report_count }} report</span>
      <span>Bergabung {{ formatDate(user.created_at) }}</span>
    </div>

    <div class="row-actions">
      <BaseButton
        variant="ghost"
        :disabled="user.role === 'admin' || actionLoadingId === user.user_id"
        @click="emit('makeAdmin', user)"
      >
        {{ user.role === 'admin' ? 'Sudah Admin' : 'Jadikan Admin' }}
      </BaseButton>

      <BaseButton
        variant="destructive"
        :disabled="user.role === 'admin' || actionLoadingId === user.user_id"
        @click="emit('openBanConfirm', user)"
      >
        Ban
      </BaseButton>
    </div>
  </article>
</template>

<style scoped>
.user-row {
  display: grid;
  grid-template-columns: minmax(0, 1.3fr) minmax(140px, 0.6fr) auto;
  gap: 16px;
  align-items: center;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 14px;
  background: rgba(255, 255, 255, 0.12);
}

.user-main {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  display: grid;
  place-items: center;
  background: rgba(106, 173, 168, 0.14);
  color: var(--primary-cyan);
  font-weight: 800;
  flex-shrink: 0;
}

.user-name-line {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.user-name-line h2 {
  font-size: 15px;
  line-height: 1.2;
  margin: 0;
}

.user-main p,
.user-main span,
.user-meta span {
  color: var(--text-secondary);
  font-size: 13px;
}

.user-main span {
  display: block;
  word-break: break-word;
}

.role-pill {
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: capitalize;
}

.role-pill--admin {
  color: var(--primary-cyan);
  border-color: rgba(106, 173, 168, 0.35);
  background: rgba(106, 173, 168, 0.08);
}

.user-meta {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.row-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

@media (max-width: 860px) {
  .user-row {
    grid-template-columns: 1fr;
  }

  .row-actions {
    justify-content: stretch;
  }

  .row-actions :deep(.base-button) {
    flex: 1;
  }
}

@media (max-width: 520px) {
  .row-actions {
    flex-direction: column;
    width: 100%;
  }

  .row-actions :deep(.base-button) {
    width: 100%;
  }
}
</style>