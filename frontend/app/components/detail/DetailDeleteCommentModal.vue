<script setup lang="ts">
const {
  deleteCommentState,
  closeDeleteComment,
  confirmDeleteComment
} = useArticleDetail()

const isOpen = computed(() => deleteCommentState.value.open)

const targetOwnerLabel = computed(() => {
  return deleteCommentState.value.targetOwner || 'pengguna ini'
})
</script>

<template>
  <Teleport to="body">
    <Transition name="glass-modal">
      <div
        v-if="isOpen"
        class="delete-modal"
        @click.self="closeDeleteComment"
      >
        <section class="delete-modal__panel" role="dialog" aria-modal="true">
          <div class="delete-modal__header">
            <p class="delete-modal__eyebrow">Konfirmasi</p>
            <h2 class="delete-modal__title">Hapus komentar?</h2>
          </div>

          <p class="delete-modal__description">
            Komentar dari {{ targetOwnerLabel }} akan dihapus dari diskusi.
            Balasan di bawah komentar ini juga akan ikut terhapus.
          </p>

          <div class="delete-modal__actions">
            <button
              type="button"
              class="delete-modal__button delete-modal__button--ghost"
              @click="closeDeleteComment"
            >
              Batal
            </button>

            <button
              type="button"
              class="delete-modal__button delete-modal__button--danger"
              @click="confirmDeleteComment"
            >
              Hapus komentar
            </button>
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.delete-modal {
  position: fixed;
  inset: 0;
  z-index: 99999;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.delete-modal__panel {
  width: min(100%, 420px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.72);
  background: var(--bg-surface);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.18);
  padding: 28px;
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
}

.delete-modal__eyebrow {
  margin-bottom: 6px;
  color: var(--primary-red);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.delete-modal__title {
  color: var(--text-primary);
  font-size: 24px;
  line-height: 1.15;
  font-weight: 700;
}

.delete-modal__description {
  margin-top: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.delete-modal__actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.delete-modal__button {
  border: none;
  border-radius: 12px;
  padding: 11px 16px;
  font: inherit;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition-fast);
}

.delete-modal__button--ghost {
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
}

.delete-modal__button--ghost:hover {
  background: rgba(255, 255, 255, 0.78);
}

.delete-modal__button--danger {
  background: var(--primary-red);
  color: white;
}

.delete-modal__button--danger:hover {
  transform: translateY(-1px);
  background: #c73629;
}

/* Di bawah ini sudah tidak diperlukan karena variabel otomatis adaptif */

@media (max-width: 480px) {
  .delete-modal {
    align-items: flex-end;
    padding: 16px;
  }

  .delete-modal__panel {
    padding: 22px;
  }

  .delete-modal__actions {
    flex-direction: column-reverse;
  }

  .delete-modal__button {
    width: 100%;
  }
}
</style>