import type { ArticleFormData, DetailArticle } from '~/types/api'

type ArticleFormMode = 'create' | 'edit'

const TITLE_MAX_LENGTH = 256
const PREVIEW_MAX_LENGTH = 128
const TAG_MAX_COUNT = 5
const TAG_MAX_LENGTH = 24

export const useArticleForm = () => {
  const articleDrafts = useState<Record<string, DetailArticle>>('ad-article-drafts', () => ({}))

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

  const isEditMode = computed(() => mode.value === 'edit')

  const normalizedTags = computed(() => normalizeTags(tagsInput.value))

  const titleLength = computed(() => form.value.article_title.length)
  const previewLength = computed(() => form.value.article_preview.length)

  const tagCount = computed(() => normalizedTags.value.length)

  const hasInvalidTagLength = computed(() =>
    normalizedTags.value.some((tag) => tag.length > TAG_MAX_LENGTH)
  )

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

  function validateForm() {
    const title = form.value.article_title.trim()
    const preview = form.value.article_preview.trim()
    const content = form.value.article_content.trim()
    const tags = normalizeTags(tagsInput.value)

    if (!title || title.length > TITLE_MAX_LENGTH) {
      return `Judul wajib diisi dan maksimal ${TITLE_MAX_LENGTH} karakter.`
    }

    if (!preview || preview.length > PREVIEW_MAX_LENGTH) {
      return `Preview wajib diisi dan maksimal ${PREVIEW_MAX_LENGTH} karakter.`
    }

    if (!content || content.length > 65536) {
      return 'Review wajib diisi.'
    }

    if (!tags.length) {
      return 'Minimal satu tag diperlukan.'
    }

    if (tags.length > TAG_MAX_COUNT) {
      return `Maksimal ${TAG_MAX_COUNT} tag.`
    }

    if (tags.some((tag) => tag.length > TAG_MAX_LENGTH)) {
      return `Setiap tag maksimal ${TAG_MAX_LENGTH} karakter.`
    }

    if (hasInvalidTagCharacters(tags)) {
      return 'Tag hanya boleh berisi huruf, angka, spasi, dash, atau underscore.'
    }

    if (!form.value.article_image) {
      return 'Gambar produk wajib diisi.'
    }

    return ''
  }

  function fileToBase64(file: File) {
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

    const base64Image = await fileToBase64(file)

    form.value.article_image = base64Image
    previewImage.value = base64Image
    imageFileName.value = file.name
    formError.value = ''
  }

  function loadForm(nextMode: ArticleFormMode, articleId?: string) {
    resetForm()
    mode.value = nextMode

    if (nextMode === 'create') {
      return
    }

    if (!articleId) {
      formError.value = 'Artikel tidak ditemukan.'
      return
    }

    const article = articleDrafts.value[articleId] ?? useMockArticleDetail(articleId)

    form.value = {
      article_id: article.article_id,
      article_title: article.article_title,
      article_preview: article.article_preview,
      article_content: article.article_content,
      article_tags: article.article_tags,
      article_image: article.article_image
    }

    tagsInput.value = article.article_tags.join(', ')
    previewImage.value = article.article_image || '/logo.jpg'
    imageFileName.value = article.article_image ? 'Gambar saat ini' : ''
  }

  async function submitForm() {
    formError.value = ''
    formSuccess.value = ''

    const validationMessage = validateForm()
    if (validationMessage) {
      formError.value = validationMessage
      return
    }

    isSubmitting.value = true

    const tags = normalizeTags(tagsInput.value)
    const articleId = isEditMode.value
      ? form.value.article_id || 'demo-article'
      : `article-${Date.now()}`

    const existingArticle = articleDrafts.value[articleId] ?? useMockArticleDetail(articleId)

    const nextArticle: DetailArticle = {
      article_id: articleId,
      article_title: form.value.article_title.trim(),
      article_preview: form.value.article_preview.trim(),
      article_content: form.value.article_content.trim(),
      article_tags: tags,
      article_image: form.value.article_image || '/logo.jpg',
      prices: existingArticle.prices ?? [],
      comments: existingArticle.comments ?? [],
      ratings: existingArticle.ratings ?? []
    }

    articleDrafts.value = {
      ...articleDrafts.value,
      [articleId]: nextArticle
    }

    formSuccess.value = isEditMode.value
      ? 'Artikel diperbarui.'
      : 'Artikel dibuat.'

    isSubmitting.value = false

    await navigateTo(`/articles/${articleId}`)
  }

  async function cancelForm() {
    if (isEditMode.value && form.value.article_id) {
      await navigateTo(`/articles/${form.value.article_id}`)
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
    isEditMode,
    normalizedTags,
    titleLength,
    previewLength,
    tagCount,
    hasInvalidTagLength,
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