<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Eye, EyeOff, LoaderCircle } from 'lucide-vue-next'
import { api } from '@/lib/api'
import { saveToken, type LoginResponse } from '@/lib/auth'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const router = useRouter()

const form = reactive({
  email: '',
  password: '',
})

const showPassword = ref(false)
const isSubmitting = ref(false)
const errorMessage = ref('')

function validateForm() {
  if (!form.email.trim()) {
    errorMessage.value = 'Email wajib diisi.'
    return false
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(form.email)) {
    errorMessage.value = 'Format email tidak valid.'
    return false
  }

  if (!form.password.trim()) {
    errorMessage.value = 'Password wajib diisi.'
    return false
  }

  return true
}

function mapErrorMessage(confirmation: string) {
  switch (confirmation) {
    case "email doesn't exist":
      return 'Email tidak terdaftar.'
    case 'password incorrect':
    case 'password is incorrect':
      return 'Password salah.'
    case 'backend error':
      return 'Terjadi kesalahan pada server.'
    case 'login successful':
      return ''
    default:
      return confirmation || 'Login gagal.'
  }
}

async function handleLogin() {
  errorMessage.value = ''

  if (!validateForm()) return

  isSubmitting.value = true

  try {
    const response = await api.post<LoginResponse>('/auth/login', {
      email: form.email,
      password: form.password,
    })

    const data = response.data

    if (data.confirmation === 'login successful' && data.token) {
      saveToken(data.token)
      router.push('/')
      return
    }

    errorMessage.value = mapErrorMessage(data.confirmation)
  } catch (error: any) {
    if (error?.response?.status === 401) {
      errorMessage.value = 'Sesi tidak valid.'
    } else if (error?.response?.status === 422) {
      errorMessage.value = 'Input login tidak valid.'
    } else {
      errorMessage.value = 'Tidak dapat terhubung ke backend.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main class="min-h-screen bg-background text-foreground px-5 py-10 sm:px-6">
    <div class="rounded-2xl border border-border bg-card p-6 shadow-lg">
      <section class="hidden lg:block">
        <div class="max-w-xl">
          <p class="mb-4 text-sm font-semibold uppercase tracking-[0.35em] text-cyan-400">
            RetoGen Platform
          </p>
          <h1 class="mb-5 text-5xl font-extrabold leading-none tracking-tight">
            Masuk untuk membaca review elektronik yang lebih terpercaya
          </h1>
          <p class="text-[15px] leading-7 text-slate-300">
            Masuk ke akunmu untuk melihat artikel, berdiskusi lewat komentar, memberi rating,
            dan menerima update berdasarkan tag yang kamu ikuti.
          </p>
        </div>
      </section>

      <Card class="bg-card text-card-foreground border-border">
        <CardHeader class="space-y-2 pb-4">
          <CardTitle class="text-3xl font-bold">
            Login
          </CardTitle>
          <CardDescription class="text-[15px] leading-6 text-slate-600">
            Gunakan email dan password yang sudah terdaftar.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form class="space-y-5" @submit.prevent="handleLogin">
            <div class="space-y-2 rounded-xl bg-muted p-4">
              <Label for="email">Email</Label>
              <Input
                id="email"
                v-model="form.email"
                type="email"
                placeholder="nama@email.com"
                class="h-12"
                autocomplete="email"
              />
            </div>

            <div class="space-y-2 rounded-xl bg-muted p-4">
              <Label for="password">Password</Label>

              <div class="relative">
                <Input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Masukkan password"
                  class="h-12 pr-12"
                  autocomplete="current-password"
                />
                <button
                  type="button"
                  class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 transition hover:text-slate-700"
                  @click="showPassword = !showPassword"
                >
                  <Eye v-if="!showPassword" class="h-5 w-5" />
                  <EyeOff v-else class="h-5 w-5" />
                </button>
              </div>
            </div>

            <div
              v-if="errorMessage"
              class="rounded-lg border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-200"
            >
              {{ errorMessage }}
            </div>

            <Button
              type="submit"
              class="h-12 w-full"
              :disabled="isSubmitting"
            >
              <LoaderCircle v-if="isSubmitting" class="mr-2 h-4 w-4 animate-spin" />
              {{ isSubmitting ? 'Sedang masuk...' : 'Masuk' }}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  </main>
</template>