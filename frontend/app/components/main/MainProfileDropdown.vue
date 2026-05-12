<script setup lang="ts">
const authStore = useAuthStore()
const { logout } = useAuth()

// Real user from store — falls back to safe defaults if somehow null
const user    = computed(() => authStore.user)
const initial = computed(() => user.value?.username?.[0]?.toUpperCase() ?? '?')

const isOpen  = ref(false)
const rootRef = ref<HTMLElement | null>(null)

const toggle = () => { isOpen.value = !isOpen.value }
const close  = () => { isOpen.value = false }

function onOutsideClick(e: MouseEvent) {
  if (rootRef.value && !rootRef.value.contains(e.target as Node)) close()
}

async function handleLogout() {
  close()
  await logout()
}

onMounted(()  => document.addEventListener('mousedown', onOutsideClick))
onUnmounted(() => document.removeEventListener('mousedown', onOutsideClick))
</script>

<template>
  <div ref="rootRef" class="profile-menu">

    <!-- Avatar trigger -->
    <button
      class="profile-avatar"
      :class="{ 'profile-avatar--open': isOpen }"
      :aria-expanded="isOpen"
      aria-haspopup="menu"
      aria-label="Menu profil pengguna"
      @click="toggle"
    >
      <span class="profile-avatar__initial">{{ initial }}</span>
    </button>

    <!-- Dropdown — solid panel via BaseDropdownPanel -->
    <Transition name="glass-fade">
      <BaseDropdownPanel v-if="isOpen" role="menu">

        <!-- User info header -->
        <div class="profile-panel__head">
          <div class="profile-panel__avatar-sm" aria-hidden="true">{{ initial }}</div>
          <div class="profile-panel__user-text">
            <span class="profile-panel__name">{{ user?.fullname ?? user?.username ?? '—' }}</span>
            <span class="profile-panel__email">{{ user?.email ?? '' }}</span>
          </div>
        </div>

        <hr class="profile-panel__divider">

        <BaseDropdownItem to="/profile" @click="close">Profil Saya</BaseDropdownItem>
        <BaseDropdownItem :danger="true" @click="handleLogout">Keluar</BaseDropdownItem>

      </BaseDropdownPanel>
    </Transition>

  </div>
</template>

<style scoped>
.profile-menu { position: relative; }

/* Avatar — gradient bg, matches BaseButton--icon sizing */
.profile-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 999px;
  border: 1px solid var(--glass-border);
  background: linear-gradient(135deg, rgba(181,107,82,0.14), rgba(106,173,168,0.14));
  cursor: pointer;
  transition: var(--transition-fast);
}

.profile-avatar:hover,
.profile-avatar--open {
  border-color: var(--primary-cyan);
  box-shadow: 0 0 0 2px rgba(106, 173, 168, 0.18);
  transform: scale(1.05);
}

.profile-avatar__initial {
  font-size: 15px;
  font-weight: 700;
  color: var(--primary-cyan);
  line-height: 1;
  user-select: none;
}

/* Panel content — layout only, surface owned by BaseDropdownPanel */
.profile-panel__head {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 10px 12px;
}

.profile-panel__avatar-sm {
  flex-shrink: 0;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(181,107,82,0.14), rgba(106,173,168,0.14));
  border: 1px solid var(--glass-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: var(--primary-cyan);
}

.profile-panel__user-text {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}

.profile-panel__name {
  font-size: 13px;
  font-weight: 700;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.profile-panel__email {
  font-size: 11px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.profile-panel__divider {
  border: none;
  border-top: 1px solid var(--glass-border);
  margin: 0 2px 6px;
}
</style>
