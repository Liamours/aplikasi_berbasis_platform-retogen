import type { DetailArticle, DetailComment, DetailCommentTree } from '~/types/api'

export const useArticleDetail = () => {
  const currentUser = {
    username: 'You',
    user_email: 'you@retogen.local',
    role: 'admin' as 'user' | 'admin'
  }

  const article = useState<DetailArticle>('ad-article', () => ({} as DetailArticle))
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
    description: ''
  }))

  const deleteCommentState = useState('ad-delete-comment-state', () => ({
    open: false,
    targetId: '',
    targetOwner: ''
  }))

  const isAdmin = computed(() => currentUser.role === 'admin')

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
    return article.value.ratings?.find(
      (rating) => rating.user_email === currentUser.user_email
    )?.rating_value ?? 0
  }

  function getUserRatingValue(userEmail: string) {
    return article.value.ratings?.find(
      (rating) => rating.user_email === userEmail
    )?.rating_value ?? null
  }

  function resetPageState(articleId: string) {
    article.value = useMockArticleDetail(articleId)
    tracked.value = false
    ratingFeedback.value = ''
    hoverRating.value = 0
    commentDraft.value = ''
    activeReplyId.value = null
    replyDrafts.value = {}
    activeEditId.value = null
    editDraft.value = ''
    deleteCommentState.value = { open: false, targetId: '', targetOwner: '' }
    ratingDraft.value = getCurrentUserRating()
  }

  function setRating(value: number) {
    const normalizedValue = Math.min(5, Math.max(1, Math.round(value)))

    if (!article.value.ratings) {
      article.value.ratings = []
    }

    const existingRating = article.value.ratings.find(
      (rating) => rating.user_email === currentUser.user_email
    )

    ratingDraft.value = normalizedValue

    if (existingRating) {
      existingRating.rating_value = normalizedValue
      ratingFeedback.value = 'Rating Anda diperbarui'
      return
    }

    article.value.ratings.push({
      rating_id: `rating-${Date.now()}`,
      owner: currentUser.username,
      user_email: currentUser.user_email,
      rating_value: normalizedValue
    })

    ratingFeedback.value = 'Rating Anda disimpan'
  }

  function submitComment(parentId: string | null = null) {
    const text = (parentId ? (replyDrafts.value[parentId] ?? '') : commentDraft.value).trim()
    if (!text) return

    if (!article.value.comments) {
      article.value.comments = []
    }

    article.value.comments.unshift({
      comment_id: `comment-${Date.now()}`,
      parent_comment_id: parentId,
      owner: currentUser.username,
      user_email: currentUser.user_email,
      comment_content: text,
      created_at: new Date().toISOString()
    })

    if (parentId) {
      replyDrafts.value[parentId] = ''
      activeReplyId.value = null
      return
    }

    commentDraft.value = ''
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
    return comment.user_email === currentUser.user_email
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

  function saveEditComment() {
    if (!activeEditId.value) return

    const text = editDraft.value.trim()
    if (!text) return

    const comment = findCommentById(activeEditId.value)

    if (!comment || !canEditComment(comment)) {
      cancelEditComment()
      return
    }

    comment.comment_content = text
    comment.updated_at = new Date().toISOString()

    cancelEditComment()
  }

  function collectCommentAndChildrenIds(commentId: string) {
    const comments = article.value.comments ?? []
    const ids = new Set<string>([commentId])
    let changed = true

    while (changed) {
      changed = false

      comments.forEach((comment) => {
        if (
          comment.parent_comment_id
          && ids.has(comment.parent_comment_id)
          && !ids.has(comment.comment_id)
        ) {
          ids.add(comment.comment_id)
          changed = true
        }
      })
    }

    return ids
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

  function confirmDeleteComment() {
    const targetId = deleteCommentState.value.targetId
    if (!targetId) return

    const comment = findCommentById(targetId)

    if (!comment || !canDeleteComment(comment)) {
      closeDeleteComment()
      return
    }

    const deletedIds = collectCommentAndChildrenIds(targetId)

    article.value.comments = (article.value.comments ?? []).filter(
      (item) => !deletedIds.has(item.comment_id)
    )

    deletedIds.forEach((id) => {
      delete replyDrafts.value[id]
    })

    if (activeReplyId.value && deletedIds.has(activeReplyId.value)) {
      activeReplyId.value = null
    }

    if (activeEditId.value && deletedIds.has(activeEditId.value)) {
      cancelEditComment()
    }

    closeDeleteComment()
  }

  function toggleTrackPrice() {
    tracked.value = !tracked.value
  }

  function openReport(type: 'article' | 'comment', targetId: string) {
    reportState.value = { open: true, type, targetId, description: '' }
  }

  function closeReport() {
    reportState.value = { ...reportState.value, open: false, description: '', targetId: '' }
  }

  function submitReport() {
    if (!reportState.value.description.trim()) return
    closeReport()
  }

  return {
    currentUser,
    isAdmin,
    article,
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
    averageRating,
    totalComments,
    articleParagraphs,
    lowestPrice,
    visibleStars,
    commentTree,
    ratingSummaryLabel,
    resetPageState,
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
    toggleTrackPrice,
    openReport,
    closeReport,
    submitReport
  }
}