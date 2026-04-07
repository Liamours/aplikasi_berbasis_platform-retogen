<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { isDark, toggleTheme } from '@/composables/useTheme'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  email: '',
  password: '',
})

const isFormValid = computed(() => {
  return form.email.trim() !== '' && form.password.trim() !== ''
})

async function handleSubmit() {
  const result = await authStore.login(form.email, form.password)

  if (result.success) {
    router.push('/home')
  }
}
</script>

<template>
  <main class="login-page">
    <div class="bg-blob bg-blob--cyan"></div>
    <div class="bg-blob bg-blob--red"></div>

    <header class="login-navbar">
      <div class="brand">RetoGen</div>

      <button class="ghost-btn icon-btn" @click="toggleTheme">
        {{ isDark ? '☀' : '☾' }}
      </button>
    </header>

    <section class="login-section">
      <div class="login-card">
        <div class="card-accent"></div>

        <h1 class="title">Welcome Back</h1>
        <p class="subtitle">
          Masuk untuk melanjutkan ke dashboard RetoGen.
        </p>

        <form class="login-form" @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              placeholder="you@example.com"
              autocomplete="email"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              placeholder="••••••••"
              autocomplete="current-password"
            />
          </div>

          <transition name="glass-fade">
            <div v-if="authStore.errorMessage" class="error-banner">
              {{ authStore.errorMessage }}
            </div>
          </transition>

          <button
            class="primary-btn"
            type="submit"
            :disabled="!isFormValid || authStore.loading"
          >
            {{ authStore.loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>
      </div>
    </section>
  </main>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  padding-top: 64px;
}

.login-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 20;
  background: var(--glass-bg);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid var(--glass-border);
}

.brand {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: 2px;
}

.login-section {
  min-height: calc(100vh - 64px);
  display: grid;
  place-items: center;
  padding: 24px;
}

.login-card {
  width: min(100%, 480px);
  padding: 40px;
  border-radius: 24px;
  position: relative;
  overflow: hidden;
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(200%);
  -webkit-backdrop-filter: blur(24px) saturate(200%);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
}

.login-card::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 1px;
  border-radius: 24px;
  background: linear-gradient(135deg, var(--glass-edge), transparent 50%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  pointer-events: none;
}

.card-accent {
  position: absolute;
  inset: 0 auto auto 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-red), var(--primary-cyan));
}

.title {
  margin: 0 0 8px;
  font-size: 36px;
  line-height: 1.15;
  font-weight: 700;
}

.subtitle {
  margin: 0 0 24px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.login-form {
  display: grid;
  gap: 20px;
}

.form-group {
  display: grid;
  gap: 8px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.form-group input {
  width: 100%;
  padding: 14px;
  border-radius: 10px;
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
  outline: none;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.form-group input::placeholder {
  color: var(--text-muted);
}

.form-group input:focus {
  border-color: rgba(0, 188, 212, 0.45);
  box-shadow: 0 0 0 4px rgba(0, 188, 212, 0.08);
}

.primary-btn {
  border: none;
  border-radius: 12px;
  padding: 14px 32px;
  font-weight: 600;
  color: white;
  background: var(--primary-cyan);
  box-shadow: 0 4px 20px rgba(0, 206, 209, 0.3);
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.primary-btn:hover:not(:disabled) {
  transform: translateY(-3px);
}

.primary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.ghost-btn {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-primary);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
}

.error-banner {
  background: rgba(227, 66, 52, 0.1);
  border: 1px solid rgba(227, 66, 52, 0.3);
  color: #e34234;
  border-radius: 8px;
  padding: 12px 14px;
  animation: slideDown 0.2s ease;
}

.bg-blob {
  position: absolute;
  width: 320px;
  height: 320px;
  border-radius: 999px;
  filter: blur(140px);
  opacity: 0.28;
  animation: float 22s alternate infinite ease-in-out;
}

.bg-blob--cyan {
  background: rgba(0, 206, 209, 0.45);
  top: 10%;
  left: 5%;
}

.bg-blob--red {
  background: rgba(227, 66, 52, 0.35);
  right: 10%;
  bottom: 10%;
}

.glass-fade-enter-active,
.glass-fade-leave-active {
  transition: opacity 0.3s ease, filter 0.3s ease;
}

.glass-fade-enter-from,
.glass-fade-leave-to {
  opacity: 0;
  filter: blur(4px);
}

@keyframes float {
  from {
    transform: translate(0, 0);
  }
  to {
    transform: translate(120px, 80px) scale(1.1);
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>