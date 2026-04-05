<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { decodeJwt, getToken, removeToken, type DecodedToken } from '@/lib/auth'

const router = useRouter()

const user = computed(() => {
  const token = getToken()
  if (!token) return null
  return decodeJwt<DecodedToken>(token)
})

function logout() {
  removeToken()
  router.push('/login')
}
</script>

<template>
  <main class="min-h-screen retogen-page px-6 py-10">
    <div class="retogen-shell mx-auto max-w-5xl">
      <section class="glass-card max-w-2xl">
        <div class="glass-accent" />

        <p class="mb-2 text-sm font-semibold tracking-[0.3em] text-[var(--primary-cyan)] uppercase">
          RetoGen
        </p>
        <h1 class="mb-3 text-4xl font-extrabold tracking-[-0.04em] text-[var(--text-primary)]">
          Login berhasil
        </h1>
        <p class="mb-6 text-[15px] leading-7 text-[var(--text-secondary)]">
          Ini halaman sementara setelah autentikasi berhasil.
        </p>

        <div class="grid gap-4 rounded-2xl bg-white/10 p-4 backdrop-blur-md">
          <p><span class="font-semibold">Email:</span> {{ user?.email }}</p>
          <p><span class="font-semibold">Role:</span> {{ user?.role }}</p>
        </div>

        <div class="mt-6 flex gap-3">
          <Button class="retogen-primary-btn" @click="logout">Logout</Button>
        </div>
      </section>
    </div>
  </main>
</template>