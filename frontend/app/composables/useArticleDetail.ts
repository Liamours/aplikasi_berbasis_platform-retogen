import type {
  ApiBaseResponse,
  ArticleViewResponse,
  DetailArticle,
  DetailComment,
  DetailCommentTree
} from '~/types/api'

type ArticleReportLog = {
  report_id: string
  reporter_id?: string | null
  reporter_username?: string | null
  reporter_email?: string | null
  description: string
  created_at?: string | null
}

type ArticleWithReports = DetailArticle & {
  report_count?: number
  reports?: ArticleReportLog[]
}

type ArticleViewResponseWithReports = ArticleViewResponse & {
  article_preview?: string
  report_count?: number
  reports?: ArticleReportLog[]
}



const priceFormatter = new Intl.NumberFormat('id-ID', {
  style: 'currency',
  currency: 'IDR',
  maximumFractionDigits: 0
})

export const useArticleDetail = () => {
  const { post } = useApi()
  const authStore = useAuthStore()
  const route = useRoute()

  const article = useState<ArticleWithReports>('ad-article', () => ({
    article_id: '',
    article_title: '',
    article_preview: '',
    article_content: '',
    article_tags: [],
    article_image: null,
    prices: [],
    comments: [],
    ratings: [],
    report_count: 0,
    reports: []
  }))

  const isLoading = useState('ad-loading', () => false)
  const error = useState('ad-error', () => '')


  const ratingDraft = useState('ad-rating-draft', () => 0)
  const ratingFeedback = useState('ad-rating-feedback', () => '')
  const hoverRating = useState('ad-hover-rating', () => 0)
  const commentDraft = useState('ad-comment-draft', () => '')
  const activeReplyId = useState<string | null>('ad-active-reply-id', () => null)
  const replyDrafts = useState<Record<string, string>>('ad-reply-drafts', () => ({}))
  const activeEditId = useState<string | null>('ad-active-edit-id', () => null)
  const editDraft = useState('ad-edit-draft', () => '')

  const reportState = useState('ad-report-state', () => ({
    open: false,
    type: 'article' as 'article' | 'comment',
    targetId: '',
    targetName: '',
    targetContent: '',
    description: ''
  }))

  const reportLogState = useState('ad-report-log-state', () => ({
    open: false
  }))

  const deleteCommentState = useState('ad-delete-comment-state', () => ({
    open: false,
    targetId: '',
    targetOwner: ''
  }))

  const deleteArticleState = useState('ad-delete-article-state', () => ({
    open: false,
    targetId: '',
    title: ''
  }))

  const isAdmin = computed(() => authStore.user?.role === 'admin')
  const currentUserEmail = computed(() => authStore.user?.email || '')

  const isReportLogOpen = computed(() => reportLogState.value.open)
  const reportLogs = computed(() => article.value.reports ?? [])
  const reportLogCount = computed(() => article.value.report_count ?? reportLogs.value.length)

  const averageRating = computed(() => {
    const ratings = article.value.ratings
    if (!ratings?.length) return '0.0'

    const total = ratings.reduce((sum, r) => sum + r.rating_value, 0)
    return (total / ratings.length).toFixed(1)
  })

  const totalComments = computed(() => article.value.comments?.length ?? 0)

  const articleParagraphs = computed(() =>
    (article.value.article_content ?? '')
      .split('\n\n')
      .map((paragraph) => paragraph.trim())
      .filter(Boolean)
  )

  const lowestPrice = computed(() =>
    [...(article.value.prices ?? [])].sort((a, b) => a.price - b.price)[0]
  )

  const visibleStars = computed(() => hoverRating.value || ratingDraft.value)

  const commentTree = computed<DetailCommentTree[]>(() =>
    buildCommentTree(article.value.comments ?? [])
  )

  const ratingSummaryLabel = computed(() => {
    if (ratingFeedback.value) return ratingFeedback.value
    if (!ratingDraft.value) return 'Pilih rating untuk artikel ini'

    const labels: Record<number, string> = {
      1: 'Kurang memuaskan',
      2: 'Masih di bawah ekspektasi',
      3: 'Cukup baik',
      4: 'Solid dan layak',
      5: 'Sangat direkomendasikan'
    }

    return labels[ratingDraft.value] ?? 'Pilih rating'
  })

  function isObjectId(value: string) {
    return /^[a-fA-F0-9]{24}$/.test(value)
  }

  function getCurrentRouteArticleId() {
    const currentId = route.params.id
    return Array.isArray(currentId) ? currentId[0] : String(currentId || '')
  }

  function toImageSrc(value?: string | null) {
    if (!value) return null
    return value.startsWith('data:') ? value : `data:image/jpeg;base64,${value}`
  }

  function getPreview(response: ArticleViewResponseWithReports) {
    if (response.article_preview) return response.article_preview

    return (response.article_content || '')
      .replace(/\s+/g, ' ')
      .trim()
      .slice(0, 128)
  }

  function clearArticleState() {
    article.value = {
      article_id: '',
      article_title: '',
      article_preview: '',
      article_content: '',
      article_tags: [],
      article_image: null,
      prices: [],
      comments: [],
      ratings: [],
      report_count: 0,
      reports: []
    }
  }

  function buildCommentTree(comments: DetailComment[]): DetailCommentTree[] {
    const map = new Map<string, DetailCommentTree>()
    const roots: DetailCommentTree[] = []

    comments.forEach((comment) => {
      map.set(comment.comment_id, { ...comment, children: [] })
    })

    map.forEach((comment) => {
      if (comment.parent_comment_id) {
        const parent = map.get(comment.parent_comment_id)

        if (parent) {
          parent.children.push(comment)
          return
        }
      }

      roots.push(comment)
    })

    return roots
  }

  function formatPrice(value: number) {
    return priceFormatter.format(value)
  }

  function getCurrentUserRating() {
    if (!currentUserEmail.value || !article.value.ratings) return 0

    const email = currentUserEmail.value.toLowerCase()

    return article.value.ratings.find(
      (rating) => rating.user_email?.toLowerCase() === email
    )?.rating_value ?? 0
  }

  watch(
    [currentUserEmail, () => article.value.ratings],
    () => {
      ratingDraft.value = getCurrentUserRating()
    },
    { immediate: true, deep: true }
  )

  function getUserRatingValue(userEmail: string) {
    return article.value.ratings?.find(
      (rating) => rating.user_email === userEmail
    )?.rating_value ?? null
  }

  async function fetchArticle(articleId: string) {
    if (!isObjectId(articleId)) {
      isLoading.value = false
      error.value = ''
      await navigateTo('/main')
      return false
    }

    isLoading.value = true
    error.value = ''

    try {
      const response = await post<ArticleViewResponseWithReports>(
        '/article/view',
        { article_id: articleId },
        true
      )

      if (response.confirmation !== 'successful') {
        await navigateTo('/main')
        return false
      }

      const currentId = getCurrentRouteArticleId()

      if (currentId && articleId !== currentId) {
        return false
      }

      article.value = {
        article_id: articleId,
        article_title: response.article_title,
        article_preview: getPreview(response),
        article_content: response.article_content,
        article_tags: response.article_tags ?? [],
        article_image: toImageSrc(response.article_image),
        prices: [],
        comments: (response.comments ?? []).map((comment) => ({
          ...comment,
          created_at: new Date().toISOString()
        })),
        ratings: response.ratings ?? [],
        report_count: response.report_count ?? response.reports?.length ?? 0,
        reports: response.reports ?? []
      }

      // Parallelize price fetching - don't block article display
      fetchPrices(response.article_title)

      return true
    } catch (err: any) {
      const status = err?.response?.status || err?.statusCode

      if (status === 401) {
        await navigateTo('/')
        return false
      }

      error.value = 'Gagal memuat artikel. Pastikan backend berjalan.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function fetchPrices(productName: string) {
    if (!productName) return

    try {
      const response = await post<any>(
        '/monitor/search',
        {
          product_name: productName,
          limit: 10
        },
        true
      )

      if (response?.results) {
        article.value.prices = response.results.map((item: any, index: number) => ({
          id: `price-${index}`,
          store: item.store || 'Tokopedia',
          product: item.product,
          price: item.price,
          rating: item.rating,
          logo: null
        }))
      }
    } catch (err) {
      console.error('Failed to fetch prices', err)
    }
  }

  async function resetPageState(articleId: string) {
    clearArticleState()

    ratingDraft.value = 0
    ratingFeedback.value = ''
    hoverRating.value = 0
    commentDraft.value = ''
    activeReplyId.value = null
    replyDrafts.value = {}
    activeEditId.value = null
    editDraft.value = ''
    reportLogState.value = { open: false }
    deleteCommentState.value = { open: false, targetId: '', targetOwner: '' }
    deleteArticleState.value = { open: false, targetId: '', title: '' }

    return await fetchArticle(articleId)
  }

  async function setRating(value: number) {
    const normalizedValue = Math.min(5, Math.max(1, Math.round(value)))
    const existingRating = article.value.ratings.find(
      (rating) => rating.user_email === currentUserEmail.value
    )

    try {
      let response: ArticleViewResponse

      if (existingRating) {
        response = await post<ArticleViewResponse>(
          '/rating/edit/update',
          {
            rating_id: existingRating.rating_id,
            article_id: article.value.article_id,
            rating_value: normalizedValue
          },
          true
        )
      } else {
        response = await post<ArticleViewResponse>(
          '/rating/add',
          {
            article_id: article.value.article_id,
            rating_value: normalizedValue
          },
          true
        )
      }

      if (response.confirmation === 'successful') {
        article.value.ratings = response.ratings
        ratingDraft.value = normalizedValue
        ratingFeedback.value = existingRating ? 'Rating diperbarui' : 'Rating disimpan'
        return
      }

      if (response.confirmation === 'already rated') {
        await fetchArticle(article.value.article_id)
        ratingFeedback.value = 'Data rating sinkron kembali. Silakan coba lagi.'
        return
      }

      ratingFeedback.value = response.confirmation
    } catch {
      ratingFeedback.value = 'Gagal menyimpan rating'
    }
  }

  async function submitComment(parentId: string | null = null) {
    const text = (parentId ? (replyDrafts.value[parentId] ?? '') : commentDraft.value).trim()

    if (!text) return

    try {
      const response = await post<ArticleViewResponse>(
        '/comment/add',
        {
          article_id: article.value.article_id,
          parent_comment_id: parentId,
          comment_content: text
        },
        true
      )

      if (response.confirmation === 'successful') {
        article.value.comments = response.comments.map((comment) => ({
          ...comment,
          created_at: new Date().toISOString()
        }))

        if (parentId) {
          replyDrafts.value[parentId] = ''
          activeReplyId.value = null
        } else {
          commentDraft.value = ''
        }
      }
    } catch (err) {
      console.error('Failed to submit comment', err)
    }
  }

  function toggleReply(commentId: string) {
    activeEditId.value = null
    editDraft.value = ''
    activeReplyId.value = activeReplyId.value === commentId ? null : commentId
  }

  function updateReplyDraft(payload: { commentId: string; value: string }) {
    replyDrafts.value[payload.commentId] = payload.value
  }

  function findCommentById(commentId: string) {
    return article.value.comments?.find((comment) => comment.comment_id === commentId) ?? null
  }

  function isOwnComment(comment: Pick<DetailComment, 'user_email'>) {
    return comment.user_email === currentUserEmail.value
  }

  function canEditComment(comment: Pick<DetailComment, 'user_email'>) {
    return isOwnComment(comment)
  }

  function canDeleteComment(comment: Pick<DetailComment, 'user_email'>) {
    return isAdmin.value || isOwnComment(comment)
  }

  function startEditComment(commentId: string) {
    const comment = findCommentById(commentId)

    if (!comment || !canEditComment(comment)) return

    activeReplyId.value = null
    activeEditId.value = commentId
    editDraft.value = comment.comment_content
  }

  function updateEditDraft(value: string) {
    editDraft.value = value
  }

  function cancelEditComment() {
    activeEditId.value = null
    editDraft.value = ''
  }

  async function saveEditComment() {
    if (!activeEditId.value) return

    const text = editDraft.value.trim()

    if (!text) return

    const comment = findCommentById(activeEditId.value)

    if (!comment || !canEditComment(comment)) {
      cancelEditComment()
      return
    }

    try {
      const response = await post<ArticleViewResponse>(
        '/comment/edit/update',
        {
          article_id: article.value.article_id,
          comment_id: activeEditId.value,
          parent_comment_id: comment.parent_comment_id,
          comment_content: text
        },
        true
      )

      if (response.confirmation === 'successful') {
        article.value.comments = response.comments.map((item) => ({
          ...item,
          created_at: new Date().toISOString()
        }))

        cancelEditComment()
      }
    } catch (err) {
      console.error('Failed to save comment edit', err)
    }
  }

  function openDeleteComment(commentId: string) {
    const comment = findCommentById(commentId)

    if (!comment || !canDeleteComment(comment)) return

    deleteCommentState.value = {
      open: true,
      targetId: comment.comment_id,
      targetOwner: comment.owner
    }
  }

  function closeDeleteComment() {
    deleteCommentState.value = {
      open: false,
      targetId: '',
      targetOwner: ''
    }
  }

  async function confirmDeleteComment() {
    const targetId = deleteCommentState.value.targetId

    if (!targetId) return

    try {
      const response = await post<ArticleViewResponse>(
        '/comment/delete',
        { comment_id: targetId },
        true
      )

      if (response.confirmation === 'successful') {
        article.value.comments = response.comments.map((comment) => ({
          ...comment,
          created_at: new Date().toISOString()
        }))

        closeDeleteComment()
      }
    } catch (err) {
      console.error('Failed to delete comment', err)
    }
  }

  function openDeleteArticle(articleId: string) {
    if (!isAdmin.value || !articleId) return

    deleteArticleState.value = {
      open: true,
      targetId: articleId,
      title: article.value.article_title
    }
  }

  function closeDeleteArticle() {
    deleteArticleState.value = {
      open: false,
      targetId: '',
      title: ''
    }
  }

  async function confirmDeleteArticle() {
    const targetId = deleteArticleState.value.targetId

    if (!targetId || !isAdmin.value) return

    try {
      const response = await post<ApiBaseResponse>(
        '/article/delete',
        { article_id: targetId },
        true
      )

      if (response.confirmation.includes('successful')) {
        closeDeleteArticle()
        await navigateTo('/main')
      }
    } catch (err) {
      console.error('Failed to delete article', err)
    }
  }

  function openReportLog() {
    if (!isAdmin.value) return

    reportLogState.value = {
      open: true
    }
  }

  function closeReportLog() {
    reportLogState.value = {
      open: false
    }
  }



  function openReport(
    type: 'article' | 'comment',
    targetId: string,
    targetName: string = '',
    targetContent: string = ''
  ) {
    reportState.value = {
      open: true,
      type,
      targetId,
      targetName,
      targetContent,
      description: ''
    }
  }

  function closeReport() {
    reportState.value = {
      ...reportState.value,
      open: false,
      description: '',
      targetId: '',
      targetName: '',
      targetContent: ''
    }
  }

  async function submitReport() {
    if (!reportState.value.description.trim()) return

    try {
      if (reportState.value.type === 'article') {
        const response = await post<ApiBaseResponse>(
          '/report_article/add',
          {
            article_id: reportState.value.targetId,
            description: reportState.value.description
          },
          true
        )

        if (response.confirmation.includes('successful')) {
          closeReport()
        }

        return
      }

      const comment = article.value.comments?.find(
        (item) => item.comment_id === reportState.value.targetId
      )

      if (!comment) return

      const response = await post<ApiBaseResponse>(
        '/report_user/report_user',
        {
          reported_user_email: comment.user_email || '',
          description: reportState.value.description
        },
        true
      )

      if (response.confirmation.includes('successful')) {
        closeReport()
      }
    } catch (err) {
      console.error('Failed to submit report', err)
    }
  }

  return {
    isAdmin,
    article,
    isLoading,
    error,

    ratingDraft,
    ratingFeedback,
    hoverRating,
    commentDraft,
    activeReplyId,
    replyDrafts,
    activeEditId,
    editDraft,
    reportState,
    reportLogState,
    deleteCommentState,
    deleteArticleState,
    isReportLogOpen,
    reportLogs,
    reportLogCount,
    averageRating,
    totalComments,
    articleParagraphs,
    lowestPrice,
    visibleStars,
    commentTree,
    ratingSummaryLabel,
    resetPageState,
    fetchArticle,
    fetchPrices,
    formatPrice,
    getUserRatingValue,
    setRating,
    submitComment,
    toggleReply,
    updateReplyDraft,
    isOwnComment,
    canEditComment,
    canDeleteComment,
    startEditComment,
    updateEditDraft,
    cancelEditComment,
    saveEditComment,
    openDeleteComment,
    closeDeleteComment,
    confirmDeleteComment,
    openDeleteArticle,
    closeDeleteArticle,
    confirmDeleteArticle,
    openReportLog,
    closeReportLog,

    openReport,
    closeReport,
    submitReport
  }
}