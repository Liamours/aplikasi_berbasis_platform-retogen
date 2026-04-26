import { ref, computed } from 'vue'

export interface ManagedUser {
  user_id: string
  username: string
  email: string
  fullname: string
  role: 'user' | 'admin' | string
  report_count: number
  created_at: string
}

interface GetUsersResponse {
  confirmation: string
  users?: ManagedUser[]
}

interface ActionResponse {
  confirmation: string
}

const dummyData: ManagedUser[] = [
  {
    user_id: '1',
    username: 'rafiqlabib',
    email: 'rafiq@mail.com',
    fullname: 'Rafiq Labib',
    role: 'admin',
    report_count: 0,
    created_at: '2025-12-12'
  },
  {
    user_id: '2',
    username: 'dzakydev',
    email: 'dzaky@mail.com',
    fullname: 'Dzaky Pratama',
    role: 'user',
    report_count: 3,
    created_at: '2026-01-08'
  },
  {
    user_id: '3',
    username: 'rifqitech',
    email: 'rifqi@mail.com',
    fullname: 'Rifqi Akbar',
    role: 'user',
    report_count: 7,
    created_at: '2026-02-18'
  }
]

export function useUserManagement() {
  const api = useApi()

  const users = ref<ManagedUser[]>(JSON.parse(JSON.stringify(dummyData)))
  const search = ref('')
  const isLoading = ref(false)
  const actionLoadingId = ref<string | null>(null)
  const selectedBanUser = ref<ManagedUser | null>(null)
  const showSuccessPopup = ref(false)
  const successMessage = ref('')
  const errorMessage = ref('')

  const filteredUsers = computed(() => {
    const keyword = search.value.trim().toLowerCase()
    if (!keyword) return users.value
    return users.value.filter((user) =>
      [user.username, user.fullname, user.email, user.role].some((v) =>
        v?.toLowerCase().includes(keyword)
      )
    )
  })

  const adminCount = computed(() => users.value.filter((u) => u.role === 'admin').length)
  const userCount = computed(() => users.value.filter((u) => u.role !== 'admin').length)

  const clearFeedback = () => {
    showSuccessPopup.value = false
    successMessage.value = ''
    errorMessage.value = ''
  }

  const closeSuccessPopup = () => {
    showSuccessPopup.value = false
    successMessage.value = ''
  }

  const fetchUsers = async () => {
    clearFeedback()
    isLoading.value = true
    try {
      // const response = await api.post<GetUsersResponse>('/user/get_all', {}, true)
      // if (response.confirmation !== 'successful') {
      //   errorMessage.value = response.confirmation || 'Gagal memuat data user.'
      //   users.value = []
      //   return
      // }
      // users.value = response.users ?? []

      await new Promise((resolve) => setTimeout(resolve, 800))
      users.value = JSON.parse(JSON.stringify(dummyData))
    } catch {
      errorMessage.value = 'Gagal terhubung ke server.'
      users.value = []
    } finally {
      isLoading.value = false
    }
  }

  const makeAdmin = async (user: ManagedUser) => {
    if (user.role === 'admin') return
    clearFeedback()
    actionLoadingId.value = user.user_id
    try {
      // const response = await api.post<ActionResponse>('/user/make_admin', { user_id: user.user_id }, true)
      // if (response.confirmation === 'successful: role updated to admin') { ... }

      await new Promise((resolve) => setTimeout(resolve, 800))
      const index = users.value.findIndex((u) => u.user_id === user.user_id)
      if (index !== -1) users.value[index].role = 'admin'
      successMessage.value = `${user.username} berhasil diubah menjadi admin.`
      showSuccessPopup.value = true
    } catch {
      errorMessage.value = 'Gagal mengubah role user.'
    } finally {
      actionLoadingId.value = null
    }
  }

  const openBanConfirm = (user: ManagedUser) => {
    clearFeedback()
    selectedBanUser.value = user
  }

  const closeBanConfirm = () => {
    selectedBanUser.value = null
  }

  const banUser = async () => {
    if (!selectedBanUser.value) return
    clearFeedback()
    actionLoadingId.value = selectedBanUser.value.user_id
    try {
      // const response = await api.post<ActionResponse>('/user/delete', { user_id: selectedBanUser.value.user_id }, true)
      // if (response.confirmation === 'successful: user deleted') { ... }

      await new Promise((resolve) => setTimeout(resolve, 800))
      users.value = users.value.filter((u) => u.user_id !== selectedBanUser.value!.user_id)
      successMessage.value = `${selectedBanUser.value.username} berhasil diban.`
      showSuccessPopup.value = true
      selectedBanUser.value = null
    } catch {
      errorMessage.value = 'Gagal memproses ban user.'
    } finally {
      actionLoadingId.value = null
    }
  }

  const formatDate = (value: string) => {
    if (!value) return '-'
    return new Intl.DateTimeFormat('id-ID', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    }).format(new Date(value))
  }

  return {
    users,
    search,
    isLoading,
    actionLoadingId,
    selectedBanUser,
    showSuccessPopup,
    successMessage,
    errorMessage,
    filteredUsers,
    adminCount,
    userCount,
    fetchUsers,
    makeAdmin,
    openBanConfirm,
    closeBanConfirm,
    banUser,
    closeSuccessPopup,
    formatDate
  }
}