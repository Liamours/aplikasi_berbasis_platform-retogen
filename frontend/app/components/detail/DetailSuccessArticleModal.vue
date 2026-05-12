<script setup lang="ts">
const { showSuccessModal } = useArticleForm()
</script>

<template>
  <Teleport to="body">
    <Transition name="glass-modal">
      <div
        v-if="showSuccessModal"
        class="success-modal"
      >
        <section
          class="success-modal__panel"
          role="dialog"
          aria-modal="true"
        >
          <div class="success-modal__icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h2 class="success-modal__title">Berhasil!</h2>
          <p class="success-modal__description">Artikel Anda telah diterbitkan.</p>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.success-modal {
  position: fixed;
  inset: 0;
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.success-modal__panel {
  width: min(100%, 320px);
  border-radius: 20px;
  border: 1px solid var(--glass-border);
  background: var(--bg-surface);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.18);
  padding: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  animation: modal-pop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modal-pop {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.success-modal__icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(106, 173, 168, 0.1);
  color: var(--primary-cyan);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.success-modal__icon svg {
  width: 28px;
  height: 28px;
}

.success-modal__title {
  margin: 0;
  color: var(--text-primary);
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.4px;
}

.success-modal__description {
  margin: 8px 0 0;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.5;
}

/* Modal Transition */
.glass-modal-enter-active,
.glass-modal-leave-active {
  transition: opacity 0.3s ease;
}

.glass-modal-enter-from,
.glass-modal-leave-to {
  opacity: 0;
}
</style>
