<script setup lang="ts">
import type { PublicUserProfile } from '~/composables/useUserProfile'

const props = defineProps<{
  open: boolean
  profile: PublicUserProfile | null
  initials: string
  isLoading: boolean
  errorMessage: string
  formatDate: (value?: string) => string
}>()

const emit = defineEmits<{
  close: []
}>()

const username = computed(() => props.profile?.username || '-')
const memberSince = computed(() => props.formatDate(props.profile?.created_at))
</script>

<template>
  <Teleport to="body">
    <Transition name="glass-modal">
      <div v-if="open" class="other-profile">
        <button
          type="button"
          class="other-profile__overlay"
          aria-label="Tutup profil user"
          @click="emit('close')"
        />

        <section
          class="other-profile__panel"
          role="dialog"
          aria-modal="true"
          aria-label="Profil user"
        >
          <button
            type="button"
            class="other-profile__close"
            aria-label="Tutup"
            @click="emit('close')"
          >
            ×
          </button>

          <div class="other-profile__avatar">
            {{ isLoading ? 'R' : initials }}
          </div>

          <div v-if="isLoading" class="other-profile__content">
            <p class="other-profile__eyebrow">Member</p>
            <h2>Memuat profil...</h2>
            <p>Mohon tunggu sebentar.</p>
          </div>

          <div v-else-if="errorMessage" class="other-profile__content">
            <p class="other-profile__eyebrow">Member</p>
            <h2>Profil tidak tersedia</h2>
            <p>{{ errorMessage }}</p>
          </div>

          <div v-else class="other-profile__content">
            <p class="other-profile__eyebrow">Member</p>
            <h2>{{ username }}</h2>
            <p>Member since {{ memberSince }}</p>

            <div v-if="profile?.reports && profile.reports.length > 0" class="reports-section">
              <h3 class="reports-title">Reports ({{ profile.reports.length }})</h3>
              <div class="reports-list">
                <div v-for="report in profile.reports" :key="report.report_id" class="report-item">
                  <div class="report-header">
                    <span class="report-date">{{ formatDate(report.created_at) }}</span>
                  </div>
                  <p class="report-description">{{ report.description }}</p>
                </div>
              </div>
            </div>
            <div v-else-if="!isLoading && !errorMessage" class="reports-empty">
              Tidak ada report untuk user ini.
            </div>
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.other-profile {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: grid;
  place-items: center;
  padding: 20px;
}

.other-profile__overlay {
  position: absolute;
  inset: 0;
  border: none;
  background: rgba(0, 0, 0, 0.48);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  cursor: pointer;
}

.other-profile__panel {
  position: relative;
  width: min(100%, 360px);
  padding: 32px;
  border-radius: var(--radius-lg);
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  text-align: center;
}

.other-profile__close {
  position: absolute;
  top: 14px;
  right: 16px;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
}

.other-profile__avatar {
  width: 72px;
  height: 72px;
  margin: 0 auto 18px;
  border-radius: var(--radius-md);
  display: grid;
  place-items: center;
  background: rgba(106, 173, 168, 0.14);
  border: 1px solid var(--glass-border);
  color: var(--primary-cyan);
  font-size: 28px;
  font-weight: 800;
}

.other-profile__content {
  display: grid;
  gap: 6px;
}

.other-profile__eyebrow {
  margin: 0;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.other-profile__content h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: 24px;
  line-height: 1.2;
  font-weight: 800;
  word-break: break-word;
}

.other-profile__content p {
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.reports-section {
  margin-top: 24px;
  text-align: left;
  border-top: 1px solid var(--glass-border);
  padding-top: 20px;
}

.reports-title {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 300px;
  overflow-y: auto;
  padding-right: 4px;
}

.reports-list::-webkit-scrollbar {
  width: 4px;
}

.reports-list::-webkit-scrollbar-thumb {
  background: var(--glass-border);
  border-radius: 10px;
}

.report-item {
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-md);
}

.report-header {
  margin-bottom: 6px;
}

.report-date {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 600;
}

.report-description {
  font-size: 13px !important;
  color: var(--text-secondary) !important;
  line-height: 1.5 !important;
  white-space: pre-wrap;
}

.reports-empty {
  margin-top: 20px;
  font-size: 13px;
  color: var(--text-muted);
  font-style: italic;
}

@media (max-width: 480px) {
  .other-profile__panel {
    padding: 28px 22px;
  }
}
</style>