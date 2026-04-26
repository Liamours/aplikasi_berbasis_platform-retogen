<script setup lang="ts">
interface ManagedUser {
  user_id: string
  username: string
  email: string
  fullname: string
  role: 'user' | 'admin' | string
  report_count: number
  created_at: string
}

interface GetUsersResponse {
  confirmation: string
  users?: ManagedUser[]
}

interface ActionResponse {
  confirmation: string
}

definePageMeta({
  layout: 'default',
//   middleware: 'auth'
})

const api = useApi()
const authStore = useAuthStore()

// const users = ref<ManagedUser[]>([])
const users = ref<ManagedUser[]>([
  {
    user_id: '1',
    username: 'rafiqlabib',
    email: 'rafiq@mail.com',
    fullname: 'Rafiq Labib',
    role: 'admin',
    report_count: 0,
    created_at: '2025-12-12'
  },
  {
    user_id: '2',
    username: 'dzakydev',
    email: 'dzaky@mail.com',
    fullname: 'Dzaky Pratama',
    role: 'user',
    report_count: 3,
    created_at: '2026-01-08'
  },
  {
    user_id: '3',
    username: 'rifqitech',
    email: 'rifqi@mail.com',
    fullname: 'Rifqi Akbar',
    role: 'user',
    report_count: 7,
    created_at: '2026-02-18'
  }
])
const search = ref('')
const isLoading = ref(false)
const actionLoadingId = ref<string | null>(null)
const selectedBanUser = ref<ManagedUser | null>(null)
const showSuccessPopup = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const filteredUsers = computed(() => {
  const keyword = search.value.trim().toLowerCase()

  if (!keyword) return users.value

  return users.value.filter((user) => {
    return [
      user.username,
      user.fullname,
      user.email,
      user.role
    ].some((value) => value?.toLowerCase().includes(keyword))
  })
})

const adminCount = computed(() => {
  return users.value.filter((user) => user.role === 'admin').length
})

const userCount = computed(() => {
  return users.value.filter((user) => user.role !== 'admin').length
})

const clearFeedback = () => {
  showSuccessPopup.value = false
  successMessage.value = ''
  errorMessage.value = ''
}

const closeSuccessPopup = () => {
  showSuccessPopup.value = false
  successMessage.value = ''
}

const fetchUsers = async () => {
  clearFeedback()
  isLoading.value = true

  try {
    const response = await api.post<GetUsersResponse>('/user/get_all', {}, true)

    if (response.confirmation !== 'successful') {
      errorMessage.value = response.confirmation || 'Gagal memuat data user.'
      users.value = []
      return
    }

    users.value = response.users ?? []
  } catch {
    errorMessage.value = 'Gagal terhubung ke server.'
    users.value = []
  } finally {
    isLoading.value = false
  }
}

const makeAdmin = async (user: ManagedUser) => {
  if (user.role === 'admin') return

  clearFeedback()
  actionLoadingId.value = user.user_id

  try {
    // --- MOCK UI ---
    // const response = await api.post<ActionResponse>(
    //   '/user/make_admin',
    //   { user_id: user.user_id },
    //   true
    // )

    // if (response.confirmation === 'successful: role updated to admin') { ...

    // Simulasi proses delay
    await new Promise(resolve => setTimeout(resolve, 800))

    // Update data lokal
    const index = users.value.findIndex(u => u.user_id === user.user_id)
    if (index !== -1) {
      users.value[index].role = 'admin'
    }

    successMessage.value = `${user.username} berhasil diubah menjadi admin.`
    showSuccessPopup.value = true
    // await fetchUsers()
    // -----------------
  } catch {
    errorMessage.value = 'Gagal mengubah role user.'
  } finally {
    actionLoadingId.value = null
  }
}

const openBanConfirm = (user: ManagedUser) => {
  clearFeedback()
  selectedBanUser.value = user
}

const closeBanConfirm = () => {
  selectedBanUser.value = null
}

const banUser = async () => {
  if (!selectedBanUser.value) return

  clearFeedback()
  actionLoadingId.value = selectedBanUser.value.user_id

  try {
    // --- MOCK UI ---
    // const response = await api.post<ActionResponse>(
    //   '/user/delete',
    //   { user_id: selectedBanUser.value.user_id },
    //   true
    // )

    // if (response.confirmation === 'successful: user deleted') { ...
    
    // Simulasi proses delay
    await new Promise(resolve => setTimeout(resolve, 800))

    // Update data lokal
    users.value = users.value.filter(u => u.user_id !== selectedBanUser.value!.user_id)
    
    successMessage.value = `${selectedBanUser.value.username} berhasil diban.`
    showSuccessPopup.value = true
    selectedBanUser.value = null
    // await fetchUsers()
    // -----------------
  } catch {
    errorMessage.value = 'Gagal memproses ban user.'
  } finally {
    actionLoadingId.value = null
  }
}

const formatDate = (value: string) => {
  if (!value) return '-'

  return new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  }).format(new Date(value))
}

// onMounted(fetchUsers)
</script>

<template>
  <BasePageShell>
    <div class="user-management-page">
      <BaseGlassCard class="user-management-card">
        <header class="management-header">
          <div class="header-left">
            <div>
              <p class="eyebrow">Admin Control</p>
              <h1 class="card-title">User Management</h1>
              <p class="management-description">
                Kelola role dan akses user RetoGen.
              </p>
            </div>

            <div class="summary-grid">
              <div class="summary-item">
                <span>{{ users.length }}</span>
                <p>Total</p>
              </div>
              <div class="summary-item">
                <span>{{ adminCount }}</span>
                <p>Admin</p>
              </div>
              <div class="summary-item">
                <span>{{ userCount }}</span>
                <p>User</p>
              </div>
            </div>
          </div>

          <div class="header-right">
            <div class="toolbar">
              <BaseInput
                v-model="search"
                placeholder="Cari nama, email, atau role"
                label="Cari user"
              />

              <BaseButton
                variant="ghost"
                :disabled="isLoading"
                @click="fetchUsers"
              >
                Refresh
              </BaseButton>
            </div>
          </div>
        </header>

        <!-- <div v-if="!authStore.isAdmin" class="error-banner">
          Akun ini tidak memiliki akses admin.
        </div>

        <template v-else> -->
        <div>



          <Transition name="glass-fade">
            <p v-if="errorMessage" class="error-banner">
              {{ errorMessage }}
            </p>
          </Transition>

          <div v-if="selectedBanUser" class="confirm-panel">
            <div>
              <strong>Ban {{ selectedBanUser.username }}?</strong>
              <p>
                Akun akan dihapus dari sistem. Admin tidak dapat diban.
              </p>
            </div>

            <div class="confirm-actions">
              <BaseButton
                variant="ghost"
                :disabled="actionLoadingId === selectedBanUser.user_id"
                @click="closeBanConfirm"
              >
                Batal
              </BaseButton>

              <BaseButton
                variant="destructive"
                :disabled="actionLoadingId === selectedBanUser.user_id"
                @click="banUser"
              >
                {{ actionLoadingId === selectedBanUser.user_id ? 'Memproses...' : 'Ban User' }}
              </BaseButton>
            </div>
          </div>

          <div class="user-list" aria-live="polite">
            <div v-if="isLoading" class="empty-state">
              Memuat data user...
            </div>

            <div v-else-if="filteredUsers.length === 0" class="empty-state">
              Tidak ada user yang cocok.
            </div>

            <article
              v-for="user in filteredUsers"
              v-else
              :key="user.user_id"
              class="user-row"
            >
              <div class="user-main">
                <div class="avatar">
                  {{ user.username.slice(0, 1).toUpperCase() }}
                </div>

                <div>
                  <div class="user-name-line">
                    <h2>{{ user.username }}</h2>
                    <span
                      class="role-pill"
                      :class="{ 'role-pill--admin': user.role === 'admin' }"
                    >
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
                  @click="makeAdmin(user)"
                >
                  {{ user.role === 'admin' ? 'Sudah Admin' : 'Jadikan Admin' }}
                </BaseButton>

                <BaseButton
                  variant="destructive"
                  :disabled="user.role === 'admin' || actionLoadingId === user.user_id"
                  @click="openBanConfirm(user)"
                >
                  Ban
                </BaseButton>
              </div>
            </article>
          </div>
        </div>
      </BaseGlassCard>
    </div>
  </BasePageShell>

  <Teleport to="body">
    <Transition name="glass-fade">
      <div v-if="showSuccessPopup" class="popup-overlay" @click.self="closeSuccessPopup">
        <div class="popup-content">
          <div class="popup-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-check-circle"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
          </div>
          <h3>Berhasil!</h3>
          <p>{{ successMessage }}</p>
          <BaseButton @click="closeSuccessPopup">Tutup</BaseButton>
        </div>
      </div>
    </Transition>
  </Teleport>
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

.management-header {
  display: flex;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 28px;
}

.header-left {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.header-right {
  display: flex;
  align-items: flex-end;
}

.eyebrow {
  color: var(--primary-cyan);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.management-description {
  color: var(--text-secondary);
  margin-top: 8px;
  max-width: 420px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(72px, 1fr));
  gap: 10px;
}

.summary-item {
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  padding: 12px;
  min-width: 78px;
  background: rgba(255, 255, 255, 0.16);
}

.summary-item span {
  display: block;
  font-size: 20px;
  font-weight: 800;
  line-height: 1.1;
}

.summary-item p {
  color: var(--text-muted);
  font-size: 12px;
  margin-top: 4px;
}

.toolbar {
  display: grid;
  grid-template-columns: 240px auto;
  gap: 14px;
  align-items: end;
}

.popup-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.popup-content {
  background: rgba(20, 20, 20, 0.95);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 32px;
  width: min(90%, 400px);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.popup-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(106, 173, 168, 0.15);
  color: var(--primary-cyan);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-icon svg {
  width: 32px;
  height: 32px;
}

.popup-content h3 {
  font-size: 24px;
  margin: 0;
  color: white;
}

.popup-content p {
  color: var(--text-secondary);
  font-size: 15px;
  margin-bottom: 8px;
}

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

.user-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

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

.empty-state {
  border: 1px dashed var(--glass-border);
  border-radius: var(--radius-lg);
  padding: 28px;
  text-align: center;
  color: var(--text-secondary);
}

@media (max-width: 860px) {
  .management-header,
  .confirm-panel {
    flex-direction: column;
  }

  .header-left,
  .header-right {
    width: 100%;
  }

  .summary-grid {
    width: 100%;
  }

  .toolbar {
    width: 100%;
    grid-template-columns: 1fr auto;
  }

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
  .user-management-card {
    padding: 24px;
  }

  .summary-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .confirm-actions,
  .row-actions {
    flex-direction: column;
    width: 100%;
  }

  .confirm-actions :deep(.base-button),
  .row-actions :deep(.base-button) {
    width: 100%;
  }
}
</style>