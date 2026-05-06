<script setup lang="ts">
const { reportState, closeReport, submitReport } = useArticleDetail()
</script>

<template>
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
          <button type="button" class="report-modal__close" @click="closeReport">×</button>
        </div>

        <div v-if="reportState.type === 'comment' && reportState.targetName" class="report-modal__target">
          <div class="report-modal__target-user">
            <span class="report-modal__target-label">User:</span>
            <span class="report-modal__target-value">{{ reportState.targetName }}</span>
          </div>
          <div class="report-modal__target-comment">
            <span class="report-modal__target-label">Komentar:</span>
            <p class="report-modal__target-text">"{{ reportState.targetContent }}"</p>
          </div>
        </div>

        <textarea
          v-model="reportState.description"
          class="report-modal__textarea"
          rows="4"
          placeholder="Jelaskan alasan report secara singkat..."
        />

        <div class="report-modal__actions">
          <BaseButton variant="ghost" @click="closeReport">Batal</BaseButton>
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
</template>

<style scoped>
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
  border-radius: var(--radius-lg);
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

.report-modal__target {
  background: rgba(106, 173, 168, 0.08);
  border: 1px solid rgba(106, 173, 168, 0.15);
  border-radius: var(--radius-md);
  padding: 14px;
  margin-bottom: 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.report-modal__target-label {
  font-size: 11px;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.5px;
  color: var(--primary-cyan);
  display: block;
  margin-bottom: 2px;
}

.report-modal__target-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.report-modal__target-text {
  font-size: 13px;
  line-height: 1.5;
  color: var(--text-secondary);
  font-style: italic;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.report-modal__textarea {
  width: 100%;
  resize: vertical;
  min-height: 120px;
  border-radius: var(--radius-md);
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

.report-modal__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 16px;
}

@media (max-width: 640px) {
  .report-modal__panel {
    width: calc(100% - 24px);
    margin-top: 10vh;
    padding: 22px;
  }

  .report-modal__actions {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
