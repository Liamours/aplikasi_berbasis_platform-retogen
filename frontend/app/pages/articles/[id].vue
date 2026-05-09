<script setup lang="ts">
definePageMeta({
  layout: 'default',
  middleware: 'auth'
})

const route = useRoute()
const { resetPageState } = useArticleDetail()

const {
  resetPageState,
  isLoading,
  error,
  reportState,
  isReportLogOpen,
  deleteCommentState,
  deleteArticleState
} = useArticleDetail()

const { isDark } = useTheme()

useHead({
  htmlAttrs: {
    class: computed(() => (isDark.value ? 'dark-mode' : ''))
  }
})

const canRenderBelowFold = ref(false)
const canRenderModals = ref(false)

const routeArticleId = computed<string>(() => {
  const id = route.params.id

  if (Array.isArray(id)) {
    return id[0] ?? ''
  }

  return typeof id === 'string' ? id : ''
})

const isObjectId = (value: string) => /^[a-fA-F0-9]{24}$/.test(value)

const scheduleIdle = (callback: () => void, fallbackDelay = 300) => {
  if (!import.meta.client) return

  const win = window as Window & {
    requestIdleCallback?: (
      callback: () => void,
      options?: { timeout: number }
    ) => number
  }

  if (typeof win.requestIdleCallback === 'function') {
    win.requestIdleCallback(callback, { timeout: 1200 })
    return
  }

  window.setTimeout(callback, fallbackDelay)
}

watch(
  routeArticleId,
  async (articleId) => {
    if (!isObjectId(articleId)) {
      await navigateTo('/main')
      return
    }

    canRenderBelowFold.value = false
    canRenderModals.value = false

    await resetPageState(articleId)

    scheduleIdle(() => {
      canRenderBelowFold.value = true
    }, 350)

    scheduleIdle(() => {
      canRenderModals.value = true
    }, 700)
  },
  { immediate: true }
)

onMounted(() => {
  scheduleIdle(() => {
    canRenderModals.value = true
  }, 700)
})
</script>

<template>
  <BasePageShell>
    <div class="detail-page">
      <section v-if="isLoading" class="detail-card detail-card--state">
        <p class="detail-feedback">
          Memuat artikel.
        </p>
      </section>

      <section v-else-if="error" class="detail-card detail-card--state">
        <p class="detail-feedback detail-feedback--error">
          {{ error }}
        </p>
      </section>

      <section v-else class="detail-card">
        <DetailArticleHero />

        <div class="detail-card__grid">
          <section class="detail-card__main">
            <DetailArticleReview />
            <DetailArticleRating />
          </section>

          <aside class="detail-card__side">
            <ClientOnly>
              <LazyDetailTrackingStatus v-if="canRenderBelowFold" />

              <div v-else class="side-placeholder">
                <p class="side-placeholder__eyebrow">Monitor harga</p>
                <strong class="side-placeholder__title">Memuat harga setelah konten utama.</strong>
              </div>
            </ClientOnly>
          </aside>
        </div>

        <ClientOnly>
          <LazyDetailArticleDiscussion v-if="canRenderBelowFold" />

          <section v-else class="discussion-placeholder">
            <h2 class="discussion-placeholder__title">Diskusi pengguna</h2>
            <p class="discussion-placeholder__text">
              Diskusi akan dimuat setelah konten utama siap.
            </p>
          </section>
        </ClientOnly>
      </section>

      <ClientOnly>
        <LazyDetailReportModal
          v-if="canRenderModals || reportState.open"
        />

        <LazyDetailReportLogModal
          v-if="canRenderModals || isReportLogOpen"
        />

        <LazyDetailDeleteCommentModal
          v-if="canRenderModals || deleteCommentState.open"
        />

        <LazyDetailDeleteArticleModal
          v-if="canRenderModals || deleteArticleState.open"
        />
      </ClientOnly>
    </div>
  </BasePageShell>
</template>

<style scoped>
.detail-page {
  display: flex;
  justify-content: center;
  min-height: calc(100vh - var(--navbar-height));
  padding: 8px 0 40px;
  background: var(--bg-page);
}

.detail-card {
  width: min(100%, 1080px);
  margin: 0 auto;
  padding: 36px;
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  background: var(--bg-surface);
  box-shadow: 0 8px 22px rgba(60, 55, 50, 0.06);

  /*
    Lebih ringan daripada BaseGlassCard:
    - tidak ada backdrop-filter
    - tidak ada saturate
    - containment bantu browser membatasi layout/paint
  */
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  contain: layout paint style;
}

.detail-card--state {
  padding: 28px;
}

.detail-feedback {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.detail-feedback--error {
  color: var(--primary-red);
}

.detail-card__grid {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.8fr);
  gap: 24px;
  align-items: start;
}

.detail-card__grid > * {
  min-width: 0;
}

.detail-card__main {
  display: grid;
  gap: 18px;
  min-width: 0;
}

.detail-card__side {
  min-width: 0;
  content-visibility: auto;
  contain-intrinsic-size: 320px;
}

.side-placeholder,
.discussion-placeholder {
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.1);
}

.side-placeholder {
  padding: 22px;
}

.side-placeholder__eyebrow {
  margin: 0 0 6px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.side-placeholder__title {
  display: block;
  color: var(--text-primary);
  font-size: 15px;
  line-height: 1.5;
}

.discussion-placeholder {
  margin-top: 28px;
  padding: 20px;
  content-visibility: auto;
  contain-intrinsic-size: 420px;
}

.discussion-placeholder__title {
  margin: 0;
  color: var(--text-primary);
  font-size: 20px;
  line-height: 1.2;
  font-weight: 700;
}

.discussion-placeholder__text {
  margin: 8px 0 0;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}

@media (max-width: 1024px) {
  .detail-card__grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .detail-card {
    padding: 28px 20px;
  }
}
</style>