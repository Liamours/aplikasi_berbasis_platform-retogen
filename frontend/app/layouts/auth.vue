<template>
  <div class="auth-layout">
    <header class="auth-layout__brand">
      <NuxtLink to="/" class="auth-layout__brand-link" aria-label="Go to homepage">
        <img src="/logo.jpg" alt="RetoGen" class="auth-layout__logo" />
        <span class="auth-layout__brand-text">RetoGen</span>
      </NuxtLink>
    </header>

    <main class="auth-layout__content">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.auth-layout {
  position: relative;
  min-height: 100vh;
  background: var(--bg-page);
  color: var(--text-primary);
}

.auth-layout__brand {
  padding: 24px 24px 0;
}

.auth-layout__brand-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--text-primary);
}

.auth-layout__logo {
  width: 34px;
  height: 34px;
  object-fit: contain;
  border-radius: 8px;
}

.auth-layout__brand-text {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.auth-layout__content {
  min-height: calc(100vh - 58px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

@media (max-width: 480px) {
  .auth-layout__brand {
    padding: 20px 20px 0;
  }

  .auth-layout__content {
    padding: 20px;
  }
}
</style>
