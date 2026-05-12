import type {
  ApiBaseResponse,
  ArticleFormData
} from '~/types/api'

type ArticleFormMode = 'create' | 'edit'

type ArticleEditGetResponse = ApiBaseResponse & {
  article_id: string
  article_title: string
  article_preview: string
  article_content: string
  article_tags: string[]
  article_image: string | null
}

const TITLE_MAX_LENGTH = 256
const PREVIEW_MAX_LENGTH = 128
const TAG_MAX_COUNT = 5
const TAG_MAX_LENGTH = 24

export const useArticleForm = () => {
  const { post } = useApi()

  const mode = useState<ArticleFormMode>('article-form-mode', () => 'create')

  const form = useState<ArticleFormData>('article-form-data', () => ({
    article_id: '',
    article_title: '',
    article_preview: '',
    article_content: '',
    article_tags: [],
    article_image: null
  }))

  const tagsInput = useState('article-form-tags-input', () => '')
  const previewImage = useState<string | null>('article-form-preview-image', () => null)
  const imageFileName = useState('article-form-image-file-name', () => '')
  const formError = useState('article-form-error', () => '')
  const formSuccess = useState('article-form-success', () => '')
  const isSubmitting = useState('article-form-submitting', () => false)
  const isLoading = useState('article-form-loading', () => false)
  const showSuccessModal = useState('article-form-show-success-modal', () => false)

  const isEditMode = computed(() => mode.value === 'edit')

  const normalizedTags = computed(() => normalizeTags(tagsInput.value))

  const titleLength = computed(() => String(form.value.article_title || '').length)
  const previewLength = computed(() => String(form.value.article_preview || '').length)

  const tagCount = computed(() => normalizedTags.value.length)

  const hasInvalidTagLength = computed(() =>
    normalizedTags.value.some((tag) => tag.length > TAG_MAX_LENGTH)
  )

  function isObjectId(value: string) {
    return /^[a-fA-F0-9]{24}$/.test(value)
  }

  function resetForm() {
    form.value = {
      article_id: '',
      article_title: '',
      article_preview: '',
      article_content: '',
      article_tags: [],
      article_image: null
    }

    tagsInput.value = ''
    previewImage.value = null
    imageFileName.value = ''
    formError.value = ''
    formSuccess.value = ''
    isSubmitting.value = false
    isLoading.value = false
  }

  function normalizeTags(value: string) {
    return value
      .split(',')
      .map((tag) => tag.trim().toLowerCase())
      .filter(Boolean)
      .map((tag) => tag.replace(/\s+/g, ' '))
  }

  function hasInvalidTagCharacters(tags: string[]) {
    return tags.some((tag) => !/^[a-z0-9 _-]+$/.test(tag))
  }

  function stripDataUrl(value: string) {
    const separatorIndex = value.indexOf(',')

    if (separatorIndex >= 0) {
      return value.slice(separatorIndex + 1)
    }

    return value
  }

  function toImageSrc(value?: string | null) {
    if (!value) return null

    if (value.startsWith('data:')) {
      return value
    }

    return `data:image/jpeg;base64,${value}`
  }

  function validateForm() {
    const title = String(form.value.article_title || '').trim()
    const preview = String(form.value.article_preview || '').trim()
    const content = String(form.value.article_content || '').trim()
    const tags = normalizeTags(tagsInput.value)

    if (!title || title.length > TITLE_MAX_LENGTH) {
      return {
        message: `Judul wajib diisi dan maksimal ${TITLE_MAX_LENGTH} karakter.`,
        fieldId: 'field-title'
      }
    }

    if (!preview || preview.length > PREVIEW_MAX_LENGTH) {
      return {
        message: `Preview wajib diisi dan maksimal ${PREVIEW_MAX_LENGTH} karakter.`,
        fieldId: 'field-preview'
      }
    }

    if (!content || content.length > 65536) {
      return {
        message: 'Review wajib diisi.',
        fieldId: 'field-content'
      }
    }

    if (!tags.length) {
      return {
        message: 'Minimal satu tag diperlukan.',
        fieldId: 'field-tags'
      }
    }

    if (tags.length > TAG_MAX_COUNT) {
      return {
        message: `Maksimal ${TAG_MAX_COUNT} tag.`,
        fieldId: 'field-tags'
      }
    }

    if (tags.some((tag) => tag.length > TAG_MAX_LENGTH)) {
      return {
        message: `Setiap tag maksimal ${TAG_MAX_LENGTH} karakter.`,
        fieldId: 'field-tags'
      }
    }

    if (hasInvalidTagCharacters(tags)) {
      return {
        message: 'Tag hanya boleh berisi huruf, angka, spasi, dash, atau underscore.',
        fieldId: 'field-tags'
      }
    }

    if (!form.value.article_image) {
      return {
        message: 'Gambar produk wajib diisi.',
        fieldId: 'field-image'
      }
    }

    return null
  }

  function fileToDataUrl(file: File) {
    return new Promise<string>((resolve, reject) => {
      const reader = new FileReader()

      reader.onload = () => {
        resolve(String(reader.result || ''))
      }

      reader.onerror = () => {
        reject(new Error('Gagal membaca gambar.'))
      }

      reader.readAsDataURL(file)
    })
  }

  async function handleImageChange(event: Event) {
    const input = event.target as HTMLInputElement
    const file = input.files?.[0]

    if (!file) return

    const allowedTypes = ['image/png', 'image/jpeg']

    if (!allowedTypes.includes(file.type)) {
      formError.value = 'Gunakan gambar PNG atau JPEG.'
      input.value = ''
      return
    }

    try {
      const dataUrl = await fileToDataUrl(file)

      form.value.article_image = stripDataUrl(dataUrl)
      previewImage.value = dataUrl
      imageFileName.value = file.name
      formError.value = ''
    } catch {
      formError.value = 'Gagal membaca gambar.'
      input.value = ''
    }
  }

  async function loadForm(nextMode: ArticleFormMode, articleId?: string) {
    resetForm()
    mode.value = nextMode

    if (nextMode === 'create') {
      return
    }

    const currentArticleId = articleId || ''

    if (!isObjectId(currentArticleId)) {
      await navigateTo('/main')
      return
    }

    isLoading.value = true

    try {
      const response = await post<ArticleEditGetResponse>(
        '/article/edit/get',
        { article_id: currentArticleId },
        true
      )

      if (response.confirmation !== 'successful') {
        await navigateTo('/main')
        return
      }

      form.value = {
        article_id: response.article_id,
        article_title: response.article_title,
        article_preview: response.article_preview,
        article_content: response.article_content,
        article_tags: response.article_tags ?? [],
        article_image: response.article_image
      }

      tagsInput.value = (response.article_tags ?? []).join(', ')
      previewImage.value = toImageSrc(response.article_image)
      imageFileName.value = response.article_image ? 'Gambar saat ini' : ''
    } catch (err: any) {
      const status = err?.response?.status || err?.statusCode

      if (status === 401) {
        await navigateTo('/')
        return
      }

      await navigateTo('/main')
    } finally {
      isLoading.value = false
    }
  }

  async function submitForm() {
    formError.value = ''
    formSuccess.value = ''

    const validation = validateForm()

    if (validation) {
      formError.value = validation.message
      const element = document.getElementById(validation.fieldId)
      if (element) {
        const offset = 100
        const bodyRect = document.body.getBoundingClientRect().top
        const elementRect = element.getBoundingClientRect().top
        const elementPosition = elementRect - bodyRect
        const offsetPosition = elementPosition - offset

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        })
      }
      return
    }

    const currentArticleId = form.value.article_id || ''

    if (isEditMode.value && !isObjectId(currentArticleId)) {
      await navigateTo('/main')
      return
    }

    isSubmitting.value = true

    const payload = {
      article_title: String(form.value.article_title || '').trim(),
      article_preview: String(form.value.article_preview || '').trim(),
      article_content: String(form.value.article_content || '').trim(),
      article_tags: normalizeTags(tagsInput.value),
      article_image: stripDataUrl(String(form.value.article_image || ''))
    }

    try {
      if (isEditMode.value) {
        const response = await post<ApiBaseResponse>(
          '/article/edit/update',
          {
            article_id: currentArticleId,
            ...payload
          },
          true
        )

        if (response.confirmation !== 'successful: article edited') {
          formError.value = response.confirmation || 'Gagal memperbarui artikel.'
          return
        }

        formSuccess.value = 'Artikel diperbarui.'
        await navigateTo(`/articles/${currentArticleId}`)
        return
      }

      const response = await post<ApiBaseResponse>(
        '/article/add',
        payload,
        true
      )

      if (response.confirmation !== 'success: article added') {
        formError.value = response.confirmation || 'Gagal membuat artikel.'
        return
      }

      formSuccess.value = 'Artikel berhasil dibuat.'
      showSuccessModal.value = true

      setTimeout(() => {
        resetForm()
        showSuccessModal.value = false
        window.scrollTo({ top: 0, behavior: 'smooth' })
      }, 2000)
    } catch (err: any) {
      const status = err?.response?.status || err?.statusCode

      if (status === 401) {
        await navigateTo('/')
        return
      }

      formError.value = 'Gagal terhubung ke server.'
    } finally {
      isSubmitting.value = false
    }
  }

  async function cancelForm() {
    const currentArticleId = form.value.article_id || ''

    if (isEditMode.value && currentArticleId) {
      await navigateTo(`/articles/${currentArticleId}`)
      return
    }

    await navigateTo('/main')
  }

  return {
    mode,
    form,
    tagsInput,
    previewImage,
    imageFileName,
    formError,
    formSuccess,
    isSubmitting,
    isLoading,
    isEditMode,
    normalizedTags,
    titleLength,
    previewLength,
    tagCount,
    hasInvalidTagLength,
    showSuccessModal,
    TITLE_MAX_LENGTH,
    PREVIEW_MAX_LENGTH,
    TAG_MAX_COUNT,
    TAG_MAX_LENGTH,
    loadForm,
    handleImageChange,
    submitForm,
    cancelForm
  }
}