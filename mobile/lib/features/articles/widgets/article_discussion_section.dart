import 'package:flutter/material.dart';
import 'package:retogen/core/theme.dart';
import 'package:retogen/features/articles/models/article_detail.dart';
import 'package:retogen/features/articles/widgets/article_comment_tile.dart';
import 'package:retogen/features/articles/widgets/article_detail_shell.dart';

class ArticleDiscussionSection extends StatelessWidget {
  final ArticleDetail article;
  final TextEditingController commentController;
  final TextEditingController editController;
  final String? activeReplyId;
  final String? activeEditId;
  final bool isSaving;
  final Future<void> Function({String? parentId}) onSubmitComment;
  final void Function(String commentId) onToggleReply;
  final void Function(ArticleComment comment) onStartEdit;
  final VoidCallback onCancelEdit;
  final Future<void> Function(ArticleComment comment) onSaveEdit;
  final Future<void> Function(ArticleComment comment) onDelete;
  final Future<void> Function(ArticleComment comment) onReport;
  final TextEditingController Function(String commentId) resolveReplyController;
  final bool Function(ArticleComment comment) isOwnComment;

  const ArticleDiscussionSection({
    super.key,
    required this.article,
    required this.commentController,
    required this.editController,
    required this.activeReplyId,
    required this.activeEditId,
    required this.isSaving,
    required this.onSubmitComment,
    required this.onToggleReply,
    required this.onStartEdit,
    required this.onCancelEdit,
    required this.onSaveEdit,
    required this.onDelete,
    required this.onReport,
    required this.resolveReplyController,
    required this.isOwnComment,
  });

  @override
  Widget build(BuildContext context) {
    final comments = article.commentTree;

    return ArticleSectionCard(
      title: 'Diskusi pengguna',
      subtitle: '${article.totalComments} komentar',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _CommentComposer(
            controller: commentController,
            isSaving: isSaving,
            onSubmit: () => onSubmitComment(parentId: null),
          ),
          const SizedBox(height: 14),
          if (comments.isEmpty)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(14),
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.glassBorder),
              ),
              child: const Text(
                'Belum ada komentar. Jadilah yang pertama memulai diskusi.',
                style: TextStyle(
                  color: AppTheme.textSecondary,
                  fontSize: 13,
                  height: 1.6,
                ),
              ),
            )
          else
            ...comments.map(
              (comment) => Padding(
                padding: const EdgeInsets.only(bottom: 12),
                child: ArticleCommentTile(
                  comment: comment,
                  article: article,
                  isOwn: isOwnComment(comment),
                  activeReplyId: activeReplyId,
                  activeEditId: activeEditId,
                  replyController: resolveReplyController(comment.commentId),
                  editController: editController,
                  isSaving: isSaving,
                  onToggleReply: onToggleReply,
                  onSubmitReply: (id) => onSubmitComment(parentId: id),
                  onStartEdit: onStartEdit,
                  onCancelEdit: onCancelEdit,
                  onSaveEdit: onSaveEdit,
                  onDelete: onDelete,
                  onReport: onReport,
                  resolveReplyController: resolveReplyController,
                  isOwnComment: isOwnComment,
                ),
              ),
            ),
        ],
      ),
    );
  }
}

class _CommentComposer extends StatelessWidget {
  final TextEditingController controller;
  final bool isSaving;
  final VoidCallback onSubmit;

  const _CommentComposer({
    required this.controller,
    required this.isSaving,
    required this.onSubmit,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppTheme.glassBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Tulis komentar',
            style: TextStyle(
              color: AppTheme.textPrimary,
              fontSize: 16,
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 10),
          ArticleMultilineField(
            controller: controller,
            hintText: 'Bagikan pengalaman, pendapat, atau insight Anda...',
            minLines: 4,
          ),
          const SizedBox(height: 12),
          SizedBox(
            width: double.infinity,
            child: FilledButton.icon(
              onPressed: isSaving ? null : onSubmit,
              icon: isSaving
                  ? const SizedBox(
                      width: 16,
                      height: 16,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    )
                  : const Icon(Icons.send_outlined),
              label: const Text('Kirim komentar'),
              style: FilledButton.styleFrom(
                backgroundColor: AppTheme.primaryCyan,
                foregroundColor: Colors.white,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
