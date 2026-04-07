<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <main style="min-height: 100vh; display: grid; place-items: center; padding: 24px;">
    <div class="home-card">
      <div class="accent"></div>
      <h1>Berhasil login</h1>
      <p>JWT token sudah tersimpan dan route ini diproteksi.</p>
      <button class="logout-btn" @click="handleLogout">Logout</button>
    </div>
  </main>
</template>

<style scoped>
.home-card {
  width: min(100%, 520px);
  padding: 40px;
  border-radius: 24px;
  background: var(--glass-bg);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  position: relative;
  overflow: hidden;
}

.accent {
  position: absolute;
  top: 0;
  left: 0;
  height: 4px;
  width: 100%;
  background: linear-gradient(90deg, var(--primary-red), var(--primary-cyan));
}

h1 {
  margin: 0 0 8px;
  font-size: 32px;
  font-weight: 700;
}

p {
  margin: 0 0 24px;
  color: var(--text-secondary);
}

.logout-btn {
  border: none;
  border-radius: 12px;
  padding: 14px 24px;
  background: var(--primary-red);
  color: white;
  font-weight: 600;
  cursor: pointer;
}
</style>