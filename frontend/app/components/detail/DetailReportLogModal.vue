<script setup lang="ts">
const {
  isReportLogOpen,
  reportLogs,
  reportLogCount,
  closeReportLog
} = useArticleDetail()

const getInitials = (value?: string | null) => {
  const source = value?.trim()

  if (!source) return 'U'

  return source.slice(0, 1).toUpperCase()
}

const formatReportDate = (value?: string | null) => {
  if (!value) return '-'

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) return '-'

  return new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}
</script>

<template>
  <Teleport to="body">
    <Transition name="glass-modal">
      <div
        v-if="isReportLogOpen"
        class="report-log-modal"
        @click.self="closeReportLog"
      >
        <section
          class="report-log-modal__panel"
          role="dialog"
          aria-modal="true"
          aria-labelledby="report-log-title"
        >
          <header class="report-log-modal__header">
            <div>
              <p class="report-log-modal__eyebrow">
                Admin log
              </p>

              <h2 id="report-log-title" class="report-log-modal__title">
                Log report artikel
              </h2>

              <p class="report-log-modal__subtitle">
                {{ reportLogCount }} report masuk untuk artikel ini.
              </p>
            </div>

            <button
              type="button"
              class="report-log-modal__close"
              aria-label="Tutup log report"
              @click="closeReportLog"
            >
              ×
            </button>
          </header>

          <div v-if="!reportLogs.length" class="report-log-modal__empty">
            Belum ada report untuk artikel ini.
          </div>

          <div v-else class="report-log-modal__list">
            <article
              v-for="report in reportLogs"
              :key="report.report_id"
              class="report-log-modal__item"
            >
              <div class="report-log-modal__reporter">
                <div class="report-log-modal__avatar" aria-hidden="true">
                  {{ getInitials(report.reporter_username) }}
                </div>

                <div class="report-log-modal__meta">
                  <div class="report-log-modal__name-row">
                    <strong class="report-log-modal__name">
                      {{ report.reporter_username || 'Unknown' }}
                    </strong>

                    <span class="report-log-modal__date">
                      {{ formatReportDate(report.created_at) }}
                    </span>
                  </div>

                  <p class="report-log-modal__email">
                    {{ report.reporter_email || 'Email tidak tersedia' }}
                  </p>
                </div>
              </div>

              <div class="report-log-modal__reason">
                <span class="report-log-modal__label">
                  Isi report
                </span>

                <p>
                  {{ report.description }}
                </p>
              </div>
            </article>
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.report-log-modal {
  position: fixed;
  inset: 0;
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(0, 0, 0, 0.46);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.report-log-modal__panel {
  width: min(100%, 620px);
  max-height: calc(100vh - 48px);
  min-width: 0;
  overflow: hidden;
  border-radius: 18px;
  border: 1px solid var(--glass-border);
  background: var(--bg-surface);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.2);
  padding: 28px;
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
}

.report-log-modal__header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 36px;
  gap: 16px;
  align-items: start;
  margin-bottom: 18px;
  min-width: 0;
}

.report-log-modal__eyebrow {
  margin: 0 0 6px;
  color: var(--primary-red);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.report-log-modal__title {
  margin: 0;
  color: var(--text-primary);
  font-size: 24px;
  line-height: 1.18;
  font-weight: 800;
  letter-spacing: -0.4px;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.report-log-modal__subtitle {
  margin: 8px 0 0;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}

.report-log-modal__close {
  width: 36px;
  height: 36px;
  border: 1px solid var(--glass-border);
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-primary);
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  transition: var(--transition-fast);
}

.report-log-modal__close:hover {
  background: rgba(227, 66, 52, 0.1);
  border-color: rgba(227, 66, 52, 0.24);
  color: var(--primary-red);
}

.report-log-modal__empty {
  padding: 18px;
  border-radius: var(--radius-md);
  border: 1px dashed var(--glass-border);
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}

.report-log-modal__list {
  display: grid;
  gap: 14px;
  max-height: min(60vh, 520px);
  overflow: auto;
  padding-right: 4px;
}

.report-log-modal__item {
  min-width: 0;
  border-radius: 16px;
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.12);
  padding: 16px;
}

.report-log-modal__reporter {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr);
  gap: 12px;
  align-items: center;
  min-width: 0;
}

.report-log-modal__avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  border: 1px solid rgba(227, 66, 52, 0.18);
  background: rgba(227, 66, 52, 0.1);
  color: var(--primary-red);
  font-size: 14px;
  font-weight: 800;
}

.report-log-modal__meta {
  min-width: 0;
}

.report-log-modal__name-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
  min-width: 0;
}

.report-log-modal__name {
  min-width: 0;
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.4;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.report-log-modal__date {
  flex-shrink: 0;
  color: var(--text-muted);
  font-size: 12px;
  line-height: 1.4;
}

.report-log-modal__email {
  margin: 3px 0 0;
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.4;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.report-log-modal__reason {
  margin-top: 14px;
  min-width: 0;
}

.report-log-modal__label {
  display: block;
  margin-bottom: 6px;
  color: var(--primary-cyan);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.report-log-modal__reason p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.7;
  white-space: pre-line;
  overflow-wrap: anywhere;
  word-break: break-word;
}

@media (max-width: 560px) {
  .report-log-modal {
    padding: 18px;
  }

  .report-log-modal__panel {
    padding: 22px;
  }

  .report-log-modal__name-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 3px;
  }

  .report-log-modal__date {
    flex-shrink: 1;
  }
}
</style>