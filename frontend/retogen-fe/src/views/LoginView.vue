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
  <main class="retogen-page min-h-screen px-5 py-10 sm:px-6">
    <div class="retogen-shell mx-auto grid min-h-[calc(100vh-5rem)] max-w-6xl items-center gap-8 lg:grid-cols-[1.1fr_480px]">
      <section class="hidden lg:block">
        <div class="max-w-xl">
          <p class="mb-4 text-sm font-semibold uppercase tracking-[0.35em] text-[var(--primary-cyan)]">
            RetoGen Platform
          </p>
          <h1 class="mb-5 text-5xl font-extrabold leading-none tracking-[-0.05em] text-[var(--text-primary)]">
            Masuk untuk membaca review elektronik yang lebih terpercaya
          </h1>
          <p class="text-[15px] leading-7 text-[var(--text-secondary)]">
            Masuk ke akunmu untuk melihat artikel, berdiskusi lewat komentar, memberi rating,
            dan menerima update berdasarkan tag yang kamu ikuti.
          </p>
        </div>
      </section>

      <Card class="glass-card border-0 shadow-none">
        <div class="glass-accent" />

        <CardHeader class="space-y-2 pb-4">
          <CardTitle class="text-3xl font-bold tracking-[-0.03em] text-[var(--text-primary)]">
            Login
          </CardTitle>
          <CardDescription class="text-[15px] leading-6 text-[var(--text-secondary)]">
            Gunakan email dan password yang sudah terdaftar.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <form class="space-y-5" @submit.prevent="handleLogin">
            <div class="space-y-2">
              <Label for="email" class="retogen-label">Email</Label>
              <Input
                id="email"
                v-model="form.email"
                type="email"
                placeholder="nama@email.com"
                class="retogen-input h-12"
                autocomplete="email"
              />
            </div>

            <div class="space-y-2">
              <Label for="password" class="retogen-label">Password</Label>

              <div class="relative">
                <Input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Masukkan password"
                  class="retogen-input h-12 pr-12"
                  autocomplete="current-password"
                />
                <button
                  type="button"
                  class="absolute top-1/2 right-3 -translate-y-1/2 text-[var(--text-secondary)] transition hover:text-[var(--primary-cyan)]"
                  @click="showPassword = !showPassword"
                >
                  <Eye v-if="!showPassword" class="h-5 w-5" />
                  <EyeOff v-else class="h-5 w-5" />
                </button>
              </div>
            </div>

            <Transition name="glass-fade">
              <div v-if="errorMessage" class="retogen-error-banner">
                {{ errorMessage }}
              </div>
            </Transition>

            <Button
              type="submit"
              class="retogen-primary-btn h-12 w-full"
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