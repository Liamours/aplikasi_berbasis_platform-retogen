import { computed, ref } from 'vue'

export interface OwnUserProfile {
  user_id?: string
  username: string
  email: string
  fullname: string
  role?: string
  created_at?: string
  updated_at?: string
  reports?: unknown[]
}

export interface PublicUserProfile {
  user_id?: string
  user_email?: string
  username: string
  fullname?: string
  role?: string
  created_at: string
  report_count?: number
  reports?: Array<{
    report_id: string
    user_id: string
    description: string
    created_at: string
  }>
}

interface UserDetailsResponse {
  confirmation: string
  user: OwnUserProfile
}

interface PublicUserProfileResponse {
  confirmation: string
  user: PublicUserProfile
}

const getInitials = (value?: string) => {
  const source = value?.trim()

  if (!source) return 'R'

  return source.slice(0, 1).toUpperCase()
}

const formatDate = (value?: string) => {
  if (!value) return '-'

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) return '-'

  return new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  }).format(date)
}

export const useUserProfile = () => {
  const api = useApi()
  const authStore = useAuthStore()

  const profile = ref<OwnUserProfile | null>(
    authStore.user
      ? {
          username: authStore.user.username,
          fullname: authStore.user.fullname ?? '',
          email: authStore.user.email,
          role: authStore.user.role ?? undefined
        }
      : null
  )

  const isLoading = ref(false)
  const errorMessage = ref('')

  const otherProfile = ref<PublicUserProfile | null>(null)
  const isOtherProfileOpen = ref(false)
  const isOtherLoading = ref(false)
  const otherErrorMessage = ref('')

  const profileInitials = computed(() =>
    getInitials(profile.value?.fullname || profile.value?.username)
  )

  const otherProfileInitials = computed(() =>
    getInitials(otherProfile.value?.username)
  )

  const fetchProfile = async () => {
    errorMessage.value = ''
    isLoading.value = true

    try {
      const response = await api.post<UserDetailsResponse>(
        '/user/get_details',
        { user_email: '' },
        true
      )

      if (response.confirmation !== 'successful') {
        errorMessage.value = response.confirmation || 'Gagal memuat profil.'
        return
      }

      profile.value = response.user

      authStore.setUser({
        email: response.user.email,
        username: response.user.username,
        fullname: response.user.fullname,
        role: response.user.role === 'admin' ? 'admin' : 'user'
      })
    } catch {
      errorMessage.value = 'Gagal terhubung ke server.'
    } finally {
      isLoading.value = false
    }
  }

  const openOtherUserProfile = async (userEmail: string) => {
    if (!userEmail) return

    otherProfile.value = null
    otherErrorMessage.value = ''
    isOtherProfileOpen.value = true
    isOtherLoading.value = true

    try {
      // Use /user/get_details which returns reports for admins
      const response = await api.post<UserDetailsResponse>(
        '/user/get_details',
        { user_email: userEmail },
        true
      )

      if (response.confirmation !== 'successful') {
        otherErrorMessage.value = response.confirmation || 'Profil tidak tersedia.'
        return
      }

      // Map OwnUserProfile to PublicUserProfile
      otherProfile.value = {
        user_id: response.user.user_id,
        user_email: response.user.email,
        username: response.user.username,
        fullname: response.user.fullname,
        role: response.user.role,
        created_at: response.user.created_at || '',
        reports: response.user.reports as any
      }
    } catch {
      otherErrorMessage.value = 'Gagal memuat profil user.'
    } finally {
      isOtherLoading.value = false
    }
  }

  const openOtherUserPreview = (user: PublicUserProfile) => {
    otherProfile.value = user
    otherErrorMessage.value = ''
    isOtherLoading.value = false
    isOtherProfileOpen.value = true
  }

  const closeOtherUserProfile = () => {
    isOtherProfileOpen.value = false
    otherProfile.value = null
    otherErrorMessage.value = ''
    isOtherLoading.value = false
  }

  return {
    profile,
    isLoading,
    errorMessage,
    profileInitials,
    otherProfile,
    otherProfileInitials,
    isOtherProfileOpen,
    isOtherLoading,
    otherErrorMessage,
    fetchProfile,
    openOtherUserProfile,
    openOtherUserPreview,
    closeOtherUserProfile,
    formatDate
  }
}