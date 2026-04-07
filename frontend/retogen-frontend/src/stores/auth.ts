import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginRequest } from '@/services/auth.service'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const loading = ref(false)
  const errorMessage = ref('')

  const isAuthenticated = computed(() => !!token.value)

  async function login(email: string, password: string) {
    loading.value = true
    errorMessage.value = ''

    try {
      const response = await loginRequest({ email, password })

      if (response.confirmation === 'login successful' && response.token) {
        token.value = response.token
        localStorage.setItem('access_token', response.token)
        return { success: true }
      }

      errorMessage.value = response.confirmation || 'Login gagal'
      return { success: false }
    } catch (error) {
      errorMessage.value = 'Terjadi kesalahan saat menghubungi server'
      return { success: false }
    } finally {
      loading.value = false
    }
  }

  function logout() {
    token.value = null
    errorMessage.value = ''
    localStorage.removeItem('access_token')
  }

  return {
    token,
    loading,
    errorMessage,
    isAuthenticated,
    login,
    logout,
  }
})