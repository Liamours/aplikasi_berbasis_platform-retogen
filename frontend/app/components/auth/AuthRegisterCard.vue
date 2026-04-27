<script setup lang="ts">
const {
  form,
  errors,
  isSubmitting,
  isSuccess,
  successMessage,
  handleCloseSuccess,
  handleSubmit
} = useRegisterForm()
</script>

<template>
  <BaseGlassCard class="register-card">
    <div class="register-card__header">
      <div class="register-card__brand">
        <img src="/logo.jpg" alt="RetoGen logo" class="register-card__logo">
        <span class="register-card__brand-text">RetoGen</span>
      </div>

      <div class="register-card__title-wrap">
        <h1 class="card-title">Buat akun baru</h1>
      </div>
    </div>

    <form class="register-form" @submit.prevent="handleSubmit">
      <Transition name="glass-fade">
        <div v-if="errors.general" class="error-banner">{{ errors.general }}</div>
      </Transition>

      <BaseInput
        v-model="form.username"
        label="Username"
        type="text"
        placeholder="8-16 karakter, huruf dan angka"
        :error="errors.username"
      />

      <BaseInput
        v-model="form.fullname"
        label="Full name"
        type="text"
        placeholder="Nama lengkap"
        :error="errors.fullname"
      />

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
        placeholder="8-16 karakter, kombinasi huruf besar, kecil, dan angka"
        :error="errors.password"
      />

      <BaseButton type="submit" variant="primary" block :disabled="isSubmitting || isSuccess">
        {{ isSubmitting ? 'Memproses...' : 'Daftar' }}
      </BaseButton>
    </form>

    <div class="register-card__footer">
      <p class="register-card__footer-text">
        Sudah punya akun?
        <NuxtLink to="/login" class="register-card__footer-link">Masuk</NuxtLink>
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
.register-card {
  width: 100%;
  max-width: var(--auth-max);
  margin: 0 auto;
  padding: 32px;
}

.register-card__header {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 28px;
}

.register-card__brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  align-self: flex-start;
}

.register-card__logo {
  width: 44px;
  height: 44px;
  object-fit: cover;
  border-radius: 14px;
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
}

.register-card__brand-text {
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.register-card__title-wrap {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.register-card__eyebrow {
  margin: 0;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--primary-cyan);
}

.register-card__description {
  margin: 0;
  color: var(--text-secondary);
  line-height: 1.6;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.register-card__footer {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px solid var(--glass-border);
}

.register-card__footer-text {
  margin: 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.register-card__footer-link {
  color: var(--primary-cyan);
  font-weight: 700;
  transition: var(--transition-fast);
}

.register-card__footer-link:hover {
  opacity: 0.9;
}

@media (max-width: 480px) {
  .register-card {
    padding: 24px 20px;
  }
}
</style>