<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserManagement } from '~/composables/useUserManagement'

// Impor komponen secara manual agar bisa menggunakan nama pendek tanpa edit nuxt.config.ts
import UMHeader from '~/components/user-management/UMHeader.vue'
import UMBanConfirmPanel from '~/components/user-management/UMBanConfirmPanel.vue'
import UMUserRow from '~/components/user-management/UMUserRow.vue'

definePageMeta({
  layout: 'default',
  // middleware: 'auth'
})

const {
  users,
  search,
  isLoading,
  actionLoadingId,
  selectedBanUser,
  showSuccessPopup,
  successMessage,
  errorMessage,
  filteredUsers,
  adminCount,
  userCount,
  fetchUsers,
  makeAdmin,
  openBanConfirm,
  closeBanConfirm,
  banUser,
  closeSuccessPopup,
  formatDate
} = useUserManagement()

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <BasePageShell>
    <div class="user-management-page">
      <BaseGlassCard class="user-management-card">
        <UMHeader
          :total-users="users.length"
          :admin-count="adminCount"
          :user-count="userCount"
          :search="search"
          :is-loading="isLoading"
          @update:search="search = $event"
          @refresh="fetchUsers"
        />

        <Transition name="glass-fade">
          <p v-if="errorMessage" class="error-banner">{{ errorMessage }}</p>
        </Transition>

        <UMBanConfirmPanel
          v-if="selectedBanUser"
          :user="selectedBanUser"
          :action-loading-id="actionLoadingId"
          @confirm="banUser"
          @cancel="closeBanConfirm"
        />

        <div class="user-list" aria-live="polite">
          <div v-if="isLoading" class="empty-state">Memuat data user...</div>

          <div v-else-if="filteredUsers.length === 0" class="empty-state">
            Tidak ada user yang cocok.
          </div>

          <UMUserRow
            v-for="user in filteredUsers"
            v-else
            :key="user.user_id"
            :user="user"
            :action-loading-id="actionLoadingId"
            :format-date="formatDate"
            @make-admin="makeAdmin"
            @open-ban-confirm="openBanConfirm"
          />
        </div>
      </BaseGlassCard>
    </div>
  </BasePageShell>

  <BaseSuccessPopup
    v-if="showSuccessPopup"
    :message="successMessage"
    @close="closeSuccessPopup"
  />
</template>

<style scoped>
.user-management-page {
  min-height: calc(100vh - var(--navbar-height) - 64px);
  display: grid;
  place-items: center;
}

.user-management-card {
  width: min(100%, 920px);
}

.user-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.empty-state {
  border: 1px dashed var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 28px;
  text-align: center;
  color: var(--text-secondary);
}

@media (max-width: 520px) {
  .user-management-card {
    padding: 24px;
  }
}
</style>
