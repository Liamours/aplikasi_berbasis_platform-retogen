<script setup lang="ts">
const { isDark, toggleTheme } = useTheme()
const authStore = useAuthStore()
const { logout } = useAuth()
</script>

<template>
  <header class="navbar">
    <div class="navbar__inner">
      <NuxtLink to="/" class="navbar__brand">
        <img src="/logo.jpg" alt="RetoGen logo" class="navbar__logo">
        <span class="navbar__brand-text">RetoGen</span>
      </NuxtLink>

      <div class="navbar__actions">
        <BaseButton variant="icon" aria-label="Toggle theme" @click="toggleTheme">
          <span>{{ isDark ? '☀' : '☾' }}</span>
        </BaseButton>

        <template v-if="authStore.isAuthenticated">
          <BaseButton variant="ghost" @click="logout">
            Logout
          </BaseButton>
        </template>

        <template v-else>
          <NuxtLink to="/login" class="navbar__link">
            <BaseButton variant="ghost">
              Login
            </BaseButton>
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

.navbar__link {
  display: inline-flex;
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