<script setup lang="ts">
const {
  deleteArticleState,
  closeDeleteArticle,
  confirmDeleteArticle
} = useArticleDetail()

const isOpen = computed(() => deleteArticleState.value.open)

const articleTitle = computed(() => {
  return deleteArticleState.value.title || 'artikel ini'
})
</script>

<template>
  <Teleport to="body">
    <Transition name="glass-modal">
      <div
        v-if="isOpen"
        class="delete-article-modal"
        @click.self="closeDeleteArticle"
      >
        <section class="delete-article-modal__panel" role="dialog" aria-modal="true">
          <p class="delete-article-modal__eyebrow">Konfirmasi</p>

          <h2 class="delete-article-modal__title">
            Hapus artikel?
          </h2>

          <p class="delete-article-modal__description">
            Artikel <strong>{{ articleTitle }}</strong> akan dihapus. Setelah konfirmasi,
            Anda akan kembali ke halaman utama.
          </p>

          <div class="delete-article-modal__actions">
            <button
              type="button"
              class="delete-article-modal__button delete-article-modal__button--ghost"
              @click="closeDeleteArticle"
            >
              Batal
            </button>

            <button
              type="button"
              class="delete-article-modal__button delete-article-modal__button--danger"
              @click="confirmDeleteArticle"
            >
              Hapus artikel
            </button>
          </div>
        </section>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.delete-article-modal {
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

.delete-article-modal__panel {
  width: min(100%, 440px);
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.72);
  background: var(--bg-surface);
  box-shadow: 0 18px 50px rgba(0, 0, 0, 0.18);
  padding: 28px;
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
}

.delete-article-modal__eyebrow {
  margin-bottom: 6px;
  color: var(--primary-red);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.delete-article-modal__title {
  color: var(--text-primary);
  font-size: 24px;
  line-height: 1.15;
  font-weight: 700;
}

.delete-article-modal__description {
  margin-top: 12px;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.7;
}

.delete-article-modal__description strong {
  color: var(--text-primary);
}

.delete-article-modal__actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.delete-article-modal__button {
  border: none;
  border-radius: 12px;
  padding: 11px 16px;
  font: inherit;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition-fast);
}

.delete-article-modal__button--ghost {
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
}

.delete-article-modal__button--ghost:hover {
  background: rgba(255, 255, 255, 0.78);
}

.delete-article-modal__button--danger {
  background: var(--primary-red);
  color: white;
}

.delete-article-modal__button--danger:hover {
  transform: translateY(-1px);
  background: #c73629;
}

/* Variabel otomatis adaptif */

@media (max-width: 480px) {
  .delete-article-modal {
    align-items: flex-end;
    padding: 16px;
  }

  .delete-article-modal__panel {
    padding: 22px;
  }

  .delete-article-modal__actions {
    flex-direction: column-reverse;
  }

  .delete-article-modal__button {
    width: 100%;
  }
}
</style>