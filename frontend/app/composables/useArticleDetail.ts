import type { DetailArticle, DetailComment, DetailCommentTree, ArticleViewResponse, ApiBaseResponse, DetailPriceEntry } from '~/types/api'

export const useArticleDetail = () => {
  const { post } = useApi()
  const authStore = useAuthStore()

  const article = useState<DetailArticle>('ad-article', () => ({} as DetailArticle))
  const isLoading = useState('ad-loading', () => false)
  const error = useState('ad-error', () => '')

  const tracked = useState('ad-tracked', () => false)
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

  const averageRating = computed(() => {
    const ratings = article.value.ratings ?? []
    if (!ratings.length) return '0.0'

    const total = ratings.reduce((sum, rating) => sum + rating.rating_value, 0)
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
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      maximumFractionDigits: 0
    }).format(value)
  }

  function getCurrentUserRating() {
    if (!currentUserEmail.value || !article.value.ratings) return 0
    return article.value.ratings.find(
      (rating) => rating.user_email === currentUserEmail.value
    )?.rating_value ?? 0
  }

  function getUserRatingValue(userEmail: string) {
    return article.value.ratings?.find(
      (rating) => rating.user_email === userEmail
    )?.rating_value ?? null
  }

  async function fetchArticle(articleId: string) {
    isLoading.value = true
    error.value = ''

    try {
      const response = await post<ArticleViewResponse>('/article/view', { article_id: articleId }, true)

      if (response.confirmation === 'successful') {
        const image = response.article_image
          ? (response.article_image.startsWith('data:') ? response.article_image : `data:image/jpeg;base64,${response.article_image}`)
          : null

        article.value = {
          article_id: articleId,
          article_title: response.article_title,
          article_preview: response.article_title.substring(0, 100),
          article_content: response.article_content,
          article_tags: response.article_tags,
          article_image: image,
          prices: [],
          comments: response.comments.map(c => ({
            ...c,
            created_at: new Date().toISOString()
          })),
          ratings: response.ratings
        }

        ratingDraft.value = getCurrentUserRating()
        
        // Fetch prices from monitor
        await fetchPrices(response.article_title)
      } else {
        error.value = response.confirmation
      }
    } catch (err: any) {
      error.value = err.message || 'Gagal memuat artikel.'
    } finally {
      isLoading.value = false
    }
  }

  async function fetchPrices(productName: string) {
    if (!productName) return

    try {
      const response = await post<any>('/monitor/search', {
        product_name: productName,
        limit: 10
      }, true)

      if (response && response.results) {
        article.value.prices = response.results.map((r: any, index: number) => ({
          id: `price-${index}`,
          store: r.store || 'Tokopedia',
          product: r.product,
          price: r.price,
          rating: r.rating,
          logo: null
        }))
      }
    } catch (err) {
      console.error('Failed to fetch prices', err)
    }
  }

  function resetPageState(articleId: string) {
    fetchArticle(articleId)
    tracked.value = false
    ratingFeedback.value = ''
    hoverRating.value = 0
    commentDraft.value = ''
    activeReplyId.value = null
    replyDrafts.value = {}
    activeEditId.value = null
    editDraft.value = ''
    deleteCommentState.value = { open: false, targetId: '', targetOwner: '' }
    deleteArticleState.value = { open: false, targetId: '', title: '' }
  }

  async function setRating(value: number) {
    const normalizedValue = Math.min(5, Math.max(1, Math.round(value)))
    const existingRating = article.value.ratings.find(
      (r) => r.user_email === currentUserEmail.value
    )

    try {
      let response: ArticleViewResponse
      if (existingRating) {
        response = await post<ArticleViewResponse>('/rating/edit/update', {
          rating_id: existingRating.rating_id,
          article_id: article.value.article_id,
          rating_value: normalizedValue
        }, true)
      } else {
        response = await post<ArticleViewResponse>('/rating/add', {
          article_id: article.value.article_id,
          rating_value: normalizedValue
        }, true)
      }

      if (response.confirmation === 'successful') {
        article.value.ratings = response.ratings
        ratingDraft.value = normalizedValue
        ratingFeedback.value = existingRating ? 'Rating diperbarui' : 'Rating disimpan'
      } else if (response.confirmation === 'already rated') {
        // If backend says already rated but we didn't find it, refresh article to get the ID
        await fetchArticle(article.value.article_id)
        ratingFeedback.value = 'Data rating sinkron kembali. Silakan coba lagi.'
      } else {
        ratingFeedback.value = response.confirmation
      }
    } catch (err: any) {
      ratingFeedback.value = 'Gagal menyimpan rating'
    }
  }

  async function submitComment(parentId: string | null = null) {
    const text = (parentId ? (replyDrafts.value[parentId] ?? '') : commentDraft.value).trim()
    if (!text) return

    try {
      const response = await post<ArticleViewResponse>('/comment/add', {
        article_id: article.value.article_id,
        parent_comment_id: parentId,
        comment_content: text
      }, true)

      if (response.confirmation === 'successful') {
        article.value.comments = response.comments.map(c => ({
          ...c,
          created_at: new Date().toISOString()
        }))

        if (parentId) {
          replyDrafts.value[parentId] = ''
          activeReplyId.value = null
        } else {
          commentDraft.value = ''
        }
      }
    } catch (err: any) {
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
      const response = await post<ArticleViewResponse>('/comment/edit/update', {
        article_id: article.value.article_id,
        comment_id: activeEditId.value,
        parent_comment_id: comment.parent_comment_id,
        comment_content: text
      }, true)

      if (response.confirmation === 'successful') {
        article.value.comments = response.comments.map(c => ({
          ...c,
          created_at: new Date().toISOString()
        }))
        cancelEditComment()
      }
    } catch (err: any) {
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
      const response = await post<ArticleViewResponse>('/comment/delete', {
        comment_id: targetId
      }, true)

      if (response.confirmation === 'successful') {
        article.value.comments = response.comments.map(c => ({
          ...c,
          created_at: new Date().toISOString()
        }))
        closeDeleteComment()
      }
    } catch (err: any) {
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
      const response = await post<ApiBaseResponse>('/article/delete', {
        article_id: targetId
      }, true)

      if (response.confirmation.includes('successful')) {
        closeDeleteArticle()
        await navigateTo('/main')
      }
    } catch (err: any) {
      console.error('Failed to delete article', err)
    }
  }

  function toggleTrackPrice() {
    tracked.value = !tracked.value
  }

  function openReport(type: 'article' | 'comment', targetId: string, targetName: string = '', targetContent: string = '') {
    reportState.value = { open: true, type, targetId, targetName, targetContent, description: '' }
  }

  function closeReport() {
    reportState.value = { ...reportState.value, open: false, description: '', targetId: '', targetName: '', targetContent: '' }
  }

  async function submitReport() {
    if (!reportState.value.description.trim()) return
    
    try {
      if (reportState.value.type === 'article') {
        const response = await post<ApiBaseResponse>('/report_article/add', {
          article_id: reportState.value.targetId,
          description: reportState.value.description
        }, true)
        
        if (response.confirmation.includes('successful')) {
          closeReport()
        }
      } else {
        const comment = article.value.comments?.find(c => c.comment_id === reportState.value.targetId)
        if (!comment) return

        const response = await post<ApiBaseResponse>('/report_user/report_user', {
          reported_user_email: comment.user_email,
          description: `${reportState.value.description}`
        }, true)

        if (response.confirmation.includes('successful')) {
          closeReport()
        }
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
    tracked,
    ratingDraft,
    ratingFeedback,
    hoverRating,
    commentDraft,
    activeReplyId,
    replyDrafts,
    activeEditId,
    editDraft,
    reportState,
    deleteCommentState,
    deleteArticleState,
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
    toggleTrackPrice,
    openReport,
    closeReport,
    submitReport
  }
}
