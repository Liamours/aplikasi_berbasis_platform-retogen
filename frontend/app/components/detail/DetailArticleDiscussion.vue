<script setup lang="ts">
import OtherUserProfileModal from '~/components/profile/OtherUserProfileModal.vue'
import DetailReportUserModal from '~/components/detail/DetailReportUserModal.vue'

const {
  commentTree,
  totalComments,
  activeReplyId,
  replyDrafts,
  openReport,
  toggleReply,
  updateReplyDraft,
  submitComment
} = useArticleDetail()

const {
  otherProfile,
  otherProfileInitials,
  isOtherProfileOpen,
  isOtherLoading,
  otherErrorMessage,
  openOtherUserProfile,
  closeOtherUserProfile,
  formatDate
} = useUserProfile()

const {
  isOpen: isReportUserOpen,
  isSubmitting: isReportUserSubmitting,
  target: reportUserTarget,
  description: reportUserDescription,
  errorMessage: reportUserErrorMessage,
  showSuccessPopup: showReportUserSuccessPopup,
  successMessage: reportUserSuccessMessage,
  commentPreview: reportUserCommentPreview,
  canSubmit: canSubmitReportUser,
  openReportUser,
  closeReportUser,
  submitReportUser,
  closeSuccessPopup: closeReportUserSuccessPopup
} = useReportUser()
</script>

<template>
  <section class="article-comments">
    <div class="article-comments__header">
      <div>
        <h2 class="article-comments__title">Diskusi pengguna</h2>
        <p class="article-comments__subtitle">
          {{ totalComments }} komentar
        </p>
      </div>
    </div>

    <DetailArticleComposer />

    <div v-if="commentTree.length" class="article-comments__list">
      <DetailCommentItem
        v-for="comment in commentTree"
        :key="comment.comment_id"
        :comment="comment"
        :active-reply-id="activeReplyId"
        :reply-drafts="replyDrafts"
        @open-report="openReport('comment', $event)"
        @open-user-profile="openOtherUserProfile"
        @open-user-report="openReportUser"
        @toggle-reply="toggleReply"
        @update-reply-draft="updateReplyDraft"
        @submit-reply="submitComment"
      />
    </div>

    <div v-else class="article-comments__empty">
      Belum ada komentar. Jadilah yang pertama memulai diskusi.
    </div>
  </section>

  <OtherUserProfileModal
    :open="isOtherProfileOpen"
    :profile="otherProfile"
    :initials="otherProfileInitials"
    :is-loading="isOtherLoading"
    :error-message="otherErrorMessage"
    :format-date="formatDate"
    @close="closeOtherUserProfile"
  />

  <DetailReportUserModal
    v-model:description="reportUserDescription"
    :open="isReportUserOpen"
    :target="reportUserTarget"
    :comment-preview="reportUserCommentPreview"
    :is-submitting="isReportUserSubmitting"
    :can-submit="canSubmitReportUser"
    :error-message="reportUserErrorMessage"
    @close="closeReportUser"
    @submit="submitReportUser"
  />

  <BaseSuccessPopup
    v-if="showReportUserSuccessPopup"
    :message="reportUserSuccessMessage"
    @close="closeReportUserSuccessPopup"
  />
</template>

<style scoped>
.article-comments {
  margin-top: 28px;
  padding-top: 28px;
  border-top: 1px solid var(--glass-border);
}

.article-comments__header {
  margin-bottom: 16px;
}

.article-comments__title {
  font-size: 20px;
  line-height: 1.1;
  font-weight: 700;
  color: var(--text-primary);
}

.article-comments__subtitle {
  margin-top: 6px;
  color: var(--text-secondary);
  font-size: 13px;
}

.article-comments__list {
  margin-top: 16px;
  display: grid;
  gap: 14px;
}

.article-comments__empty {
  margin-top: 16px;
  padding: 16px;
  border-radius: var(--radius-md);
  border: 1px dashed var(--glass-border);
  color: var(--text-secondary);
  font-size: 13px;
  line-height: 1.6;
}
</style>