import type { DetailArticle, DetailComment, DetailCommentTree } from '~/types/api'

export const useArticleDetail = () => {
  const currentUser = { username: 'You', user_email: 'you@retogen.local' }

  const article      = useState<DetailArticle>('ad-article', () => ({} as DetailArticle))
  const tracked      = useState('ad-tracked', () => false)
  const ratingDraft  = useState('ad-rating-draft', () => 0)
  const hoverRating  = useState('ad-hover-rating', () => 0)
  const commentDraft = useState('ad-comment-draft', () => '')
  const activeReplyId = useState<string | null>('ad-active-reply-id', () => null)
  const replyDrafts  = useState<Record<string, string>>('ad-reply-drafts', () => ({}))
  const reportState  = useState('ad-report-state', () => ({
    open: false,
    type: 'article' as 'article' | 'comment',
    targetId: '',
    description: ''
  }))

  const averageRating = computed(() => {
    const ratings = article.value.ratings ?? []
    if (!ratings.length) return '0.0'
    const total = ratings.reduce((sum, r) => sum + r.rating_value, 0)
    return (total / ratings.length).toFixed(1)
  })

  const totalComments = computed(() => article.value.comments?.length ?? 0)

  const articleParagraphs = computed(() =>
    (article.value.article_content ?? '')
      .split('\n\n')
      .map((p) => p.trim())
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
    comments.forEach((c) => map.set(c.comment_id, { ...c, children: [] }))
    map.forEach((c) => {
      if (c.parent_comment_id) {
        const parent = map.get(c.parent_comment_id)
        if (parent) { parent.children.push(c); return }
      }
      roots.push(c)
    })
    return roots
  }

  function formatPrice(value: number) {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency', currency: 'IDR', maximumFractionDigits: 0
    }).format(value)
  }

  function getCurrentUserRating() {
    return article.value.ratings?.find((r) => r.user_email === currentUser.user_email)?.rating_value ?? 0
  }

  function resetPageState(articleId: string) {
    article.value     = useMockArticleDetail(articleId)
    tracked.value     = false
    hoverRating.value = 0
    commentDraft.value = ''
    activeReplyId.value = null
    replyDrafts.value = {}
    ratingDraft.value = getCurrentUserRating()
  }

  function setRating(value: number) {
    ratingDraft.value = value
    const existing = article.value.ratings.find((r) => r.user_email === currentUser.user_email)
    if (existing) { existing.rating_value = value; return }
    article.value.ratings.push({
      rating_id: `rating-${Date.now()}`,
      owner: currentUser.username,
      user_email: currentUser.user_email,
      rating_value: value
    })
  }

  function submitComment(parentId: string | null = null) {
    const text = (parentId ? (replyDrafts.value[parentId] ?? '') : commentDraft.value).trim()
    if (!text) return
    article.value.comments.unshift({
      comment_id: `comment-${Date.now()}`,
      parent_comment_id: parentId,
      owner: currentUser.username,
      user_email: currentUser.user_email,
      comment_content: text,
      created_at: new Date().toISOString()
    })
    if (parentId) { replyDrafts.value[parentId] = ''; activeReplyId.value = null; return }
    commentDraft.value = ''
  }

  function toggleReply(commentId: string) {
    activeReplyId.value = activeReplyId.value === commentId ? null : commentId
  }

  function updateReplyDraft(payload: { commentId: string; value: string }) {
    replyDrafts.value[payload.commentId] = payload.value
  }

  function toggleTrackPrice() { tracked.value = !tracked.value }

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
    article, tracked, ratingDraft, hoverRating, commentDraft,
    activeReplyId, replyDrafts, reportState,
    averageRating, totalComments, articleParagraphs, lowestPrice,
    visibleStars, commentTree, ratingSummaryLabel,
    resetPageState, formatPrice, setRating, submitComment,
    toggleReply, updateReplyDraft, toggleTrackPrice,
    openReport, closeReport, submitReport
  }
}
