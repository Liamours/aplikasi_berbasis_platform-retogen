<script setup lang="ts">
const { form, errors, isSubmitting, isSuccess, successMessage, handleCloseSuccess, handleSubmit } = useLoginForm()
</script>

<template>
  <BaseGlassCard class="login-card">
    <div class="login-card__header">
      <div class="login-card__brand">
        <img src="/logo.jpg" alt="RetoGen logo" class="login-card__logo">
        <span class="login-card__brand-text">RetoGen</span>
      </div>

      <div class="login-card__title-wrap">
        <h1 class="card-title">Masuk ke akun Anda</h1>
      </div>
    </div>

    <form class="login-form" @submit.prevent="handleSubmit">
      <Transition name="glass-fade">
        <div v-if="errors.general" class="error-banner">{{ errors.general }}</div>
      </Transition>

      <BaseInput
        v-model="form.email"
        label="Email"
        type="email"
        placeholder="nama@email.com"
        :error="errors.email"
      />

      <BaseInput
        v-model="form.password"
        label="Password"
        type="password"
        placeholder="Masukkan password"
        :error="errors.password"
      />

      <BaseButton type="submit" variant="primary" block :disabled="isSubmitting">
        {{ isSubmitting ? 'Memproses...' : 'Masuk' }}
      </BaseButton>
    </form>

    <div class="login-card__footer">
      <p class="login-card__footer-text">
        Belum punya akun?
        <NuxtLink to="/register" class="login-card__footer-link">Daftar</NuxtLink>
      </p>
    </div>
  </BaseGlassCard>

  <BaseSuccessPopup
    v-if="isSuccess"
    :message="successMessage"
    @close="handleCloseSuccess"
  />
</template>

<style scoped>
.login-card {
  width: 100%;
  max-width: var(--auth-max);
  margin: 0 auto;
  padding: 32px;
}

.login-card__header {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 28px;
}

.login-card__brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  align-self: flex-start;
}

.login-card__logo {
  width: 44px;
  height: 44px;
  object-fit: cover;
  border-radius: 14px;
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
}

.login-card__brand-text {
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.login-card__title-wrap {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.login-card__eyebrow {
  margin: 0;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--primary-cyan);
}

.login-card__description {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.6;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.login-card__footer {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px solid var(--glass-border);
}

.login-card__footer-text {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.login-card__footer-link {
  color: var(--primary-cyan);
  font-weight: 700;
  transition: var(--transition-fast);
}

.login-card__footer-link:hover {
  opacity: 0.9;
}

@media (max-width: 480px) {
  .login-card { padding: 24px 20px; }
}
</style>
