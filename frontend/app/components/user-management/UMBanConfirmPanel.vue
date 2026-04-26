<script setup lang="ts">
import type { ManagedUser } from '~/composables/useUserManagement'

defineProps<{
  user: ManagedUser
  actionLoadingId: string | null
}>()

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()
</script>

<template>
  <div class="confirm-panel">
    <div>
      <strong>Ban {{ user.username }}?</strong>
      <p>Akun akan dihapus dari sistem. Admin tidak dapat diban.</p>
    </div>

    <div class="confirm-actions">
      <BaseButton
        variant="ghost"
        :disabled="actionLoadingId === user.user_id"
        @click="emit('cancel')"
      >
        Batal
      </BaseButton>

      <BaseButton
        variant="destructive"
        :disabled="actionLoadingId === user.user_id"
        @click="emit('confirm')"
      >
        {{ actionLoadingId === user.user_id ? 'Memproses...' : 'Ban User' }}
      </BaseButton>
    </div>
  </div>
</template>

<style scoped>
.confirm-panel {
  border: 1px solid rgba(181, 107, 82, 0.28);
  background: rgba(181, 107, 82, 0.09);
  border-radius: var(--radius-lg);
  padding: 16px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
  margin-bottom: 16px;
}

.confirm-panel strong {
  display: block;
  font-size: 15px;
  margin-bottom: 4px;
}

.confirm-panel p {
  color: var(--text-secondary);
  font-size: 14px;
}

.confirm-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

@media (max-width: 860px) {
  .confirm-panel {
    flex-direction: column;
  }
}

@media (max-width: 520px) {
  .confirm-actions {
    flex-direction: column;
    width: 100%;
  }

  .confirm-actions :deep(.base-button) {
    width: 100%;
  }
}
</style>