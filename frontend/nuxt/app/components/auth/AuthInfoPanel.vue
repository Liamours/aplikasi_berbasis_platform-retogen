<template>
  <section class="auth-info-panel">
    <NuxtLink to="/" class="brand" aria-label="RetoGen home">
      <img src="/logo.png" alt="RetoGen logo" class="brand__logo" />
      <div class="brand__text">
        <span class="brand__eyebrow">RetoGen</span>
        <strong class="brand__name">Electronics Review Platform</strong>
      </div>
    </NuxtLink>

    <div class="auth-info-panel__content">
      <div class="badge-row">
        <span class="badge-chip badge-chip--cyan">Verified reviews</span>
        <span class="badge-chip badge-chip--red">Community insight</span>
      </div>

      <h3 class="auth-info-panel__title">
        Masuk untuk lanjut mengikuti update yang relevan terkait barang elektronik.
      </h3>

      <p class="auth-info-panel__description">
        Review elektronik yang lebih rapi, diskusi yang lebih jelas, dan akses yang siap berkembang ke artikel, notifikasi tag, serta pengalaman user yang konsisten.
      </p>

      <div class="feature-list">
        <article class="feature-item">
          <div class="feature-item__icon feature-item__icon--cyan" />
          <div>
            <h2>Review lebih terstruktur</h2>
            <p>Konten, rating, dan komentar ditata untuk cepat dipahami.</p>
          </div>
        </article>

        <article class="feature-item">
          <div class="feature-item__icon feature-item__icon--red" />
          <div>
            <h2>Diskusi lebih fokus</h2>
            <p>Interaksi komunitas terasa ringkas, jelas, dan relevan.</p>
          </div>
        </article>

        <article class="feature-item">
          <div class="feature-item__icon feature-item__icon--mix" />
          <div>
            <h2>Siap untuk notifikasi tag</h2>
            <p>Dibangun untuk alur login hingga personal update berikutnya.</p>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.auth-info-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 32px;
  min-height: 100%;
  padding: 28px;
  border-radius: 28px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.18));
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  box-shadow: var(--glass-shadow);
  overflow: hidden;
}

.auth-info-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  padding: 1px;
  border-radius: 28px;
  background: linear-gradient(135deg, var(--glass-edge), transparent 55%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}

.auth-info-panel::after {
  content: '';
  position: absolute;
  inset: 0 0 auto 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-red), var(--primary-cyan));
}

.brand {
  position: relative;
  z-index: 1;
  display: inline-flex;
  align-items: center;
  gap: 14px;
  width: fit-content;
  text-decoration: none;
  color: var(--text-primary);
}

.brand__logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 14px;
  padding: 6px;
  background: rgba(255, 255, 255, 0.36);
  border: 1px solid rgba(255, 255, 255, 0.38);
}

.brand__text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand__eyebrow {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.brand__name {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.2;
}

.auth-info-panel__content {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 24px;
}

.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.badge-chip {
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 14px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.03em;
  border: 1px solid transparent;
}

.badge-chip--cyan {
  color: var(--primary-cyan);
  background: rgba(0, 188, 212, 0.1);
  border-color: rgba(0, 188, 212, 0.18);
}

.badge-chip--red {
  color: var(--primary-red);
  background: rgba(227, 66, 52, 0.1);
  border-color: rgba(227, 66, 52, 0.18);
}

.auth-info-panel__title {
  max-width: 20ch;
  margin: 0;
  font-size: clamp(2.2rem, 4vw, 3.5rem);
  line-height: 1.08;
  letter-spacing: -0.04em;
  font-weight: 800;
  color: var(--text-primary);
}

.auth-info-panel__description {
  max-width: 56ch;
  margin: 0;
  font-size: 15px;
  line-height: 1.7;
  color: var(--text-secondary);
}

.feature-list {
  display: grid;
  gap: 12px;
}

.feature-item {
  display: grid;
  grid-template-columns: 14px 1fr;
  gap: 14px;
  align-items: start;
  padding: 16px 18px;
  border-radius: 18px;
  background: rgba(100, 100, 100, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.14);
  transition: transform 0.25s ease, border-color 0.25s ease, background 0.25s ease;
}

.feature-item:hover {
  transform: translateX(4px);
  border-color: rgba(255, 255, 255, 0.24);
  background: rgba(100, 100, 100, 0.06);
}

.feature-item__icon {
  width: 14px;
  height: 14px;
  border-radius: 999px;
  margin-top: 6px;
  box-shadow: 0 0 0 6px rgba(255, 255, 255, 0.04);
}

.feature-item__icon--cyan {
  background: var(--primary-cyan);
}

.feature-item__icon--red {
  background: var(--primary-red);
}

.feature-item__icon--mix {
  background: linear-gradient(135deg, var(--primary-red), var(--primary-cyan));
}

.feature-item h2 {
  margin: 0 0 4px;
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}

.feature-item p {
  margin: 0;
  font-size: 13px;
  line-height: 1.6;
  color: var(--text-secondary);
}

@media (max-width: 1024px) {
  .auth-info-panel__title {
    max-width: none;
  }
}

@media (max-width: 850px) {
  .auth-info-panel {
    padding: 24px;
  }

  .auth-info-panel__title {
    font-size: clamp(2rem, 7vw, 2.75rem);
  }
}

@media (max-width: 480px) {
  .auth-info-panel {
    padding: 20px;
    border-radius: 24px;
  }

  .brand__logo {
    width: 42px;
    height: 42px;
  }

  .feature-item {
    padding: 14px 16px;
  }
}
</style>