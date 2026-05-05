<script setup lang="ts">
import type { OwnUserProfile } from '~/composables/useUserProfile'

const props = defineProps<{
  profile: OwnUserProfile | null
  initials: string
  isLoading: boolean
  errorMessage: string
  formatDate: (value?: string) => string
}>()

const emit = defineEmits<{
  logout: []
}>()

const username = computed(() => props.profile?.username || '-')
const fullname = computed(() => props.profile?.fullname || '-')
const email = computed(() => props.profile?.email || '-')
const memberSince = computed(() => props.formatDate(props.profile?.created_at))
</script>

<template>
  <BaseGlassCard variant="account" class="profile-card">
    <div class="profile-card__header">
      <div class="profile-card__avatar">
        {{ initials }}
      </div>

      <div class="profile-card__intro">
        <p class="profile-card__eyebrow">Profile Account</p>
        <h1>Profil akun</h1>
      </div>
    </div>

    <Transition name="glass-fade">
      <p v-if="errorMessage" class="profile-card__error">
        {{ errorMessage }}
      </p>
    </Transition>

    <div class="profile-card__content" aria-live="polite">
      <div class="profile-card__item">
        <span>Username</span>
        <strong>{{ isLoading ? 'Memuat...' : username }}</strong>
      </div>

      <div class="profile-card__item">
        <span>Fullname</span>
        <strong>{{ isLoading ? 'Memuat...' : fullname }}</strong>
      </div>

      <div class="profile-card__item">
        <span>Email</span>
        <strong>{{ isLoading ? 'Memuat...' : email }}</strong>
      </div>

      <div class="profile-card__item">
        <span>Member since</span>
        <strong>{{ isLoading ? 'Memuat...' : memberSince }}</strong>
      </div>
    </div>

    <div class="profile-card__actions">
        <BaseButton
            variant="ghost"
            @click="$router.back()"
        >
            ← Kembali
        </BaseButton>
        <BaseButton
            variant="destructive"
            :disabled="isLoading"
            @click="emit('logout')"
        >
            Logout
        </BaseButton>
    </div>
  </BaseGlassCard>
</template>

<style scoped>
.profile-card {
  width: min(100%, 560px);
}

.profile-card__header {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-bottom: 28px;
}

.profile-card__avatar {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-md);
  display: grid;
  place-items: center;
  background: rgba(106, 173, 168, 0.14);
  border: 1px solid var(--glass-border);
  color: var(--primary-cyan);
  font-size: 24px;
  font-weight: 800;
  flex-shrink: 0;
}

.profile-card__intro {
  min-width: 0;
}

.profile-card__eyebrow {
  margin: 0 0 4px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.profile-card__intro h1 {
  margin: 0;
  color: var(--text-primary);
  font-size: 28px;
  line-height: 1.15;
  font-weight: 800;
}

.profile-card__intro p {
  margin: 8px 0 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.6;
}

.profile-card__error {
  margin-bottom: 18px;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  border: 1px solid rgba(227, 66, 52, 0.28);
  background: rgba(227, 66, 52, 0.08);
  color: var(--primary-red);
  font-size: 13px;
  line-height: 1.5;
}

.profile-card__content {
  display: grid;
  gap: 10px;
}

.profile-card__item {
  padding: 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.1);
}

.profile-card__item span {
  display: block;
  margin-bottom: 6px;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.profile-card__item strong {
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 600;
  word-break: break-word;
}

.profile-card__actions {
  margin-top: 22px;
  display: flex;
  justify-content: space-between;
  gap: 16px;
}

@media (max-width: 520px) {
  .profile-card {
    padding: 28px;
  }

  .profile-card__header {
    align-items: flex-start;
    flex-direction: column;
  }

  .profile-card__intro h1 {
    font-size: 24px;
  }

  .profile-card__actions {
    justify-content: stretch;
    flex-direction: column-reverse;
  }

  .profile-card__actions :deep(.base-button) {
    width: 100%;
  }
}
</style>