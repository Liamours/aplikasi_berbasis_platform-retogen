<script setup lang="ts">
import type { ReportUserTarget } from '~/composables/useReportUser'

defineProps<{
  open: boolean
  target: ReportUserTarget | null
  description: string
  commentPreview: string
  isSubmitting: boolean
  canSubmit: boolean
  errorMessage: string
}>()

const emit = defineEmits<{
  close: []
  submit: []
  'update:description': [value: string]
}>()
</script>

<template>
  <Teleport to="body">
    <Transition name="glass-modal">
      <div v-if="open" class="report-user-modal">
        <button
          type="button"
          class="report-user-modal__overlay"
          aria-label="Tutup report user"
          @click="emit('close')"
        />

        <section
          class="report-user-modal__panel"
          role="dialog"
          aria-modal="true"
          aria-label="Report user"
        >
          <div class="report-user-modal__header">
            <div class="report-user-modal__icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none">
                <path
                  d="M12 9v4M12 17h.01M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>

            <div>
              <h2>Laporkan {{ target?.username || 'user' }}</h2>
            </div>

            <button
              type="button"
              class="report-user-modal__close"
              aria-label="Tutup"
              @click="emit('close')"
            >
              ×
            </button>
          </div>

          <div class="report-user-modal__comment">
            <span>Komentar</span>
            <p>{{ commentPreview || '-' }}</p>
          </div>

          <label class="report-user-modal__field">
            <span>Alasan report</span>
            <textarea
              :value="description"
              rows="5"
              placeholder="Jelaskan alasan report secara singkat..."
              @input="emit('update:description', ($event.target as HTMLTextAreaElement).value)"
            />
          </label>

          <Transition name="glass-fade">
            <p v-if="errorMessage" class="report-user-modal__error">
              {{ errorMessage }}
            </p>
          </Transition>

          <div class="report-user-modal__actions">
            <BaseButton
              variant="ghost"
              :disabled="isSubmitting"
              @click="emit('close')"
            >
              Batal
            </BaseButton>

            <BaseButton
              variant="destructive"
              :disabled="!canSubmit"
              @click="emit('submit')"
            >
              {{ isSubmitting ? 'Mengirim...' : 'Kirim report' }}
            </BaseButton>
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.report-user-modal {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: grid;
  place-items: center;
  padding: 20px;
}

.report-user-modal__overlay {
  position: absolute;
  inset: 0;
  border: none;
  background: rgba(0, 0, 0, 0.48);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  cursor: pointer;
}

.report-user-modal__panel {
  position: relative;
  width: min(100%, 460px);
  padding: 28px;
  border-radius: var(--radius-lg);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
}

.report-user-modal__header {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr) 32px;
  gap: 12px;
  align-items: start;
  margin-bottom: 18px;
}

.report-user-modal__icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: grid;
  place-items: center;
  background: rgba(227, 66, 52, 0.1);
  color: var(--primary-red);
  border: 1px solid rgba(227, 66, 52, 0.24);
}

.report-user-modal__icon svg {
  width: 22px;
  height: 22px;
}

.report-user-modal__eyebrow {
  margin: 0 0 4px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.report-user-modal__header h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 22px;
  line-height: 1.2;
  font-weight: 800;
  word-break: break-word;
}

.report-user-modal__close {
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
}

.report-user-modal__comment {
  padding: 14px;
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.1);
  margin-bottom: 14px;
}

.report-user-modal__comment span,
.report-user-modal__field span {
  display: block;
  margin-bottom: 8px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.report-user-modal__comment p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.65;
}

.report-user-modal__field {
  display: block;
}

.report-user-modal__field textarea {
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

.report-user-modal__field textarea:focus {
  border-color: rgba(227, 66, 52, 0.36);
  box-shadow: 0 0 0 3px rgba(227, 66, 52, 0.08);
}

.report-user-modal__error {
  margin: 12px 0 0;
  padding: 11px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(227, 66, 52, 0.28);
  background: rgba(227, 66, 52, 0.08);
  color: var(--primary-red);
  font-size: 13px;
  line-height: 1.5;
}

.report-user-modal__actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 18px;
}

@media (max-width: 520px) {
  .report-user-modal__panel {
    padding: 22px;
  }

  .report-user-modal__header {
    grid-template-columns: 40px minmax(0, 1fr) 28px;
  }

  .report-user-modal__actions {
    flex-direction: column;
  }

  .report-user-modal__actions :deep(.base-button) {
    width: 100%;
  }
}
</style>