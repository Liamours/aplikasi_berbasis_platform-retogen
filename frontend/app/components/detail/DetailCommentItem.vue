<script setup lang="ts">
import type { DetailCommentTree } from '~/types/api'

defineOptions({
  name: 'DetailCommentItem'
})

const props = defineProps<{
  comment: DetailCommentTree
  activeReplyId: string | null
  replyDrafts: Record<string, string>
}>()

const emit = defineEmits<{
  openReport: [commentId: string]
  openUserProfile: [userEmail: string]
  toggleReply: [commentId: string]
  updateReplyDraft: [{ commentId: string, value: string }]
  submitReply: [parentId: string]
}>()

const {
  activeEditId,
  editDraft,
  isAdmin,
  canEditComment,
  canDeleteComment,
  isOwnComment,
  getUserRatingValue,
  startEditComment,
  updateEditDraft,
  cancelEditComment,
  saveEditComment,
  openDeleteComment
} = useArticleDetail()

const formatCommentTime = (value: string) => {
  const date = new Date(value)

  return new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const openProfile = () => {
  if (!props.comment.user_email) return

  emit('openUserProfile', props.comment.user_email)
}

const replyValue = computed(() => props.replyDrafts[props.comment.comment_id] ?? '')
const isReplying = computed(() => props.activeReplyId === props.comment.comment_id)
const isEditing = computed(() => activeEditId.value === props.comment.comment_id)
const initials = computed(() => props.comment.owner.slice(0, 1).toUpperCase())

const commentUserRating = computed(() => getUserRatingValue(props.comment.user_email))

const showEditAction = computed(() => canEditComment(props.comment) && !isEditing.value)
const showDeleteAction = computed(() => canDeleteComment(props.comment))
const showReportAction = computed(() => !isOwnComment(props.comment) && !isAdmin.value)
</script>

<template>
  <article class="comment-item">
    <div class="comment-item__header">
      <div class="comment-item__author">
        <button
          type="button"
          class="comment-item__avatar"
          :aria-label="`Lihat profil ${comment.owner}`"
          @click="openProfile"
        >
          {{ initials }}
        </button>

        <div class="comment-item__meta">
          <div class="comment-item__name-row">
            <button
              type="button"
              class="comment-item__name"
              @click="openProfile"
            >
              {{ comment.owner }}
            </button>

            <span v-if="commentUserRating" class="comment-item__rating">
              {{ commentUserRating }}/5
            </span>
          </div>

          <span class="comment-item__time">
            {{ formatCommentTime(comment.created_at) }}
            <span v-if="comment.updated_at" class="comment-item__edited">Diedit</span>
          </span>
        </div>
      </div>

      <div class="comment-item__actions">
        <button
          v-if="!isEditing"
          type="button"
          class="comment-item__reply-btn"
          @click="$emit('toggleReply', comment.comment_id)"
        >
          {{ isReplying ? 'Tutup' : 'Balas' }}
        </button>

        <DetailReportMenu
          :show-edit="showEditAction"
          :show-delete="showDeleteAction"
          :show-report="showReportAction"
          edit-label="Edit komentar"
          delete-label="Hapus komentar"
          report-label="Laporkan komentar"
          @edit="startEditComment(comment.comment_id)"
          @remove="openDeleteComment(comment.comment_id)"
          @report="$emit('openReport', comment.comment_id)"
        />
      </div>
    </div>

    <Transition name="glass-fade" mode="out-in">
      <div v-if="isEditing" class="comment-item__edit-box">
        <textarea
          :value="editDraft"
          class="comment-item__textarea"
          rows="4"
          placeholder="Edit komentar"
          @input="updateEditDraft(($event.target as HTMLTextAreaElement).value)"
          @keydown.ctrl.enter.prevent="saveEditComment"
        />

        <div class="comment-item__reply-actions">
          <BaseButton variant="ghost" @click="cancelEditComment">
            Batal
          </BaseButton>

          <BaseButton @click="saveEditComment">
            Simpan perubahan
          </BaseButton>
        </div>
      </div>

      <p v-else class="comment-item__body">
        {{ comment.comment_content }}
      </p>
    </Transition>

    <Transition name="glass-fade">
      <div v-if="isReplying && !isEditing" class="comment-item__reply-box">
        <textarea
          :value="replyValue"
          class="comment-item__textarea"
          rows="3"
          placeholder="Tulis balasan singkat..."
          @input="$emit('updateReplyDraft', { commentId: comment.comment_id, value: ($event.target as HTMLTextAreaElement).value })"
        />

        <div class="comment-item__reply-actions">
          <BaseButton variant="ghost" @click="$emit('toggleReply', comment.comment_id)">
            Batal
          </BaseButton>

          <BaseButton @click="$emit('submitReply', comment.comment_id)">
            Kirim balasan
          </BaseButton>
        </div>
      </div>
    </Transition>

    <div v-if="comment.children.length" class="comment-item__children">
      <DetailCommentItem
        v-for="child in comment.children"
        :key="child.comment_id"
        :comment="child"
        :active-reply-id="activeReplyId"
        :reply-drafts="replyDrafts"
        @open-report="$emit('openReport', $event)"
        @open-user-profile="$emit('openUserProfile', $event)"
        @toggle-reply="$emit('toggleReply', $event)"
        @update-reply-draft="$emit('updateReplyDraft', $event)"
        @submit-reply="$emit('submitReply', $event)"
      />
    </div>
  </article>
</template>

<style scoped>
.comment-item {
  padding: 16px;
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.22);
  border: 1px solid var(--glass-border);
}

.comment-item__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.comment-item__author {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.comment-item__avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--glass-border);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-surface);
  color: var(--text-primary);
  font-weight: 700;
  flex-shrink: 0;
  cursor: pointer;
  transition: var(--transition-fast);
}

.comment-item__avatar:hover {
  color: var(--primary-cyan);
  border-color: rgba(106, 173, 168, 0.32);
  background: rgba(106, 173, 168, 0.08);
}

.comment-item__meta {
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.comment-item__name-row {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.comment-item__name {
  border: none;
  background: transparent;
  padding: 0;
  color: var(--primary-red);
  font: inherit;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.comment-item__name:hover {
  text-decoration: underline;
}

.comment-item__rating {
  display: inline-flex;
  align-items: center;
  min-height: 22px;
  padding: 3px 7px;
  border-radius: 10px;
  background: rgba(106, 173, 168, 0.1);
  color: var(--primary-cyan);
  font-size: 11px;
  font-weight: 700;
  white-space: nowrap;
}

.comment-item__time {
  margin-top: 2px;
  font-size: 12px;
  color: var(--text-secondary);
}

.comment-item__edited {
  margin-left: 6px;
  color: var(--primary-cyan);
  font-weight: 600;
}

.comment-item__actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.comment-item__reply-btn {
  border: none;
  background: transparent;
  color: var(--primary-cyan);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.comment-item__reply-btn:hover {
  text-decoration: underline;
}

.comment-item__body {
  margin-top: 12px;
  color: var(--text-secondary);
  line-height: 1.65;
}

.comment-item__reply-box,
.comment-item__edit-box {
  margin-top: 14px;
  padding: 12px;
  border-radius: var(--radius-md);
  background: rgba(106, 173, 168, 0.06);
  border: 1px solid rgba(106, 173, 168, 0.12);
}

.comment-item__textarea {
  width: 100%;
  resize: vertical;
  min-height: 92px;
  border-radius: var(--radius-md);
  border: 1px solid var(--glass-border);
  background: var(--input-bg);
  color: var(--text-primary);
  padding: 14px;
  outline: none;
  font: inherit;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.comment-item__textarea:focus {
  border-color: rgba(106, 173, 168, 0.34);
}

.comment-item__reply-actions {
  margin-top: 12px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.comment-item__children {
  margin-top: 16px;
  margin-left: 24px;
  padding-left: 16px;
  border-left: 2px solid rgba(106, 173, 168, 0.2);
  display: grid;
  gap: 12px;
}

@media (max-width: 480px) {
  .comment-item__header {
    flex-direction: column;
  }

  .comment-item__actions {
    width: 100%;
    justify-content: space-between;
  }

  .comment-item__children {
    margin-left: 12px;
    padding-left: 12px;
  }

  .comment-item__reply-actions {
    flex-direction: column;
  }
}
</style>