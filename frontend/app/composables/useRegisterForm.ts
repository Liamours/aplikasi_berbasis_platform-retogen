import type { RegisterRequest } from '~/types/api'

type RegisterFormErrors = {
  username: string
  fullname: string
  email: string
  password: string
  general: string
}

export const useRegisterForm = () => {
  const { register } = useAuth()

  const form = reactive<RegisterRequest>({
    username: '',
    fullname: '',
    email: '',
    password: ''
  })

  const errors = reactive<RegisterFormErrors>({
    username: '',
    fullname: '',
    email: '',
    password: '',
    general: ''
  })

  const isSubmitting = ref(false)
  const isSuccess = ref(false)

  const clearErrors = () => {
    errors.username = ''
    errors.fullname = ''
    errors.email = ''
    errors.password = ''
    errors.general = ''
  }

  const validateForm = () => {
    clearErrors()
    let isValid = true

    const username = form.username.trim()
    const fullname = form.fullname.trim()
    const email = form.email.trim()
    const password = form.password

    if (!username) {
      errors.username = 'Username wajib diisi.'
      isValid = false
    } else if (!/^[a-zA-Z0-9]+$/.test(username)) {
      errors.username = 'Username hanya boleh huruf dan angka.'
      isValid = false
    } else if (username.length < 8 || username.length > 16) {
      errors.username = 'Username harus 8-16 karakter.'
      isValid = false
    }

    if (!fullname) {
      errors.fullname = 'Nama lengkap wajib diisi.'
      isValid = false
    } else if (!/^[A-Za-z\s]+$/.test(fullname)) {
      errors.fullname = 'Nama lengkap hanya boleh huruf dan spasi.'
      isValid = false
    } else if (fullname.length < 4 || fullname.length > 32) {
      errors.fullname = 'Nama lengkap harus 4-32 karakter.'
      isValid = false
    }

    if (!email) {
      errors.email = 'Email wajib diisi.'
      isValid = false
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errors.email = 'Format email tidak valid.'
      isValid = false
    }

    if (!password) {
      errors.password = 'Password wajib diisi.'
      isValid = false
    } else if (password.length < 8 || password.length > 16) {
      errors.password = 'Password harus 8-16 karakter.'
      isValid = false
    } else if (
      !/[A-Z]/.test(password) ||
      !/[a-z]/.test(password) ||
      !/[0-9]/.test(password)
    ) {
      errors.password = 'Password harus mengandung huruf besar, huruf kecil, dan angka.'
      isValid = false
    }

    return isValid
  }

  const applyServerError = (message: string) => {
    const normalized = message.toLowerCase()

    if (normalized.includes('email')) {
      errors.email = message
      return
    }

    if (normalized.includes('username')) {
      errors.username = message
      return
    }

    if (normalized.includes('fullname') || normalized.includes('full name') || normalized.includes('name')) {
      errors.fullname = message
      return
    }

    if (normalized.includes('password')) {
      errors.password = message
      return
    }

    errors.general = message
  }

  const resetForm = () => {
    form.username = ''
    form.fullname = ''
    form.email = ''
    form.password = ''
  }

  const handleSubmit = async () => {
    if (isSubmitting.value || isSuccess.value || !validateForm()) return

    isSubmitting.value = true

    try {
      const payload: RegisterRequest = {
        username: form.username.trim(),
        fullname: form.fullname.trim().replace(/\s+/g, ' '),
        email: form.email.trim(),
        password: form.password
      }

      const response = await register(payload)

      if (response.confirmation === 'register successful') {
        isSuccess.value = true
        clearErrors()
        resetForm()

        setTimeout(() => {
          navigateTo('/login')
        }, 900)

        return
      }

      if (response.confirmation === 'email already registered') {
        errors.email = 'Email sudah terdaftar.'
        return
      }

      applyServerError(response.confirmation || 'Registrasi belum berhasil.')
    } catch {
      errors.general = 'Terjadi kendala saat menghubungkan ke server.'
    } finally {
      isSubmitting.value = false
    }
  }

  return {
    form,
    errors,
    isSubmitting,
    isSuccess,
    handleSubmit
  }
}