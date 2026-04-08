<script setup lang="ts">
interface CommentItem {
  comment_id: string
  parent_comment_id: string | null
  owner: string
  user_email: string
  comment_content: string
}

const props = defineProps<{
  comments: CommentItem[]
}>()

const groupedComments = computed(() => {
  const roots = props.comments.filter(comment => !comment.parent_comment_id)
  const replies = props.comments.filter(comment => comment.parent_comment_id)

  return roots.map(root => ({
    ...root,
    replies: replies.filter(reply => reply.parent_comment_id === root.comment_id)
  }))
})
</script>

<template>
  <div class="comment-thread">
    <div
      v-for="comment in groupedComments"
      :key="comment.comment_id"
      class="comment-thread__group"
    >
      <div class="comment-thread__item">
        <div class="comment-thread__header">
          <span class="comment-thread__owner">{{ comment.owner }}</span>
          <span class="comment-thread__email">{{ comment.user_email }}</span>
        </div>
        <p class="comment-thread__content">
          {{ comment.comment_content }}
        </p>
      </div>

      <div
        v-if="comment.replies.length"
        class="comment-thread__replies"
      >
        <div
          v-for="reply in comment.replies"
          :key="reply.comment_id"
          class="comment-thread__item comment-thread__item--reply"
        >
          <div class="comment-thread__header">
            <span class="comment-thread__owner">{{ reply.owner }}</span>
            <span class="comment-thread__email">{{ reply.user_email }}</span>
          </div>
          <p class="comment-thread__content">
            {{ reply.comment_content }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comment-thread {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.comment-thread__group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-thread__item {
  padding: 16px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.4);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.dark-mode .comment-thread__item {
  background: rgba(255, 255, 255, 0.03);
}

.comment-thread__item--reply {
  margin-left: 24px;
}

.comment-thread__replies {
  margin-left: 24px;
  padding-left: 16px;
  border-left: 2px solid rgba(0, 188, 212, 0.2);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-thread__header {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 8px;
}

.comment-thread__owner {
  color: var(--primary-red);
  font-weight: 600;
}

.comment-thread__email {
  color: var(--text-secondary);
  font-size: 13px;
}

.comment-thread__content {
  margin: 0;
  color: var(--text-primary);
  line-height: 1.6;
}
</style>