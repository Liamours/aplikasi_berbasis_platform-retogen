import { computed, ref } from 'vue'

export interface ReportUserTarget {
  username: string
  userEmail: string
  commentContent: string
}

interface ReportUserResponse {
  confirmation: string
}

const normalizeCommentPreview = (value: string) => {
  const cleanValue = value.trim().replace(/\s+/g, ' ')

  if (cleanValue.length <= 260) return cleanValue

  return `${cleanValue.slice(0, 260)}...`
}

export const useReportUser = () => {
  const api = useApi()

  const isOpen = ref(false)
  const isSubmitting = ref(false)
  const target = ref<ReportUserTarget | null>(null)
  const description = ref('')
  const errorMessage = ref('')
  const showSuccessPopup = ref(false)
  const successMessage = ref('')

  const commentPreview = computed(() =>
    target.value ? normalizeCommentPreview(target.value.commentContent) : ''
  )

  const canSubmit = computed(() =>
    Boolean(target.value?.userEmail && description.value.trim() && !isSubmitting.value)
  )

  const openReportUser = (payload: ReportUserTarget) => {
    target.value = payload
    description.value = ''
    errorMessage.value = ''
    successMessage.value = ''
    showSuccessPopup.value = false
    isOpen.value = true
  }

  const closeReportUser = () => {
    if (isSubmitting.value) return

    isOpen.value = false
    target.value = null
    description.value = ''
    errorMessage.value = ''
  }

  const closeSuccessPopup = () => {
    showSuccessPopup.value = false
    successMessage.value = ''
  }

  const buildReportDescription = () => {
    if (!target.value) return description.value.trim()

    return [
      `Alasan: ${description.value.trim()}`,
      '',
      `Komentar yang dilaporkan: "${commentPreview.value}"`
    ].join('\n')
  }

  const submitReportUser = async () => {
    if (!target.value || !canSubmit.value) return

    errorMessage.value = ''
    isSubmitting.value = true

    try {
      const response = await api.post<ReportUserResponse>(
        '/report_user/report_user',
        {
          reported_user_email: target.value.userEmail,
          description: buildReportDescription()
        },
        true
      )

      if (response.confirmation !== 'successful: user reported') {
        errorMessage.value = response.confirmation || 'Gagal mengirim report.'
        return
      }

      successMessage.value = `${target.value.username} berhasil dilaporkan.`
      showSuccessPopup.value = true
      isOpen.value = false
      target.value = null
      description.value = ''
    } catch {
      errorMessage.value = 'Gagal terhubung ke server.'
    } finally {
      isSubmitting.value = false
    }
  }

  return {
    isOpen,
    isSubmitting,
    target,
    description,
    errorMessage,
    showSuccessPopup,
    successMessage,
    commentPreview,
    canSubmit,
    openReportUser,
    closeReportUser,
    submitReportUser,
    closeSuccessPopup
  }
}