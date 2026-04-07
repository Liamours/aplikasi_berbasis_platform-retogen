<template>
  <div class="auth-layout">
    <div class="auth-layout__grid" aria-hidden="true" />
    <div class="auth-layout__blob auth-layout__blob--cyan" aria-hidden="true" />
    <div class="auth-layout__blob auth-layout__blob--red" aria-hidden="true" />

    <header class="auth-layout__brand">
      <NuxtLink to="/" class="auth-layout__brand-link" aria-label="Go to homepage">
        <img src="/logo.png" alt="RetoGen" class="auth-layout__logo" />
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
  overflow: hidden;
  background:
    radial-gradient(circle at top, rgba(255, 255, 255, 0.35), transparent 38%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.08), transparent 40%),
    var(--bg-color, #e8e8e8);
  color: var(--text-primary);
}

.auth-layout__grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 206, 209, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 206, 209, 0.04) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none;
}

.auth-layout__blob {
  position: absolute;
  border-radius: 999px;
  filter: blur(140px);
  opacity: 0.28;
  pointer-events: none;
  animation: authFloat 22s alternate infinite ease-in-out;
}

.auth-layout__blob--cyan {
  top: -8%;
  left: -6%;
  width: 360px;
  height: 360px;
  background: rgba(0, 206, 209, 0.22);
}

.auth-layout__blob--red {
  right: -10%;
  bottom: -8%;
  width: 340px;
  height: 340px;
  background: rgba(227, 66, 52, 0.18);
}

.auth-layout__brand {
  position: relative;
  z-index: 2;
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
  border-radius: 10px;
}

.auth-layout__brand-text {
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.auth-layout__content {
  position: relative;
  z-index: 2;
  min-height: calc(100vh - 58px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

:global(.dark-mode) .auth-layout {
  background:
    radial-gradient(circle at top, rgba(255, 255, 255, 0.05), transparent 38%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.02), transparent 40%),
    #0d0d0d;
}

:global(.dark-mode) .auth-layout__grid {
  background-image:
    linear-gradient(rgba(93, 215, 218, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(93, 215, 218, 0.05) 1px, transparent 1px);
}

:global(.dark-mode) .auth-layout__blob--cyan {
  background: rgba(93, 215, 218, 0.18);
  opacity: 0.24;
}

:global(.dark-mode) .auth-layout__blob--red {
  background: rgba(255, 107, 94, 0.14);
  opacity: 0.22;
}

@keyframes authFloat {
  from {
    transform: translate(0, 0) scale(1);
  }
  to {
    transform: translate(120px, 80px) scale(1.1);
  }
}

@media (max-width: 480px) {
  .auth-layout__brand {
    padding: 20px 20px 0;
  }

  .auth-layout__content {
    padding: 20px;
  }

  .auth-layout__blob--cyan,
  .auth-layout__blob--red {
    width: 260px;
    height: 260px;
  }
}
</style>