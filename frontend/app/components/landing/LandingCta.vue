<template>
  <section class="cta">
    <BaseGlassCard class="cta__card">
      <div class="cta__content">
        <div>
          <p class="cta__label">Get started</p>
          <h2 class="cta__title">Cari, bandingkan, dan pantau harga produk elektronik dengan mudah.</h2>
        </div>

        <NuxtLink to="/login">
          <BaseButton variant="primary">Mulai Sekarang</BaseButton>
        </NuxtLink>
      </div>
    </BaseGlassCard>
  </section>
</template>

<style scoped>
.cta {
  padding: 12px 0 8px;
}

.cta__card {
  padding-top: 40px;
  padding-bottom: 40px;
}

.cta__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}

.cta__label {
  margin: 0 0 8px;
  color: var(--primary-red);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.cta__title {
  max-width: 680px;
  margin: 0;
  font-size: clamp(28px, 4vw, 36px);
  line-height: 1.15;
  font-weight: 700;
  color: var(--text-primary);
}

@media (max-width: 1024px) {
  .cta__content {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 480px) {
  .cta__content {
    width: 100%;
  }

  .cta__content :deep(.base-button) {
    width: 100%;
  }
}
</style>
