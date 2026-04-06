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
  <main class="min-h-screen bg-background text-foreground px-5 py-10 sm:px-6">
    
    <div class="rounded-2xl border border-border bg-card p-6 shadow-lg">
      
      <p class="mb-2 text-sm font-semibold uppercase tracking-widest text-cyan-500">
        RetoGen
      </p>

      <h1 class="mb-3 text-3xl font-bold">
        Login berhasil
      </h1>

      <p class="mb-6 text-sm text-slate-600">
        Ini halaman sementara setelah autentikasi berhasil.
      </p>

      <div class="space-y-2 rounded-xl bg-muted p-4">
        <p><span class="font-semibold">Email:</span> {{ user?.email }}</p>
        <p><span class="font-semibold">Role:</span> {{ user?.role }}</p>
      </div>

      <div class="mt-6">
        <Button @click="logout">Logout</Button>
      </div>

    </div>

  </main>
</template>