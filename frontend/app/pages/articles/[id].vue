<script setup lang="ts">
import DetailCommentItem from '~/components/article-detail/DetailCommentItem.vue'
import DetailPriceTracker from '~/components/article-detail/DetailPriceTracker.vue'
import DetailRatingStars from '~/components/article-detail/DetailRatingStars.vue'
import DetailReportMenu from '~/components/article-detail/DetailReportMenu.vue'

import {
  createDummyArticleDetail,
  type DetailArticle,
  type DetailComment,
  type DetailCommentTree
} from '~/temp/article-detail'

definePageMeta({
  layout: 'default'
})

const route = useRoute()

const currentUser = {
  username: 'You',
  user_email: 'you@retogen.local'
}

const article = ref<DetailArticle>(createDummyArticleDetail(String(route.params.id || 'demo-article')))
const tracked = ref(false)
const ratingDraft = ref(0)
const hoverRating = ref(0)
const commentDraft = ref('')
const activeReplyId = ref<string | null>(null)
const replyDrafts = reactive<Record<string, string>>({})
const reportState = reactive<{
  open: boolean
  type: 'article' | 'comment'
  targetId: string
  description: string
}>({
  open: false,
  type: 'article',
  targetId: '',
  description: ''
})

watch(
  () => route.params.id,
  (newId) => {
    article.value = createDummyArticleDetail(String(newId || 'demo-article'))
    tracked.value = false
    ratingDraft.value = getCurrentUserRating()
    hoverRating.value = 0
    commentDraft.value = ''
    activeReplyId.value = null
    Object.keys(replyDrafts).forEach((key) => delete replyDrafts[key])
  },
  { immediate: true }
)

function getCurrentUserRating() {
  const existing = article.value.ratings.find((item) => item.user_email === currentUser.user_email)
  return existing?.rating_value ?? 0
}

const averageRating = computed(() => {
  if (!article.value.ratings.length) return '0.0'

  const total = article.value.ratings.reduce((sum, item) => sum + item.rating_value, 0)
  return (total / article.value.ratings.length).toFixed(1)
})

const totalComments = computed(() => article.value.comments.length)

const articleParagraphs = computed(() => {
  return article.value.article_content
    .split('\n\n')
    .map((paragraph) => paragraph.trim())
    .filter(Boolean)
})

const lowestPrice = computed(() => {
  return [...article.value.prices].sort((a, b) => a.price - b.price)[0]
})

const visibleStars = computed(() => hoverRating.value || ratingDraft.value)

const commentTree = computed<DetailCommentTree[]>(() => buildCommentTree(article.value.comments))

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

  comments.forEach((comment) => {
    map.set(comment.comment_id, {
      ...comment,
      children: []
    })
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

function setRating(value: number) {
  ratingDraft.value = value

  const existingRating = article.value.ratings.find((item) => item.user_email === currentUser.user_email)

  if (existingRating) {
    existingRating.rating_value = value
    return
  }

  article.value.ratings.push({
    rating_id: `rating-${Date.now()}`,
    owner: currentUser.username,
    user_email: currentUser.user_email,
    rating_value: value
  })
}

function submitComment(parentId: string | null = null) {
  const sourceValue = parentId ? (replyDrafts[parentId] ?? '') : commentDraft.value
  const finalValue = sourceValue.trim()

  if (!finalValue) return

  article.value.comments.unshift({
    comment_id: `comment-${Date.now()}`,
    parent_comment_id: parentId,
    owner: currentUser.username,
    user_email: currentUser.user_email,
    comment_content: finalValue,
    created_at: new Date().toISOString()
  })

  if (parentId) {
    replyDrafts[parentId] = ''
    activeReplyId.value = null
    return
  }

  commentDraft.value = ''
}

function toggleReply(commentId: string) {
  activeReplyId.value = activeReplyId.value === commentId ? null : commentId
}

function updateReplyDraft(payload: { commentId: string, value: string }) {
  replyDrafts[payload.commentId] = payload.value
}

function toggleTrackPrice() {
  tracked.value = !tracked.value
}

function openReport(type: 'article' | 'comment', targetId: string) {
  reportState.open = true
  reportState.type = type
  reportState.targetId = targetId
  reportState.description = ''
}

function closeReport() {
  reportState.open = false
  reportState.description = ''
  reportState.targetId = ''
}

function submitReport() {
  if (!reportState.description.trim()) return
  closeReport()
}
</script>

<template>
  <BasePageShell>
    <div class="article-detail-page">
      <BaseGlassCard class="article-detail-card">
        <div class="article-detail-card__hero">
          <div class="article-detail-card__topbar">
            <div class="article-detail-card__breadcrumbs">
              <NuxtLink to="/" class="article-detail-card__crumb">Home</NuxtLink>
              <span>/</span>
              <span>Article</span>
            </div>

            <DetailReportMenu @report="openReport('article', article.article_id)" />
          </div>

          <div class="article-detail-card__headline">
            <div class="article-detail-card__image-wrap">
              <img
                :src="article.article_image || '/logo.jpg'"
                :alt="article.article_title"
                class="article-detail-card__image"
              >
            </div>

            <div class="article-detail-card__summary">
              <p class="article-detail-card__eyebrow">Electronic review</p>

              <h1 class="article-detail-card__title">
                {{ article.article_title }}
              </h1>

              <p class="article-detail-card__preview">
                {{ article.article_preview }}
              </p>

              <div class="article-detail-card__tags">
                <span v-for="tag in article.article_tags" :key="tag" class="article-detail-card__tag">
                  {{ tag }}
                </span>
              </div>

              <div class="article-detail-card__stats">
                <div class="article-detail-card__stat">
                  <span class="article-detail-card__stat-label">Rating</span>
                  <strong class="article-detail-card__stat-value">{{ averageRating }}/5</strong>
                </div>

                <div class="article-detail-card__stat">
                  <span class="article-detail-card__stat-label">Komentar</span>
                  <strong class="article-detail-card__stat-value">{{ totalComments }}</strong>
                </div>

                <div class="article-detail-card__stat">
                  <span class="article-detail-card__stat-label">Harga terbaik</span>
                  <strong class="article-detail-card__stat-value">{{ formatPrice(lowestPrice.price) }}</strong>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="article-detail-card__content-grid">
          <section class="article-detail-section">
            <div class="content-block">
              <h2 class="content-block__title">Review</h2>

              <div class="content-block__body">
                <p v-for="(paragraph, index) in articleParagraphs" :key="index">
                  {{ paragraph }}
                </p>
              </div>
            </div>

            <div class="content-block">
              <div class="content-block__header">
                <div>
                  <h2 class="content-block__title">Rating pengguna</h2>
                  <p class="content-block__helper">{{ ratingSummaryLabel }}</p>
                </div>

                <div class="content-block__score">
                  <span class="content-block__score-value">{{ averageRating }}</span>
                  <span class="content-block__score-meta">dari {{ article.ratings.length }} rating</span>
                </div>
              </div>

              <div class="content-block__rating-row">
                <DetailRatingStars
                  :model-value="visibleStars"
                  size="lg"
                  @update:model-value="setRating"
                  @hover="hoverRating = $event"
                  @leave="hoverRating = 0"
                />

                <span v-if="ratingDraft" class="content-block__chosen-rating">
                  {{ ratingDraft }}/5
                </span>
              </div>
            </div>

            <div class="content-block">
              <h2 class="content-block__title">Tulis komentar</h2>

              <textarea
                v-model="commentDraft"
                class="article-textarea"
                rows="5"
                placeholder="Bagikan pengalaman, pendapat, atau insight singkat Anda..."
              />

              <div class="content-block__composer-actions">
                <span class="content-block__hint">Komentar singkat dan jelas akan lebih mudah dibaca.</span>
                <BaseButton @click="submitComment()">
                  Kirim komentar
                </BaseButton>
              </div>
            </div>
          </section>

          <aside class="article-detail-side">
            <div class="side-block">
              <DetailPriceTracker
                :prices="article.prices"
                :tracked="tracked"
                @toggle-track="toggleTrackPrice"
              />
            </div>

            <div class="side-block">
              <h2 class="side-block__title">Status tracking</h2>
              <p class="side-block__description">
                {{ tracked ? 'Harga sedang dipantau. Anda bisa lanjutkan integrasi notifikasi di tahap berikutnya.' : 'Aktifkan tracking untuk menandai artikel ini ke daftar pantauan harga.' }}
              </p>

              <div class="side-block__status-row">
                <span class="side-block__status-chip" :class="{ 'is-active': tracked }">
                  {{ tracked ? 'Tracking aktif' : 'Belum aktif' }}
                </span>
                <span class="side-block__status-note">
                  Update terakhir: {{ lowestPrice.updatedAt }}
                </span>
              </div>
            </div>
          </aside>
        </div>

        <section class="article-comments">
          <div class="article-comments__header">
            <div>
              <h2 class="article-comments__title">Diskusi</h2>
              <p class="article-comments__subtitle">Komentar dan balasan tampil dalam satu alur yang rapi.</p>
            </div>
          </div>

          <div class="article-comments__list">
            <DetailCommentItem
              v-for="comment in commentTree"
              :key="comment.comment_id"
              :comment="comment"
              :active-reply-id="activeReplyId"
              :reply-drafts="replyDrafts"
              @open-report="openReport('comment', $event)"
              @toggle-reply="toggleReply"
              @update-reply-draft="updateReplyDraft"
              @submit-reply="submitComment"
            />
          </div>
        </section>
      </BaseGlassCard>

      <Transition name="glass-modal">
        <div v-if="reportState.open" class="report-modal">
          <div class="report-modal__overlay" @click="closeReport" />
          <div class="report-modal__panel">
            <div class="report-modal__header">
              <div>
                <p class="report-modal__eyebrow">Report</p>
                <h2 class="report-modal__title">
                  {{ reportState.type === 'article' ? 'Laporkan artikel' : 'Laporkan komentar' }}
                </h2>
              </div>

              <button type="button" class="report-modal__close" @click="closeReport">
                ×
              </button>
            </div>

            <textarea
              v-model="reportState.description"
              class="article-textarea"
              rows="5"
              placeholder="Jelaskan alasan report secara singkat..."
            />

            <div class="report-modal__actions">
              <BaseButton variant="ghost" @click="closeReport">
                Batal
              </BaseButton>
              <BaseButton
                variant="destructive"
                :disabled="!reportState.description.trim()"
                @click="submitReport"
              >
                Kirim report
              </BaseButton>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </BasePageShell>
</template>

<style scoped>
.article-detail-page {
  display: flex;
  justify-content: center;
  padding: 8px 0 40px;
}

.article-detail-card {
  width: min(100%, 1080px);
  margin: 0 auto;
}

.article-detail-card__hero {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 32px;
}

.article-detail-card__topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.article-detail-card__breadcrumbs {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-size: 13px;
}

.article-detail-card__crumb {
  color: var(--text-secondary);
}

.article-detail-card__headline {
  display: grid;
  grid-template-columns: 260px minmax(0, 1fr);
  gap: 28px;
  align-items: center;
}

.article-detail-card__image-wrap {
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid var(--glass-border);
  background: linear-gradient(135deg, rgba(181, 107, 82, 0.12), rgba(106, 173, 168, 0.14));
  min-height: 260px;
}

.article-detail-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-detail-card__summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.article-detail-card__eyebrow {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
}

.article-detail-card__title {
  font-size: clamp(30px, 4vw, 44px);
  line-height: 1.08;
  font-weight: 800;
  letter-spacing: -1px;
  color: var(--text-primary);
}

.article-detail-card__preview {
  max-width: 64ch;
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.7;
}

.article-detail-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.article-detail-card__tag {
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(181, 107, 82, 0.1);
  color: var(--primary-red);
}

.article-detail-card__stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.article-detail-card__stat {
  padding: 16px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid var(--glass-border);
}

.article-detail-card__stat-label {
  display: block;
  font-size: 12px;
  color: var(--text-secondary);
  margin-bottom: 4px;
}

.article-detail-card__stat-value {
  font-size: 18px;
  color: var(--text-primary);
  font-weight: 700;
}

.article-detail-card__content-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(300px, 0.8fr);
  gap: 24px;
  align-items: start;
}

.article-detail-section,
.article-detail-side {
  display: grid;
  gap: 18px;
}

.content-block,
.side-block {
  border-radius: 20px;
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.14);
  padding: 22px;
}

.content-block__title,
.side-block__title,
.article-comments__title {
  font-size: 20px;
  line-height: 1.1;
  font-weight: 700;
  color: var(--text-primary);
}

.content-block__body {
  margin-top: 14px;
  display: grid;
  gap: 14px;
  color: var(--text-secondary);
}

.content-block__body p {
  line-height: 1.75;
}

.content-block__header {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
  margin-bottom: 14px;
}

.content-block__helper {
  margin-top: 6px;
  color: var(--text-secondary);
  font-size: 13px;
}

.content-block__score {
  text-align: right;
}

.content-block__score-value {
  display: block;
  font-size: 28px;
  font-weight: 800;
  line-height: 1;
  color: var(--text-primary);
}

.content-block__score-meta {
  font-size: 12px;
  color: var(--text-secondary);
}

.content-block__rating-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.content-block__chosen-rating {
  border-radius: 999px;
  padding: 7px 12px;
  background: rgba(181, 107, 82, 0.1);
  color: var(--primary-red);
  font-size: 12px;
  font-weight: 700;
}

.article-textarea {
  width: 100%;
  resize: vertical;
  min-height: 120px;
  margin-top: 14px;
  border-radius: 14px;
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
  padding: 14px;
  outline: none;
  font: inherit;
  line-height: 1.65;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.content-block__composer-actions {
  margin-top: 14px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: center;
}

.content-block__hint {
  color: var(--text-secondary);
  font-size: 13px;
}

.side-block__description {
  margin-top: 10px;
  color: var(--text-secondary);
  line-height: 1.7;
}

.side-block__status-row {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.side-block__status-chip {
  align-self: flex-start;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(99, 99, 96, 0.12);
  color: var(--text-secondary);
  font-size: 12px;
  font-weight: 700;
}

.side-block__status-chip.is-active {
  background: rgba(106, 173, 168, 0.14);
  color: var(--primary-cyan);
}

.side-block__status-note {
  font-size: 12px;
  color: var(--text-secondary);
}

.article-comments {
  margin-top: 28px;
  padding-top: 28px;
  border-top: 1px solid var(--glass-border);
}

.article-comments__header {
  margin-bottom: 18px;
}

.article-comments__subtitle {
  margin-top: 6px;
  color: var(--text-secondary);
  font-size: 14px;
}

.article-comments__list {
  display: grid;
  gap: 14px;
}

.report-modal {
  position: fixed;
  inset: 0;
  z-index: 9999;
}

.report-modal__overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.report-modal__panel {
  position: relative;
  width: min(100%, 460px);
  margin: 12vh auto 0;
  padding: 28px;
  border-radius: 20px;
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
}

.report-modal__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}

.report-modal__eyebrow {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.report-modal__title {
  font-size: 22px;
  line-height: 1.1;
  font-weight: 700;
  color: var(--text-primary);
}

.report-modal__close {
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
}

.report-modal__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}

@media (max-width: 1024px) {
  .article-detail-card__content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 850px) {
  .article-detail-card__headline {
    grid-template-columns: 1fr;
  }

  .article-detail-card__image-wrap {
    min-height: 220px;
  }

  .article-detail-card__stats {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .article-detail-card {
    padding: 28px 20px;
  }

  .content-block,
  .side-block {
    padding: 18px;
  }

  .content-block__header,
  .content-block__composer-actions,
  .report-modal__actions {
    flex-direction: column;
    align-items: stretch;
  }

  .content-block__score {
    text-align: left;
  }

  .report-modal__panel {
    width: calc(100% - 24px);
    margin-top: 10vh;
    padding: 22px;
  }
}
</style>