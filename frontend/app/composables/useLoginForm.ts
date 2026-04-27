import type { LoginRequest } from '~/types/api'

export const useLoginForm = () => {
  const { login } = useAuth()

  const form = reactive<LoginRequest>({ email: '', password: '' })
  const errors = reactive({ email: '', password: '', general: '' })
  const isSubmitting = ref(false)

  const clearErrors = () => {
    errors.email = ''
    errors.password = ''
    errors.general = ''
  }

  const validateForm = () => {
    clearErrors()
    let isValid = true

    if (!form.email.trim()) {
      errors.email = 'Email wajib diisi.'
      isValid = false
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      errors.email = 'Format email tidak valid.'
      isValid = false
    }

    if (!form.password) {
      errors.password = 'Password wajib diisi.'
      isValid = false
    }

    return isValid
  }

  const handleSubmit = async () => {
    if (isSubmitting.value || !validateForm()) return

    isSubmitting.value = true
    try {
      const response = await login({ email: form.email.trim(), password: form.password })

      if (response.confirmation === 'login successful') {
        await navigateTo('/main')
        return
      }
      if (response.confirmation === "email doesn't exist") {
        errors.general = 'Email tidak terdaftar.'
        return
      }
      if (response.confirmation === 'password incorrect' || response.confirmation === 'password is incorrect') {
        errors.general = 'Password yang Anda masukkan salah.'
        return
      }
      errors.general = 'Login belum berhasil. Silakan coba lagi.'
    } catch {
      errors.general = 'Terjadi kendala saat menghubungkan ke server.'
    } finally {
      isSubmitting.value = false
    }
  }

  return { form, errors, isSubmitting, handleSubmit }
}
