<script setup lang="ts">
const props = defineProps<{
  mode: 'create' | 'edit'
  articleId?: string
}>()

const {
  form,
  tagsInput,
  previewImage,
  imageFileName,
  formError,
  formSuccess,
  isSubmitting,
  isEditMode,
  normalizedTags,
  titleLength,
  previewLength,
  tagCount,
  hasInvalidTagLength,
  TITLE_MAX_LENGTH,
  PREVIEW_MAX_LENGTH,
  TAG_MAX_COUNT,
  TAG_MAX_LENGTH,
  loadForm,
  handleImageChange,
  submitForm,
  cancelForm
} = useArticleForm()

watch(
  () => [props.mode, props.articleId],
  () => {
    loadForm(props.mode, props.articleId)
  },
  { immediate: true }
)

const pageTitle = computed(() => {
  return isEditMode.value ? 'Edit artikel' : 'Buat artikel'
})

const pageSubtitle = computed(() => {
  return isEditMode.value
    ? 'Perbarui konten review elektronik dengan informasi terbaru.'
    : 'Tulis review elektronik yang ringkas, jelas, dan mudah dipahami.'
})

const submitLabel = computed(() => {
  if (isSubmitting.value) return 'Menyimpan...'
  return isEditMode.value ? 'Simpan perubahan' : 'Terbitkan artikel'
})

const isTitleInvalid = computed(() => titleLength.value > TITLE_MAX_LENGTH)
const isPreviewInvalid = computed(() => previewLength.value > PREVIEW_MAX_LENGTH)
const isTagCountInvalid = computed(() => tagCount.value > TAG_MAX_COUNT)
const isTagsInvalid = computed(() => isTagCountInvalid.value || hasInvalidTagLength.value)
</script>

<template>
  <section class="article-form">
    <div class="article-form__header">
      <div>
        <p class="article-form__eyebrow">Admin article</p>
        <h1 class="article-form__title">{{ pageTitle }}</h1>
        <p class="article-form__subtitle">{{ pageSubtitle }}</p>
      </div>

      <button type="button" class="article-form__back" @click="cancelForm">
        Batal
      </button>
    </div>

    <div v-if="formError" class="article-form__alert article-form__alert--error">
      {{ formError }}
    </div>

    <div v-if="formSuccess" class="article-form__alert article-form__alert--success">
      {{ formSuccess }}
    </div>

    <div class="article-form__grid">
      <div class="article-form__main">
        <label class="article-form__field">
          <span>Judul artikel</span>
          <input
            v-model="form.article_title"
            class="article-form__input"
            :class="{ 'is-invalid': isTitleInvalid }"
            type="text"
            placeholder="Contoh: Sony WH-1000XM5"
          >
          <small :class="{ 'is-danger': isTitleInvalid }">
            {{ titleLength }}/{{ TITLE_MAX_LENGTH }} karakter
          </small>
        </label>

        <label class="article-form__field">
          <span>Preview singkat</span>
          <textarea
            v-model="form.article_preview"
            class="article-form__textarea article-form__textarea--preview"
            :class="{ 'is-invalid': isPreviewInvalid }"
            rows="3"
            placeholder="Ringkasan singkat yang muncul di kartu artikel."
          />
          <small :class="{ 'is-danger': isPreviewInvalid }">
            {{ previewLength }}/{{ PREVIEW_MAX_LENGTH }} karakter
          </small>
        </label>

        <label class="article-form__field">
          <span>Review lengkap</span>
          <textarea
            v-model="form.article_content"
            class="article-form__textarea"
            rows="13"
            placeholder="Tulis review lengkap, pengalaman penggunaan, kelebihan, kekurangan, dan rekomendasi."
          />
        </label>

        <label class="article-form__field">
          <span>Tag</span>
          <input
            v-model="tagsInput"
            class="article-form__input"
            :class="{ 'is-invalid': isTagsInvalid }"
            type="text"
            placeholder="audio, headphone, wireless"
          >
          <small :class="{ 'is-danger': isTagsInvalid }">
            {{ tagCount }}/{{ TAG_MAX_COUNT }} tag, maksimal {{ TAG_MAX_LENGTH }} karakter per tag.
          </small>

          <div v-if="normalizedTags.length" class="article-form__tag-preview">
            <span
              v-for="tag in normalizedTags"
              :key="tag"
              class="article-form__tag"
              :class="{ 'is-invalid': tag.length > TAG_MAX_LENGTH }"
            >
              {{ tag }}
            </span>
          </div>
        </label>
      </div>

      <aside class="article-form__side">
        <div class="article-form__image-card">
          <span class="article-form__image-label">Gambar produk</span>

          <div class="article-form__image-preview">
            <img
              v-if="previewImage"
              :src="previewImage"
              alt="Preview gambar artikel"
            >
            <span v-else>Preview gambar</span>
          </div>

          <label class="article-form__upload">
            <input
              type="file"
              accept="image/png,image/jpeg"
              @change="handleImageChange"
            >
            <span>Pilih gambar</span>
          </label>

          <p class="article-form__file-name">
            {{ imageFileName || 'PNG atau JPEG' }}
          </p>
        </div>

        <div class="article-form__note">
          <h2>Catatan</h2>
          <p>
            Pastikan review fokus pada produk, mudah dibaca, dan tidak terlalu panjang.
            Tags akan disimpan sebagai daftar kategori.
          </p>
        </div>
      </aside>
    </div>

    <div class="article-form__actions">
      <button
        type="button"
        class="article-form__button article-form__button--ghost"
        @click="cancelForm"
      >
        Batal
      </button>

      <button
        type="button"
        class="article-form__button article-form__button--primary"
        :disabled="isSubmitting"
        @click="submitForm"
      >
        {{ submitLabel }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.article-form {
  width: min(100%, 1080px);
  margin: 0 auto;
  min-width: 0;
}

.article-form__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
  margin-bottom: 24px;
  min-width: 0;
}

.article-form__eyebrow {
  color: var(--text-muted);
  font-size: 12px;
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.article-form__title {
  color: var(--text-primary);
  font-size: clamp(30px, 4vw, 42px);
  line-height: 1.08;
  font-weight: 800;
  letter-spacing: -1px;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.article-form__subtitle {
  max-width: 62ch;
  margin-top: 10px;
  color: var(--text-secondary);
  font-size: 15px;
  line-height: 1.7;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.article-form__back {
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-primary);
  border-radius: 12px;
  padding: 10px 14px;
  font: inherit;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition-fast);
  flex-shrink: 0;
}

.article-form__back:hover {
  background: rgba(106, 173, 168, 0.1);
  border-color: rgba(106, 173, 168, 0.24);
}

.article-form__alert {
  margin-bottom: 16px;
  padding: 12px 14px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.article-form__alert--error {
  color: var(--primary-red);
  background: rgba(181, 107, 82, 0.1);
  border: 1px solid rgba(181, 107, 82, 0.22);
}

.article-form__alert--success {
  color: var(--primary-cyan);
  background: rgba(106, 173, 168, 0.1);
  border: 1px solid rgba(106, 173, 168, 0.22);
}

.article-form__grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;
  gap: 22px;
  align-items: start;
  min-width: 0;
}

.article-form__main,
.article-form__side {
  display: grid;
  gap: 16px;
  min-width: 0;
}

.article-form__field,
.article-form__image-card,
.article-form__note {
  min-width: 0;
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.14);
  padding: 18px;
}

.article-form__field {
  display: grid;
  gap: 10px;
}

.article-form__field span,
.article-form__image-label,
.article-form__note h2 {
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 700;
}

.article-form__field small {
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.5;
}

.article-form__field small.is-danger {
  color: var(--primary-red);
  font-weight: 600;
}

.article-form__input,
.article-form__textarea {
  width: 100%;
  min-width: 0;
  border-radius: 14px;
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
  padding: 14px;
  outline: none;
  font: inherit;
  line-height: 1.65;
  overflow-wrap: anywhere;
  word-break: break-word;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.article-form__textarea {
  resize: vertical;
  min-height: 320px;
}

.article-form__textarea--preview {
  min-height: 92px;
}

.article-form__input:focus,
.article-form__textarea:focus {
  border-color: rgba(106, 173, 168, 0.34);
}

.article-form__input.is-invalid,
.article-form__textarea.is-invalid {
  border-color: rgba(181, 107, 82, 0.42);
}

.article-form__tag-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  min-width: 0;
}

.article-form__tag {
  max-width: 100%;
  padding: 5px 9px;
  border-radius: var(--radius-sm);
  background: rgba(181, 107, 82, 0.1);
  color: var(--primary-red);
  font-size: 12px;
  font-weight: 600;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.article-form__tag.is-invalid {
  border: 1px solid rgba(181, 107, 82, 0.36);
}

.article-form__image-card {
  display: grid;
  gap: 12px;
}

.article-form__image-preview {
  min-height: 220px;
  border-radius: 16px;
  border: 1px dashed var(--glass-border);
  background: var(--bg-surface);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  color: var(--text-secondary);
  font-size: 13px;
}

.article-form__image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-form__upload {
  position: relative;
  display: inline-flex;
  justify-content: center;
  border-radius: 12px;
  border: 1px solid rgba(106, 173, 168, 0.24);
  background: rgba(106, 173, 168, 0.08);
  color: var(--primary-cyan);
  padding: 11px 14px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 700;
  transition: var(--transition-fast);
}

.article-form__upload:hover {
  background: rgba(106, 173, 168, 0.14);
}

.article-form__upload input {
  position: absolute;
  inset: 0;
  opacity: 0;
  cursor: pointer;
}

.article-form__file-name {
  color: var(--text-secondary);
  font-size: 12px;
  line-height: 1.5;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.article-form__note h2 {
  margin-bottom: 8px;
}

.article-form__note p {
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.7;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.article-form__actions {
  margin-top: 22px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.article-form__button {
  border: none;
  border-radius: 12px;
  padding: 12px 18px;
  font: inherit;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: var(--transition-fast);
}

.article-form__button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.article-form__button--ghost {
  border: 1px solid var(--glass-border);
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-primary);
}

.article-form__button--ghost:hover {
  background: rgba(255, 255, 255, 0.14);
}

.article-form__button--primary {
  background: var(--primary-cyan);
  color: white;
}

.article-form__button--primary:hover:not(:disabled) {
  transform: translateY(-1px);
  background: var(--primary-cyan);
}

@media (max-width: 900px) {
  .article-form__grid {
    grid-template-columns: 1fr;
  }

  .article-form__side {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .article-form__header {
    flex-direction: column;
  }

  .article-form__back {
    width: 100%;
  }

  .article-form__actions {
    flex-direction: column-reverse;
  }

  .article-form__button {
    width: 100%;
  }
}
</style>