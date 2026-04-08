<script setup lang="ts">
const techChips = ['Laptop', 'Smartphone', 'Audio', 'Display']
</script>

<template>
  <section class="hero">
    <div class="hero__content">
      <div class="hero__copy">
        <div class="hero__brand">
          <img src="/logo.jpg" alt="RetoGen logo" class="hero__logo">
          <span class="hero__brand-name">RetoGen</span>
        </div>

        <h1 class="page-title">
          Review elektronik yang lebih tenang untuk dibaca.
        </h1>

        <p class="hero__description">
          Temukan ulasan, insight komunitas, dan pantauan harga dalam satu tempat.
        </p>

        <div class="hero__actions">
          <NuxtLink to="/login">
            <BaseButton variant="primary">Mulai Jelajahi</BaseButton>
          </NuxtLink>
          <BaseButton variant="ghost">Lihat Artikel</BaseButton>
        </div>
      </div>

      <div class="hero__visual">
        <BaseGlassCard class="hero-device">
          <div class="hero-device__top">
            <span class="hero-device__dot" />
            <span class="hero-device__dot" />
            <span class="hero-device__dot" />
          </div>

          <div class="hero-device__screen">
            <div class="hero-device__screen-glow" />

            <div class="hero-device__spec">
              <span class="hero-device__spec-label">Category</span>
              <strong class="hero-device__spec-value">Electronics Review</strong>
            </div>

            <div class="hero-device__bars">
              <span class="hero-device__bar hero-device__bar--lg" />
              <span class="hero-device__bar hero-device__bar--md" />
              <span class="hero-device__bar hero-device__bar--sm" />
            </div>

            <div class="hero-device__chips">
              <span v-for="chip in techChips" :key="chip" class="hero-device__chip">
                {{ chip }}
              </span>
            </div>
          </div>
        </BaseGlassCard>

        <BaseGlassCard variant="ghost" class="hero-float hero-float--price">
          <p class="hero-float__label">Price Watch</p>
          <strong class="hero-float__value">Real-time</strong>
        </BaseGlassCard>

        <BaseGlassCard variant="ghost" class="hero-float hero-float--rating">
          <p class="hero-float__label">Community</p>
          <strong class="hero-float__value">Rating & Comment</strong>
        </BaseGlassCard>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding: 28px 0 12px;
}

.hero__content {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
  gap: 24px;
  align-items: center;
  min-height: calc(100vh - 140px);
}

.hero__copy {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 20px;
}

.hero__brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
}

.hero__logo {
  width: 52px;
  height: 52px;
  object-fit: cover;
  border-radius: 16px;
  border: 1px solid var(--glass-border);
  box-shadow: var(--glass-shadow);
}

.hero__brand-name {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.hero__description {
  max-width: 620px;
  margin: 0;
  font-size: 18px;
  line-height: 1.6;
  color: var(--text-secondary);
}

.hero__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.hero__visual {
  position: relative;
  min-height: 460px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-device {
  width: min(100%, 420px);
  padding: 24px;
}

.hero-device__top {
  display: flex;
  gap: 8px;
  margin-bottom: 18px;
}

.hero-device__dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.5);
}

.hero-device__screen {
  position: relative;
  min-height: 280px;
  border-radius: 18px;
  padding: 22px;
  background:
    linear-gradient(135deg, rgba(227,66,52,0.1), rgba(0,206,209,0.08)),
    rgba(255,255,255,0.06);
  border: 1px solid var(--glass-border);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 18px;
}

.hero-device__screen-glow {
  position: absolute;
  inset: auto -40px -60px auto;
  width: 180px;
  height: 180px;
  border-radius: 999px;
  background: rgba(0, 206, 209, 0.16);
  filter: blur(60px);
  pointer-events: none;
}

.hero-device__spec {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.hero-device__spec-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.hero-device__spec-value {
  font-size: 26px;
  line-height: 1.2;
  font-weight: 700;
  color: var(--text-primary);
}

.hero-device__bars {
  position: relative;
  z-index: 1;
  display: grid;
  gap: 10px;
}

.hero-device__bar {
  display: block;
  height: 12px;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(227,66,52,0.78), rgba(0,206,209,0.78));
}

.hero-device__bar--lg { width: 100%; }
.hero-device__bar--md { width: 76%; }
.hero-device__bar--sm { width: 48%; }

.hero-device__chips {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.hero-device__chip {
  padding: 8px 14px;
  border-radius: 20px;
  background: rgba(255,255,255,0.08);
  border: 1px solid var(--glass-border);
  color: var(--text-primary);
  font-size: 12px;
  font-weight: 600;
}

.hero-float {
  position: absolute;
  padding: 16px 18px;
  min-width: 160px;
  box-shadow: none;
}

.hero-float--price { top: 26px; right: 0; }
.hero-float--rating { bottom: 34px; left: 0; }

.hero-float__label {
  margin: 0 0 6px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.hero-float__value {
  font-size: 16px;
  line-height: 1.3;
  color: var(--text-primary);
}

@media (max-width: 1024px) {
  .hero__content {
    grid-template-columns: 1fr;
  }

  .hero__visual {
    min-height: auto;
    padding-top: 10px;
    display: grid;
    gap: 16px;
  }

  .hero-device {
    width: 100%;
  }

  .hero-float--price,
  .hero-float--rating {
    position: static;
  }
}

@media (max-width: 480px) {
  .hero__description { font-size: 16px; }

  .hero__actions {
    width: 100%;
    flex-direction: column;
  }

  .hero__actions :deep(.base-button) {
    width: 100%;
  }

  .hero-device__spec-value { font-size: 22px; }
}
</style>
