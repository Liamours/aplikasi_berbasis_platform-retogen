<script setup lang="ts">
const { commentTree, activeReplyId, replyDrafts, openReport, toggleReply, updateReplyDraft, submitComment } = useArticleDetail()
</script>

<template>
  <section class="article-comments">
    <div class="article-comments__header">
      <h2 class="article-comments__title">Diskusi</h2>
    </div>

    <div class="article-comments__list">
      <DetailCommentItem
        v-for="comment in commentTree"
        :key="comment.comment_id"
        :comment="comment"
        :active-reply-id="activeReplyId"
        :reply-drafts="replyDrafts"
        @open-report="openReport('comment', $event)"
        @toggle-reply="toggleReply"
        @update-reply-draft="updateReplyDraft"
        @submit-reply="submitComment"
      />
    </div>
  </section>
</template>

<style scoped>
.article-comments {
  margin-top: 28px;
  padding-top: 28px;
  border-top: 1px solid var(--glass-border);
}

.article-comments__header {
  margin-bottom: 18px;
}

.article-comments__title {
  font-size: 20px;
  line-height: 1.1;
  font-weight: 700;
  color: var(--text-primary);
}

.article-comments__list {
  display: grid;
  gap: 14px;
}
</style>
