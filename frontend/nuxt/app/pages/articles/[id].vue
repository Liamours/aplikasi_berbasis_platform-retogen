<script setup lang="ts">
const article = {
  article_id: 'demo-article-001',
  article_title: 'MacBook Air M3 untuk produktivitas harian: ringan, cepat, dan tetap efisien',
  article_content: `
MacBook Air M3 hadir sebagai salah satu laptop yang paling menarik untuk kebutuhan produktivitas harian. Desainnya tetap tipis, ringan, dan terasa premium saat digunakan dalam waktu lama.

Untuk pekerjaan seperti browsing berat, penulisan, meeting online, desain ringan, dan multitasking, performanya terasa stabil dan konsisten. Transisi antar aplikasi halus, konsumsi daya efisien, dan pengalaman penggunaan secara umum terasa matang.

Dari sisi layar, kualitas visual tetap menjadi salah satu nilai kuat. Panel yang tajam dan akurat membuat aktivitas membaca, editing ringan, dan konsumsi konten terasa nyaman. Keyboard dan trackpad juga masih menjadi salah satu yang paling enak di kelasnya.

Meski bukan perangkat yang ditujukan untuk semua skenario berat, laptop ini tetap sangat relevan untuk mahasiswa, profesional, content worker ringan, dan pengguna yang mengutamakan portabilitas tanpa kehilangan performa inti.

Secara keseluruhan, MacBook Air M3 cocok untuk pengguna yang ingin perangkat tipis, modern, efisien, dan nyaman dipakai setiap hari.
  `.trim(),
  article_tags: ['laptop', 'apple', 'productivity'],
  article_image: '/logo.png'
}

const ratings = [
  { rating_id: 'r1', owner: 'Farhan', user_email: 'farhan@email.com', rating_value: 5 },
  { rating_id: 'r2', owner: 'Nadia', user_email: 'nadia@email.com', rating_value: 4 },
  { rating_id: 'r3', owner: 'Raka', user_email: 'raka@email.com', rating_value: 5 },
  { rating_id: 'r4', owner: 'Sinta', user_email: 'sinta@email.com', rating_value: 4 }
]

const comments = [
  {
    comment_id: 'c1',
    parent_comment_id: null,
    owner: 'Aldo',
    user_email: 'aldo@email.com',
    comment_content: 'Bahasannya enak dibaca dan cukup membantu buat yang lagi cari laptop ringan untuk kerja harian.'
  },
  {
    comment_id: 'c2',
    parent_comment_id: 'c1',
    owner: 'Mira',
    user_email: 'mira@email.com',
    comment_content: 'Setuju, terutama bagian efisiensi baterainya. Itu yang paling menarik buatku.'
  },
  {
    comment_id: 'c3',
    parent_comment_id: null,
    owner: 'Dimas',
    user_email: 'dimas@email.com',
    comment_content: 'Akan lebih menarik kalau nanti ada pembahasan perbandingan dengan Windows ultrabook di range harga yang mirip.'
  }
]

const averageRating = computed(() => {
  const total = ratings.reduce((sum, item) => sum + item.rating_value, 0)
  return (total / ratings.length).toFixed(1)
})

const articleParagraphs = computed(() => {
  return article.article_content
    .split('\n\n')
    .map(item => item.trim())
    .filter(Boolean)
})

const actionButtons = [
  { label: 'Beri Rating', variant: 'primary' },
  { label: 'Tulis Komentar', variant: 'ghost' },
  { label: 'Report', variant: 'ghost' }
] as const
</script>

<template>
  <BasePageShell>
    <div class="article-page">
      <section class="article-hero">
        <div class="article-hero__content">
          <div class="article-hero__copy">
            <div class="article-hero__tags">
              <span
                v-for="tag in article.article_tags"
                :key="tag"
                class="article-tag"
              >
                {{ tag }}
              </span>
            </div>

            <h1 class="article-hero__title">
              {{ article.article_title }}
            </h1>

            <ArticleMetaBar
              author="RetoGen Editorial"
              published-at="14 Jan 2026"
              reading-time="6 min read"
            />
          </div>

          <BaseGlassCard variant="ghost" class="article-hero__visual">
            <img
              :src="article.article_image"
              alt="Article visual"
              class="article-hero__image"
            >
          </BaseGlassCard>
        </div>
      </section>

      <section class="article-layout">
        <div class="article-main">
          <BaseGlassCard class="article-content">
            <div class="article-content__body">
              <p
                v-for="(paragraph, index) in articleParagraphs"
                :key="index"
                class="article-content__paragraph"
              >
                {{ paragraph }}
              </p>
            </div>
          </BaseGlassCard>

          <BaseGlassCard class="article-comments">
            <div class="article-comments__head">
              <div>
                <p class="article-section-label">Discussion</p>
                <h2 class="article-section-title">
                  Komentar
                </h2>
              </div>

              <span class="article-comments__count">
                {{ comments.length }} komentar
              </span>
            </div>

            <CommentThread :comments="comments" />
          </BaseGlassCard>
        </div>

        <aside class="article-sidebar">
          <ArticleSidebarCard title="Ringkasan">
            <div class="article-summary">
              <div class="article-summary__item">
                <span class="article-summary__label">Rating</span>
                <strong class="article-summary__value">
                  {{ averageRating }}/5
                </strong>
              </div>

              <div class="article-summary__item">
                <span class="article-summary__label">Total rating</span>
                <strong class="article-summary__value">
                  {{ ratings.length }}
                </strong>
              </div>

              <div class="article-summary__item">
                <span class="article-summary__label">Komentar</span>
                <strong class="article-summary__value">
                  {{ comments.length }}
                </strong>
              </div>
            </div>
          </ArticleSidebarCard>

          <ArticleSidebarCard title="Aksi">
            <div class="article-actions">
              <BaseButton
                v-for="action in actionButtons"
                :key="action.label"
                :variant="action.variant"
                block
              >
                {{ action.label }}
              </BaseButton>
            </div>
          </ArticleSidebarCard>

          <ArticleSidebarCard title="Tag">
            <div class="article-sidebar__tags">
              <span
                v-for="tag in article.article_tags"
                :key="tag"
                class="article-tag"
              >
                {{ tag }}
              </span>
            </div>
          </ArticleSidebarCard>
        </aside>
      </section>
    </div>
  </BasePageShell>
</template>

<style scoped>
.article-page {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.article-hero {
  padding-top: 16px;
}

.article-hero__content {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) 320px;
  gap: 24px;
  align-items: stretch;
}

.article-hero__copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 18px;
}

.article-hero__tags,
.article-sidebar__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.article-tag {
  background: rgba(227, 66, 52, 0.1);
  color: var(--primary-red);
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.article-hero__title {
  margin: 0;
  font-size: clamp(34px, 5vw, 52px);
  line-height: 1.08;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -1px;
}

.article-hero__visual {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 260px;
  padding: 24px;
}

.article-hero__image {
  width: min(100%, 180px);
  aspect-ratio: 1;
  object-fit: contain;
  filter: drop-shadow(0 18px 40px rgba(0, 0, 0, 0.12));
}

.article-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 24px;
  align-items: start;
}

.article-main {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.article-content__body {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.article-content__paragraph {
  margin: 0;
  color: var(--text-primary);
  line-height: 1.8;
  font-size: 16px;
}

.article-comments {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.article-comments__head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.article-section-label {
  margin: 0 0 6px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--primary-red);
}

.article-section-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--text-primary);
}

.article-comments__count {
  padding: 8px 12px;
  border-radius: 14px;
  background: rgba(0, 188, 212, 0.08);
  color: var(--primary-cyan);
  font-size: 13px;
  font-weight: 600;
}

.article-sidebar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  position: sticky;
  top: 88px;
}

.article-summary {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.article-summary__item {
  padding: 16px;
  border-radius: 14px;
  background: rgba(100, 100, 100, 0.04);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  transition: var(--transition-standard);
}

.article-summary__item:hover {
  transform: translateX(4px);
}

.article-summary__label {
  color: var(--text-secondary);
  font-size: 14px;
}

.article-summary__value {
  color: var(--text-primary);
  font-size: 16px;
  font-weight: 700;
}

.article-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

@media (max-width: 1024px) {
  .article-hero__content,
  .article-layout {
    grid-template-columns: 1fr;
  }

  .article-sidebar {
    position: static;
  }

  .article-hero__visual {
    min-height: 220px;
  }
}

@media (max-width: 850px) {
  .article-hero__title {
    font-size: 40px;
  }
}

@media (max-width: 480px) {
  .article-content__paragraph {
    font-size: 15px;
  }

  .article-hero__title {
    font-size: 32px;
  }
}
</style>