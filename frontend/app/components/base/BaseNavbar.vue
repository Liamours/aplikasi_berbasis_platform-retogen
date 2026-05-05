<script setup lang="ts">
const { isDark, toggleTheme } = useTheme()
const route = useRoute()
const { logout } = useAuth()

// Profile + add-article only on the main article listing page
const isMainPage = computed(() => route.path === '/main')
const isSimpleNavbarPage = computed(() => ['/profile', '/user-management'].includes(route.path))

const authButton = computed(() => {
  if (route.path === '/login') {
    return { text: 'Register', link: '/register' }
  }
  return { text: 'Login', link: '/login' }
})

const refreshPage = () => {
  if (import.meta.client) {
    window.location.reload()
  }
}
</script>

<template>
  <header class="navbar">
    <div class="navbar__inner">
      <div class="navbar__brand" @click="refreshPage" style="cursor: pointer;">
        <img src="/logo.jpg" alt="RetoGen logo" class="navbar__logo">
        <span class="navbar__brand-text">RetoGen</span>
      </div>

      <div class="navbar__actions">
        <!-- Main page: admin add-article + profile -->
        <template v-if="isMainPage">
          <MainAdminMenu/>
        </template>
        <!-- Theme toggle — always visible -->
        <BaseButton variant="icon" aria-label="Toggle theme" @click="toggleTheme">
          <span>{{ isDark ? '☀' : '☾' }}</span>
        </BaseButton>

        <!-- Main page: admin add-article + profile -->
        <template v-if="isMainPage">
          <MainProfileDropdown />
        </template>

        <!-- Simple navbar pages (Profile, User Management): Only show theme toggle -->
        <template v-else-if="isSimpleNavbarPage">
          <!-- no extra actions -->
        </template>

        <!-- Auth pages: toggle between login/register -->
        <template v-else>
          <NuxtLink :to="authButton.link">
            <BaseButton variant="ghost">{{ authButton.text }}</BaseButton>
          </NuxtLink>
        </template>
      </div>
    </div>
  </header>
</template>

<style scoped>
.navbar {
  position: fixed;
  inset: 0 0 auto 0;
  height: 64px;
  z-index: 1000;
  background: var(--glass-bg);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--glass-border);
}

.navbar__inner {
  width: min(100%, 1200px);
  height: 100%;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.navbar__brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.navbar__logo {
  width: 38px;
  height: 38px;
  object-fit: cover;
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  flex-shrink: 0;
}

.navbar__brand-text {
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 2px;
  color: var(--text-primary);
}

.navbar__actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

@media (max-width: 480px) {
  .navbar__inner {
    padding: 0 20px;
  }

  .navbar__brand-text {
    font-size: 14px;
  }
}
</style>